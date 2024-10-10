# tests/test_statistics.py
from calculator.statistics import mean, median, mode, standard_deviation

def test_mean():
    result = mean([1, 2, 3, 4, 5])
    print(f"test_mean: {'Passed' if result == 3 else 'Failed'}")

def test_median():
    result = median([1, 2, 3, 4, 5])
    print(f"test_median: {'Passed' if result == 3 else 'Failed'}")

def test_mode():
    result = mode([1, 1, 2, 2, 2, 3])
    print(f"test_mode: {'Passed' if result == 2 else 'Failed'}")

def test_standard_deviation():
    result = round(standard_deviation([1, 2, 3, 4, 5]), 2)
    print(f"test_standard_deviation: {'Passed' if result == 1.58 else 'Failed'}")

if __name__ == "__main__":
    test_mean()
    test_median()
    test_mode()
    test_standard_deviation()
