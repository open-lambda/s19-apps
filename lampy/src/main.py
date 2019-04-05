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


@testcase
def test_basic_fetch():
    # Local
    base_dir = os.getcwd()
    matrix_path = os.path.join(base_dir, '../dump/a.np')

    a = LamObject(matrix_path)
    b = LamObject(matrix_path)
    d = LamObject([4])

    c = a + b + d
    c.run()

    print(c)
    assert ((c.val == np.array([6, 8, 10])).all())

@testcase
def test_remote_fetch():
    # TODO: will fail because not support https
    remote_path = "https://github.com/open-lambda/s19-apps/blob/master/lampy/dump/a.np?raw=true"
    # remote_path = "https://raw.githubusercontent.com/open-lambda/s19-apps/master/lampy/dump/a.json"
    matrix_path = os.path.join(remote_path)

    a = LamObject(matrix_path)
    b = LamObject(matrix_path)
    d = LamObject([4])

    c = a + b + d
    c.run()

    print(c)
    assert ((c.val == np.array([6, 8, 10])).all())


if __name__ == '__main__':
    # test_basic_addition()
    # test_basic_fetch()
    test_remote_fetch()
