# tests/test_advanced_operations.py
from calculator.advanced_operations import power, square_root, factorial

def test_power():
    result = power(2, 3)
    print(f"test_power: {'Passed' if result == 8 else 'Failed'}")

def test_square_root():
    result = square_root(9)
    print(f"test_square_root: {'Passed' if result == 3 else 'Failed'}")
    try:
        square_root(-1)
        print("test_square_root_negative: Failed")
    except ValueError:
        print("test_square_root_negative: Passed")

def test_factorial():
    result = factorial(5)
    print(f"test_factorial: {'Passed' if result == 120 else 'Failed'}")

if __name__ == "__main__":
    test_power()
    test_square_root()
    test_factorial()
