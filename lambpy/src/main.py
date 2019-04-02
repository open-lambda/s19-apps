import os

import numpy as np

from src.lampy import LamObject


def testcase(func):
    def wrapper():
        print(f"Start {func.__name__} ")
        func()
        print(f"End {func.__name__} \n")
        return

    return wrapper


@testcase
def test_basic_addition():
    a = LamObject([1, 2, 3])
    b = LamObject([1, 2, 3])
    d = LamObject([4])

    c = a + b + d
    c.run()

    print(c)
    assert ((c.val == np.array([6, 8, 10])).all())




if __name__ == '__main__':
    test_basic_addition()
