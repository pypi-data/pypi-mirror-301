# SynchroPy

SynchroPy is a synchronation libary for Python with easy code.


## Examples
### Threading
you can give a function this decorator, and when the function will be called, the decorator starts a thread, you can call it like a normal function.
~~~
from synchro import thread


@thread
def example(text):
    return text

example("test")  # Returns a concurrent.futures.Future
print(example.get_return_value())  # waiting for real return value

~~~
~~~ 
test 
~~~
