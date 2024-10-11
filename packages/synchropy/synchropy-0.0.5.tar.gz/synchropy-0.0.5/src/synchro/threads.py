import concurrent.futures
import queue
class thread_wrapper:
        def __init__(self, func):
            self.func = func
            self.return_value = queue.Queue()
        def __call__(self, *args, **kwargs) -> concurrent.futures.Future:
            def __():
                self.return_value.put(self.func(*args, **kwargs))
            with concurrent.futures.ThreadPoolExecutor() as e:
                e.submit(__)
        def get_return_value(self):
            return self.return_value.get()
def thread(func):
    return thread_wrapper(func) 
    
    
    





