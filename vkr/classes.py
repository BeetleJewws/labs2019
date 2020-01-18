class Reducer:
    # Interface of a reducer

    def __init__(self, reducer):
        # Takes reducing function
        pass

    def initial(self):
        # Initial seed
        pass

    def step(self, result, item):
        # Iterating step in reduction process
        pass

    def complete(self, result):
        # Summorize
        pass


class Reduced:
    # Mark sequence with a flag
    # Flag indicates end of a reduction process

    def __init__(self, setting_flag):
        self._flag = setting_flag

    @property
    def flag(self):
        return self._flag


class First:
    # Returns only first entry
    # By marking sequence with "Reduced" flag

    def __init__(self, reducer, predicate):
        self.reducer = reducer
        self.predicate = predicate

    def initial(self):
        return self.reducer.initial()

    def step(self, result, item):
        return Reduced(self.reducer.step(result, item)) if self.predicate(item) else result

    def complete(self, result):
        return self.reducer.complete(result)


class SingleStep:
    # Assumes that a result will contain only one element of the sequence

    def __init__(self):
        self.steps = 0

    def initial(self):
        return None

    def step(self, result, item):
        assert result is None
        self.steps += 1
        if self.steps > 1:
            raise RuntimeError("Too many")
        return item

    def complete(self, result):
        if self.steps < 1:
            raise RuntimeError("Too few")
        return result


class Filtering:
    # Filter implementation of transducer

    def __init__(self, reducer, predicate):
        self.reducer = reducer
        self.predicate = predicate

    def initial(self):
        return self.reducer.initial()

    def step(self, result, item):
        if self.predicate(item):
            return self.reducer.step(result, item)
        return result

    def complete(self, result):
        return self.reducer.complete(result)


class Mapping:
    # Mapping implementation of transducer

    def __init__(self, reducer, transform):
        self.reducer = reducer
        self.transform = transform

    def initial(self):
        return self.reducer.initial()

    def step(self, result, item):
        return self.reducer.step(result, self.transform(item))

    def complete(self, result):
        return self.reducer.complete(result)


class Appending:
    # for mutable sequences

    def initial(self):
        return []

    def step(self, result, item):
        result.append(item)
        return result

    def complete(self, result):
        return result


class Conjoining:
    # for immutable sequences

    def initial(self):
        return tuple()

    def step(self, result, item):
        return result + type(result)((item,))

    def complete(self, result):
        return result


class Enumerating:
    # Creates a pair
    # First element - accumulating index
    # Second element - item of reducting sequence

    def __init__(self, reducer, start):
        self.reducer = reducer
        self.index = start

    def initial(self):
        return self.reducer.initial()

    def step(self, result, item):
        i = self.index
        self.index += 1
        return self.reducer.step(result, (i, item))

    def complete(self, result):
        return self.reducer.complete(result)


class Chunking:
    # Splits (Combines) elements into groups of specific size

    def __init__(self, reducer, size):
        self.reducer = reducer
        self.size = size
        self.pending = []

    def initial(self):
        return self.reducer.initial()

    def step(self, result, item):
        self.pending.append(item)
        if len(self.pending) == self.size:
            batch = self.pending
            self.pending = []
            return self.reducer.step(result, batch)
        return result

    def complete(self, result):
        if len(self.pending) > 0:
            r = self.reducer.step(result, self.pending)
        else:
            r = result
        return self.reducer.complete(r)


class Repeating:
    # Repeats each element of reducting sequence n-times

    def __init__(self, reducer, num_times):
        self.reducer = reducer
        self.steps = num_times

    def initial(self):
        return self.reducer.initial()

    def step(self, result, item):
        for _ in range(self.steps):
            result = self.reducer.step(result, item)
        return result

    def complete(self, result):
        return self.reducer.complete(result)


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return start


@coroutine
def null_sink():
    while True:
        _ = (yield)


class Sending:
    # Appender to specified sink

    def initial(self):
        # kick-start
        return null_sink()

    def step(self, result, item):
        try:
            result.send(item)
        except StopIteration:
            return Reduced(result)
        else:
            return result

    def complete(result):
        #  closing of the generator
        result.close()
        return result
