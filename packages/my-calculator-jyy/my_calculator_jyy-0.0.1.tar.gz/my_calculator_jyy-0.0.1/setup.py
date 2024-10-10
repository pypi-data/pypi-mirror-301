from setuptools import setup, find_packages

setup(
    name="my_calculator_jyy",
    version="0.0.1",
    packages=find_packages(),
    description="A comprehensive calculator module for various mathematical operations",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # Ensure this is included for Markdown README
    author="Jewon Yeon",
    author_email="jewon.yeon@sjsu.edu",
    url="https://github.com/yeon971105/my_calculator",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)

