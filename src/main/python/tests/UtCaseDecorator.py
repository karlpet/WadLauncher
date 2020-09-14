import unittest

def ut_case(test_func):
    case = unittest.TestCase()

    def inner():
        test_func(case)

    return inner
