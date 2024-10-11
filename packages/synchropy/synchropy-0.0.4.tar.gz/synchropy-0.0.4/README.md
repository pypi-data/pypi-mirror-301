# SynchroPy

SynchroPy is a synchronation libary for Python with easy code.


## Examples
### Threading
you can give a function this decorator, and when the function will be called, the decorator starts a thread, you can call it like a normal function.
~~~
from synchro import thread


@thread
def example(text):
    print(f"text: {text}")

example("Text")
~~~
~~~ 
test 
~~~
### Channel
You can give a function your channel, like a pointer.
~~~
from synchro import Channel

channel = Channel()
channel.set(100)

def function(c: Channel):
    print(c.get())
    c.set(5)

print(channel.get())
~~~
~~~
100
5
~~~
