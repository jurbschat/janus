from janus.const import State
import time
import asyncio
import threading
from janus.controllers.controllerbase import ControllerBase

class Axis:
    def __init__(self, loop, name, device):
        self.loop = loop
        self.name = name
        self.device = device
        self.target = 0
        self.target_sucesfully_written = 0
        self.reties = 5
        self.state = State.UNKNOWN
        self.execute_move_task = None
        self.lock = threading.Lock()
        self.move_tasks = []

    def set_position(self, pos):
        self.target = pos
        self._target_changed()

    def get_position(self):
        return self.device.position()

    def translate(self, offset):
        self.target = self.target + offset
        self._target_changed()

    def _target_changed(self):
        distance = abs(self.get_position() - self.target)
        if distance < 0.1:
            return
        with self.lock:
            if self.execute_move_task is not None:
                return
            #print("creating task")
            self.execute_move_task = asyncio.run_coroutine_threadsafe(self._coro_wrapper(self.target, True), self.loop)
            #print("task created ({}".format(self.execute_move_task))

    async def _coro_wrapper(self, target, abort):
        ret = await self._execute_move(target, abort)
        #print("task completed ({})".format(self.execute_move_task))
        with self.lock:
            self.execute_move_task = None

    async def _execute_move(self, new_position, abort_current):
        success = False
        for i in range(self.reties):
            if abort_current is True and self.device.state() == State.MOVING:
                #print("executing move while still moving, stopping move! (self: {}".format(self))
                self.device.stop()
            while self.device.state() == State.MOVING:
                #print("aborting, wait! (self: {})".format(self))
                await asyncio.sleep(0.05)
            success = self.device.position(new_position)
            if success:
                self.target_sucesfully_written = new_position
                success = True
                break
            else:
                print("unable to execute move with state: {}, retrying({})".format(i + 1, self.device.state()))
                await asyncio.sleep(0.5)
        if success is False:
            print("unable to execute move command, aborting")

    def get_state(self):
        return self.device.state()


class AxisController(ControllerBase):
    def __init__(self, axis_dict):
        self.loop = asyncio.get_event_loop()
        self.axis_dict = {key: Axis(self.loop, key, value) for key, value in axis_dict.items()}
        self.initial_axis_dict = axis_dict
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    def stop_controller(self):
        while True:
            shouldWait = False
            for axis in self.axis_dict:
                if self.axis_dict[axis].execute_move_task is not None:
                    shouldWait = True
                    break
            if shouldWait:
                time.sleep(0.5)
            else:
                break
        self.loop.call_soon_threadsafe(self.loop.stop)
        if self.thread is not None and self.thread.isAlive():
            self.thread.join()

    def set_position(self, axis_name, pos):
        self.axis_dict[axis_name].set_position(pos)

    def get_position(self, axis_name):
        return self.axis_dict[axis_name].get_position()

    def translate(self, axis_name, offset):
        pos = self.get_position(axis_name)
        self.axis_dict[axis_name].set_position(pos + offset)

    def state(self, axis_name):
        return self.axis_dict[axis_name].state()
