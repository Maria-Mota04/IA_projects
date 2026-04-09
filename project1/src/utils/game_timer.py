import time


class GameTimer:
    def __init__(self):
        self.start_time = time.time()
        self.paused_time = 0
        self.pause_start = None
        self.is_paused = False

    def pause(self):
        if not self.is_paused:
            self.pause_start = time.time()
            self.is_paused = True

    def resume(self):
        if self.is_paused:
            self.paused_time += time.time() - self.pause_start
            self.is_paused = False

    def get_time(self):
        if self.is_paused:
            return self.pause_start - self.start_time - self.paused_time
        return time.time() - self.start_time - self.paused_time

    def reset(self):
        self.start_time = time.time()
        self.paused_time = 0
        self.pause_start = None
        self.is_paused = False
