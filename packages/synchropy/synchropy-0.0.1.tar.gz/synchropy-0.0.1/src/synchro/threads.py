import threading


def thread(*args, **kwargs):
    def wrapper(func):
        def _():
            def __():
                func(*args, **kwargs)
            thread = threading.Thread(target=__)
            thread.run()
        return _
    def stop():
        pass
    
    wrapper.stop = stop
    return wrapper









@thread("test")
def mythread(text):
    print(text)

mythread()
