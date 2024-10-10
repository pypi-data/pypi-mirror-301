# tests/test_logarithms.py
from calculator.logarithms import log, natural_log, exponential

def test_log():
    result = log(100, 10)
    print(f"test_log: {'Passed' if result == 2 else 'Failed'}")

def test_natural_log():
    result = round(natural_log(2.71828), 2)
    print(f"test_natural_log: {'Passed' if result == 1 else 'Failed'}")

def test_exponential():
    result = exponential(1)
    print(f"test_exponential: {'Passed' if result == 2.718281828459045 else 'Failed'}")

if __name__ == "__main__":
    test_log()
    test_natural_log()
    test_exponential()
