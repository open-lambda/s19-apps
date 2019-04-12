from src.lampy import LampyObject


def test_addition():
    a = LampyObject([1, 2, 3])
    print(a)

    b = LampyObject([1, 2, 3])
    print(a)

    c = a + b
    print(c.shape)
    print(c)


def test_multiplication():
    a = LampyObject([1, 2, 3])
    print(a)

    b = LampyObject([1, 2, 3])
    print(a)

    c = LampyObject( [[1, 2, 3], [1, 2, 3]] )

    d = a * b
    print(d.shape)
    print(d)

    e = c * b
    print(e.shape)
    print(e)


if __name__ == '__main__':
    test_multiplication()