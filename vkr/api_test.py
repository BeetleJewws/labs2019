import unittest
from transducers.api import Transducers as T

from math import sqrt


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.appending = T.get_mutable_appender()
        self.conjoining = T.get_immutable_appender()

    def test_appending_reducer(self):
        self.assertEqual(
            self.appending.__class__.__name__, 'Appending')

        result = T.transduce(T.compose(T.mapping(lambda x: x)),
                             self.appending, range(5))
        self.assertEqual([0, 1, 2, 3, 4], result)

    def test_conj_reducer(self):
        conj_reducer = T.get_immutable_appender()
        self.assertEqual(self.conjoining.__class__.__name__, 'Conjoining')

        result = T.transduce(T.compose(T.mapping(lambda x: x)),
                             self.conjoining, range(5))
        self.assertEqual((0, 1, 2, 3, 4), result)

    def test_transduce(self):
        transducer = T.compose(T.filtering(is_prime), T.mapping(
            lambda x: x+1))

        self.assertEqual(transducer.__class__.__name__, 'function')

        result = T.transduce(transducer, self.appending, range(20))
        self.assertEqual([3, 4, 6, 8, 12, 14, 18, 20], result)

    def test_chunking(self):
        transducer = T.compose(T.mapping(lambda x: x*x), T.chunking(2))

        result = T.transduce(transducer, self.appending, range(5))
        self.assertEqual([[0, 1], [4, 9], [16]], result)

    def test_repeating(self):
        transducer = T.compose(T.mapping(lambda x: x*x), T.repeating(2))

        result = T.transduce(transducer, self.appending, range(2))
        self.assertEqual([0, 0, 1, 1], result)

    def test_first(self):
        transducer = T.compose(T.filtering(lambda x: True if x > 4 else False), T.first(
            lambda x: True if x*x > 64 else False))

        result = T.transduce(transducer, T.single(), range(1000))
        self.assertEqual(9, result)

    def test_enumerating(self):
        transducer = T.compose(T.mapping(lambda x: x*2+3), T.enumerating())

        result = T.transduce(transducer, self.appending, range(4))
        self.assertEqual([(0, 3), (1, 5), (2, 7), (3, 9)], result)


def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(sqrt(x)) + 1):
        if x % i == 0:
            return False
    return True


if __name__ == '__main__':
    unittest.main()
