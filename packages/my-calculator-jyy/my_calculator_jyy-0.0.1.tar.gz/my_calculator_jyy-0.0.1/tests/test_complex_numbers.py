# tests/test_complex_numbers.py
from calculator.complex_numbers import add_complex, subtract_complex, multiply_complex, divide_complex

def test_add_complex():
    result = add_complex(1 + 2j, 2 + 3j)
    print(f"test_add_complex: {'Passed' if result == (3 + 5j) else 'Failed'}")

def test_subtract_complex():
    result = subtract_complex(5 + 6j, 2 + 3j)
    print(f"test_subtract_complex: {'Passed' if result == (3 + 3j) else 'Failed'}")

def test_multiply_complex():
    result = multiply_complex(1 + 2j, 3 + 4j)
    print(f"test_multiply_complex: {'Passed' if result == (-5 + 10j) else 'Failed'}")

def test_divide_complex():
    try:
        result = divide_complex(1 + 2j, 3 + 4j)
        expected_result = (0.44 + 0.08j)
        print(f"test_divide_complex: {'Passed' if round(result.real, 2) == round(expected_result.real, 2) and round(result.imag, 2) == round(expected_result.imag, 2) else 'Failed'}")
        
        divide_complex(1 + 2j, 0)
        print("test_divide_complex_by_zero: Failed")
    except ValueError:
        print("test_divide_complex_by_zero: Passed")

if __name__ == "__main__":
    test_add_complex()
    test_subtract_complex()
    test_multiply_complex()
    test_divide_complex()
