from math import sqrt
from transducers.api import Transducers as T
import sys
import random
from time import sleep
import time


def coroutine(func):
    def start(*args, **kwargs):
        g = func(*args, **kwargs)
        next(g)
        return g
    return start


class Generator:

    def __init__(self, target, master, transducer=None, reducer=None, action=None, data='Test'):
        self.data = data
        self.target = target
        self.master = master
        self.trasducer = transducer
        self.reducer = reducer

        self.cashe = {}

        print("Generator is created:", data)

        this = self

        @coroutine
        def generator():
            try:
                print('Generator is starting:', data)
                while True:
                    iterrable = (yield)

                    if this.cashe.get(tuple(iterrable)) == None:
                        if transducer is not None:
                            new_itterable = T.transduce(
                                transducer, reducer, iterrable)
                            this.cashe[tuple(iterrable)] = new_itterable
                            print('.', data, new_itterable)
                        else:
                            if action is not None:
                                new_itterable = action(iterrable)
                                this.cashe[tuple(iterrable)] = new_itterable
                                print('.', data, new_itterable)
                    else:
                        new_itterable = this.cashe[tuple(iterrable)]
                        print('.c', data, new_itterable)

                    try:
                        if this.target == None:
                            pass
                        else:
                            this.target.send(new_itterable)
                    except StopIteration as e:
                        return e.value

            except GeneratorExit:
                print("Generator is closing:", data)

        self.generator = generator()

    def get(self):
        return self.generator

    def set_target(self, target):
        self.target = target


class master:

    def __init__(self):
        self.generators = {}

        for i in range(4):
            pass

    def create_generator(self, target=None, transducer=None, reducer=None, action=None, data="Non-specified"):
        if (transducer is not None) & (reducer is not None):
            if self.generators.get(tuple([transducer, reducer])) == None:
                new_generator = Generator(
                    target=target, master=self, transducer=transducer, reducer=reducer, data=data)
                self.generators[tuple([transducer, reducer])] = new_generator
                return new_generator
            else:
                generator = self.generators.get(tuple([transducer, reducer]))
                generator.set_target(target)
                return generator
        else:
            if action is not None:
                if self.generators.get(tuple([action])) == None:
                    new_generator = Generator(
                        target=target, master=self, action=action, data=data)
                    return new_generator
                else:
                    generator = self.generators.get(tuple([action]))
                    generator.set_target(target)
                    return generator

    def solve(self, transducers=None, actions=None, target=None, reducer=T.get_mutable_appender()):
        current_target = target
        for action in reversed(actions):
            a = self.create_generator(
                target=current_target, action=action, data=action.__name__)
            current_target = a.get()

        for transducer in reversed(transducers):
            a = self.create_generator(
                target=current_target, transducer=transducer, reducer=reducer, data="Transducer")
            current_target = a.get()

        return current_target


def input(iterable, target):
    l = 0
    data = []
    for item in iterable:
        l = l + 1
        data.append(item)
        if l > 3:
            l = 0
            try:
                print('data:', data)
                target.send(data)
            except StopIteration as e:
                return e.value
            data = []
    return None


@coroutine
def output():
    try:
        while True:
            item = (yield)
            print('Result:', str(item))

    except GeneratorExit:
        print("end")


# g0 = master.create_generator(target=None, transducer=T.compose(
#     T.mapping(lambda x: print(x))), reducer=T.get_mutable_appender())
# g1 = master.create_generator(
#     target=printer, transducer=T.compose(T.mapping(lambda x: pow(x, (x*15+x*x*23)/(x*x*x*x*45)))), reducer=T.get_mutable_appender())
# g2 = master.create_generator(
#     target=g1.get(), transducer=T.compose(T.filtering(is_prime)), reducer=T.get_mutable_appender())
# new1 = Generator(data='new1', target=printer, master=master)
# new2 = Generator(data="new2", target=new1.get(), master=master)

# start_time = time.time()
# piston(rate=0.5, iterable=range(15), target=g2.get())
# print("--- %s seconds ---" % (time.time() - start_time))

# print('\nCashed:\n')

# start_time = time.time()
# piston(rate=0.5, iterable=range(15), target=g2.get())
# print("--- %s seconds ---" % (time.time() - start_time))


def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


def test1(data):
    # Any actions
    return data


def test2(data):
    # Any actions
    return data


master = master()
output_sink = output()


transducer2 = T.compose(T.mapping(lambda x: x), T.filtering(is_prime))
transducer1 = T.compose(T.mapping(lambda x: x+1),
                        T.filtering(lambda x: True if x > 1 else False))

chain = master.solve(transducers=[transducer1, transducer2], actions=[
                     test1, test2], target=output_sink)

input(iterable=range(15), target=chain)


print('\nCashed:\n')


input(iterable=range(20), target=chain)
