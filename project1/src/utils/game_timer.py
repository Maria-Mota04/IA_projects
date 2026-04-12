import time


class GameTimer:
    def __init__(self):
        """@brief Initialize timer and pause bookkeeping fields."""
        self.start_time = time.time()
        self.paused_time = 0
        self.pause_start = None
        self.is_paused = False

    def get_time(self):
        """
        @brief Return elapsed active time in seconds.

        @return Elapsed non-paused time.
        """
        if self.is_paused:
            return self.pause_start - self.start_time - self.paused_time
        return time.time() - self.start_time - self.paused_time

    def reset(self):
        """@brief Reset timer to initial running state."""
        self.start_time = time.time()
        self.paused_time = 0
        self.pause_start = None
        self.is_paused = False
