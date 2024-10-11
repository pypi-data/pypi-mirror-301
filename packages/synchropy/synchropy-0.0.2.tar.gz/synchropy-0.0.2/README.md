# SynchroPy

SynchroPy is a synchronation libary for Python with easy code.


## Examples
### Threading
~~~
from synchro import thread


@thread()
def example(text):
    print(f"text: {text}")

example("Text")