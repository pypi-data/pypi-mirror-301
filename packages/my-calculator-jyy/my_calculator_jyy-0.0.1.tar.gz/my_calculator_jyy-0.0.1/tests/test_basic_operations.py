# tests/test_basic_operations.py
from calculator.basic_operations import add, subtract, multiply, divide

# Basic Operations Tests
def test_add():
    result = add(2, 3)
    print(f"test_add: {'Passed' if result == 5 else 'Failed'}")

def test_subtract():
    result = subtract(5, 3)
    print(f"test_subtract: {'Passed' if result == 2 else 'Failed'}")

def test_multiply():
    result = multiply(2, 3)
    print(f"test_multiply: {'Passed' if result == 6 else 'Failed'}")

def test_divide():
    try:
        result = divide(6, 3)
        print(f"test_divide: {'Passed' if result == 2 else 'Failed'}")
        
        divide(5, 0)
        print("test_divide_zero: Failed")
    except ValueError:
        print("test_divide_zero: Passed")

if __name__ == "__main__":
    test_add()
    test_subtract()
    test_multiply()
    test_divide()
