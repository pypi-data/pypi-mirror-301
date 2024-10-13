import time
import random

class Retrier:
    def __init__(self, max_retries=5, base_delay=1.0, jitter=0.5):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.jitter = jitter

    def execute(self, func, *args, **kwargs):
        retries = 0
        while retries < self.max_retries:
            response = func(*args, **kwargs)
            if response.status_code == 200:
                return response
            elif response.status_code == 429 or response.status_code >= 500:
                retries += 1
                sleep_time = self.base_delay * (2 ** retries) + random.uniform(0, self.jitter)
                time.sleep(sleep_time)
            else:
                return response
        return None