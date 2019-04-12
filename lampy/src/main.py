# from src.lampy import LampyOperator
import time

import src.lampy as np


def testfunc(func):
    def wrapper():
        print(f"<-[Test]-- {func.__name__} start")
        st = time.time_ns() / 1000000
        func()
        ed = time.time_ns() / 1000000
        print(f"<-[Test]-- {func.__name__} end\n"
              f"        Exec Time: {ed - st} (ms)\n")

    return wrapper


@testfunc
def test_addition():
    a = np.array([1, 2, 3])
    print(a)

    b = np.array([1, 2, 3])
    print(a)

    c = a + b
    print(c.status)

    print(c.shape); print(c.status)
    print(c); print(c.status)

    d = 2 + c
    print(d.shape)
    print(d)


@testfunc
def test_multiplication():
    a = np.array([1, 2, 3])
    print(a)

    b = np.array([1, 2, 3])
    print(a)

    c = np.array([[1, 2, 3], [1, 2, 3]])

    d = a * b
    print(d.shape)
    print(d)

    e = c * b
    print(e.shape)
    print(e)


@testfunc
def test_dot_product():
    a = np.array([1, 2, 3])
    b = np.array([1, 2, 3])
    d = a.dot(b)
    print(d.shape)
    print(d)


@testfunc
def test_conv():
    a = np.array([1, -1, 1])
    b = np.array([1, 1, 1, 1, 1])
    d = a.conv(b)
    print(d.shape)
    print(d)


@testfunc
def test_conv2d():
    # TODO: a bit buggy...
    pass


@testfunc
def test_remote_fetch():
    a = np.array("https://raw.githubusercontent.com/open-lambda/s19-apps/master/lampy/dump/a.json")
    b = np.array("https://raw.githubusercontent.com/open-lambda/s19-apps/master/lampy/dump/a.json")
    print(a.status)
    print(b.status)
    c = a * b + b * a + a * a
    print(a.status)
    print(b.status)
    print(c.status)
    # print(c.shape)
    print(c)
    print(a.status)
    print(b.status)
    print(c.status)
    pass


@testfunc
def test_mult_const():
    a = np.array([1, 2, 3])
    print(a)
    b = a * 2
    print(b)
    c = 2 * a
    print(c)


@testfunc
def demo():
    url = "https://raw.githubusercontent.com/open-lambda/s19-apps/master/lampy/dump/a.json"
    a = np.array(url)
    b = np.array(url)
    print(a)
    print(a.status)
    print(b)
    print(b.status)

    c = a + b
    print(c.status)

    print(c.shape)
    print(c.status)

    print(c)
    print(c.status)




if __name__ == '__main__':
    test_addition()
    test_multiplication()
    test_dot_product()
    test_conv()
    test_remote_fetch()
    test_mult_const()
