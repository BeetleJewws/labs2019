from functools import reduce
from itertools import chain
from transducers.classes import *
from collections import deque

UNSET = object()


class Transducers:

    def coroutine(func):
        def start(*args, **kwargs):
            g = func(*args, **kwargs)
            next(g)
            return g
        return start

    @coroutine
    def reactive_transduce(transducer, target=None):
        reducer = transducer(Sending())
        accumulator = target if (target is not None) else reducer.initial()
        try:
            while True:
                item = (yield)
                accumulator = reducer.step(accumulator, item)
                if isinstance(accumulator, Reduced):
                    accumulator = accumulator.value
                    break
        except GeneratorExit:
            pass
        return reducer.complete(accumulator)

    def transduce(transducer, reducer, iterable, init=UNSET):
        r = transducer(reducer)
        accumulator = init if (init is not UNSET) else reducer.initial()
        for item in iterable:
            accumulator = r.step(accumulator, item)
            if isinstance(accumulator, Reduced):
                accumulator = accumulator.flag
                break
        return r.complete(accumulator)

    def compose(f, *fs):
        """
        Composition of functions right -> left

        compose(a, b, c)(x) -> a(b(c(x)))

        Args:
        f, *fs: Start and the rest - callables
        Right functon can accept any arguments of type "X"

        Returns:
        The composition of the argument functions. 
        """

        rfs = list(chain([f], fs))
        rfs.reverse()

        def composed(*args, **kwargs):
            return reduce(
                lambda result, fn: fn(result),
                rfs[1:],
                rfs[0](*args, **kwargs))
        return composed

    def transducer(reducer):
        return Reducer(reducer)

    def filtering(predicate):

        def filtering_transducer(reducer):
            return Filtering(reducer, predicate)

        return filtering_transducer

    def mapping(transform):

        def mapping_transducer(reducer):
            return Mapping(reducer, transform)

        return mapping_transducer

    def enumerating(start=0):

        def enumerating_transducer(reducer):
            return Enumerating(reducer, start)

        return enumerating_transducer

    def chunking(size):
        if size < 1:
            raise ValueError("<1")

        def chunking_transducer(reducer):
            return Chunking(reducer, size)

        return chunking_transducer

    def true(*args, **kwargs):
        return True

    def first(predicate=None):
        if predicate is None:
            predicate = true

        def first_transducer(reducer):
            return First(reducer, predicate)

        return first_transducer

    def repeating(num_times):

        if num_times < 0:
            raise ValueError("negative")

        def repeating_transducer(reducer):
            return Repeating(reducer, num_times)

        return repeating_transducer

    def single():
        return SingleStep()

    def get_mutable_appender():

        return Appending()

    def get_immutable_appender():
        # Conjoiner takes immutable sequences
        return Conjoining()
