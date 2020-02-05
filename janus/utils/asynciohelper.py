import threading
import asyncio

class ThreadedEventLoop:

    def __init__(self):
        self.event_loop = None
        self.shutdown_event = False
        self.thread = threading.Thread(target=self.run_loop_fct, name="AsyncLoop")
        self.startup_wait_event = threading.Event()
        self.thread.start()
        self.startup_wait_event.wait()

    def get_event_loop(self):
        return self.event_loop

    def start_event_loop(self):
        if self.thread.is_alive():
            return
        self.thread.start()

    def stop_event_loop(self):
        self.shutdown_event = True
        self.thread.join()
        pass

    async def event_loop_shutdown_poller(self):
        asyncio.Task.current_task().name = "Shutdown Task"
        while not self.shutdown_event:
            await asyncio.sleep(0.25)
        pass

    def run_loop_fct(self):
        self.event_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.event_loop)
        print("START coro event loop")
        self.startup_wait_event.set()
        self.event_loop.run_until_complete(self.event_loop_shutdown_poller())
        self.event_loop.stop()
        print("SHUTDOWN coro event loop")