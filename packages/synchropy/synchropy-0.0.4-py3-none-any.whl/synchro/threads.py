import threading


def thread(func):
    def wrapper(*args, **kwargs):
        def __():
                func(*args, **kwargs)
        thread = threading.Thread(target=__)
        thread.run()
    return wrapper   
    
    
    









