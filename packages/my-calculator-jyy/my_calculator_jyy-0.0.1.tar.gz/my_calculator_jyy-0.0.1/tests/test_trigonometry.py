# tests/test_trigonometry.py
from calculator.trigonometry import sine, cosine, tangent

def test_sine():
    result = round(sine(30), 2)
    print(f"test_sine: {'Passed' if result == 0.5 else 'Failed'}")

def test_cosine():
    result = round(cosine(60), 2)
    print(f"test_cosine: {'Passed' if result == 0.5 else 'Failed'}")

def test_tangent():
    result = round(tangent(45), 2)
    print(f"test_tangent: {'Passed' if result == 1 else 'Failed'}")

if __name__ == "__main__":
    test_sine()
    test_cosine()
    test_tangent()
