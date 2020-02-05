from janus.const import State
import time
import asyncio
import threading
from janus.utils.asynciohelper import ThreadedEventLoop
from janus.controllers.controllerbase import ControllerBase

class GridAxisNames:
    AXIS_X = "grid_x"
    AXIS_Y = "grid_y"
    AXIS_Z = "grid_z"

class Axis:
    def __init__(self, event_loop, name, device):
        self.event_loop = event_loop
        self.name = name
        self.device = device
        self.target = 0
        self.target_successfully_written = 0
        self.reties = 5
        self.execute_move_task = None
        self.move_tasks = []
        self.state = State(self.device.state())
        self.lock = threading.Lock()

    def set_position(self, pos, abort=False):
        self.target = pos
        self._target_changed(abort)

    def get_position(self, refresh=False):
        return self.device.position(refresh=refresh)

    def translate(self, offset):
        self.target = self.target + offset
        self._target_changed()

    def _target_changed(self, abort):
        distance = abs(self.get_position() - self.target)
        if distance < 0.1:
            return
        with self.lock:
            if self.execute_move_task is not None:
                return
            self.state = State.MOVING
            self.execute_move_task = asyncio.run_coroutine_threadsafe(self._coro_wrapper(self.target, abort), loop=self.event_loop)

    async def _coro_wrapper(self, target, abort):
        asyncio.Task.current_task().name = "MOVE: (x: {}, y:{})".format(target.x(), target.y())
        ret = await self._execute_move(target, abort)
        with self.lock:
            self.execute_move_task = None

    async def _execute_move(self, new_position, abort_current):
        success = False
        for i in range(self.reties):
            if abort_current is True and self.device.state() == State.MOVING:
                self.device.stop()
            while self.device.state() == State.MOVING:
                await asyncio.sleep(0.05)
            print("executing move")
            success = self.device.position(new_position)
            if success:
                self.target_successfully_written = new_position
                success = True
                break
            else:
                print("unable to execute move with state: {}, retrying({})".format(i + 1, self.device.state()))
                await asyncio.sleep(0.5)
        if success is False:
            print("unable to execute move command, aborting")
        while self.device.state(True) == State.MOVING:
            await asyncio.sleep(0.05)
        self.state = State(self.device.state(True))

    def get_state(self):
        return self.state

class AxisController(ControllerBase):
    def __init__(self, axis_dict):
        self.threaded_event_loop = None #ThreadedEventLoop()
        self.axis_dict = {key: Axis(None, key, value) for key, value in axis_dict.items()}
        self.initial_axis_dict = axis_dict

    def stop_controller(self):
        return
        while True:
            should_wait = False
            for axis in self.axis_dict:
                if self.axis_dict[axis].execute_move_task is not None:
                    should_wait = True
                    break
            if should_wait:
                time.sleep(0.5)
            else:
                break
        self.threaded_event_loop.stop_event_loop()

    def get_limits(self):
        limits = {}
        for axis in self.axis_dict:
            cw = self.axis_dict[axis].device.soft_limit_min()
            ccw = self.axis_dict[axis].device.soft_limit_max()
            limits[axis] = [cw, ccw]
        return limits

    def set_position(self, axis_name, pos, abort=False):
        self.axis_dict[axis_name].set_position(pos, abort)

    def get_position(self, axis_name, refresh=False):
        return self.axis_dict[axis_name].get_position(refresh=refresh)

    def translate(self, axis_name, offset):
        pos = self.get_position(axis_name)
        self.axis_dict[axis_name].set_position(pos + offset)

    def state(self, axis_name):
        return self.axis_dict[axis_name].get_state()

    def all_moves_completed(self):
        for axis in self.axis_dict:
            state = self.axis_dict[axis].get_state()
            if state == State.MOVING:
                return False
        return True
