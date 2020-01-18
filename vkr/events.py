from math import sqrt
from transducers.api import Transducers as T
import sys
import random
from time import sleep


def piston(rate, iterable, target):
    for item in iterable:
        duration = random.expovariate(rate)
        sleep(duration)
        try:
            target.send(item)
        except StopIteration as e:
            return e.value
    target.close()
    return None


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return start


@coroutine
def my_print():
    try:
        first_item = (yield)
        print(str(first_item))
        while True:
            item = (yield)
            print(str(item))

    except GeneratorExit:
        print("end")


printer = my_print()


def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


piston(rate=0.5, iterable=range(1000), target=T.reactive_transduce(
    transducer=T.compose(T.filtering(is_prime), T.mapping(lambda x: x+1), T.repeating(3), T.chunking(3), T.enumerating()), target=printer))
