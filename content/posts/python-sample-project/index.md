---
title: "Python: Sample Project"
date: "2023-02-01T12:00:00Z"
slug: "python-sample-project"
description: "Python is a high-level programming language that is widely used for web development, machine learning, scientific computing and more."
categories: ["technical"]
tags: ["project", "python"]
aliases: ["/wps/2023/02/01/python-sample-project/"]
recovered: "Internet Archive snapshot 2026-03-12"
---

Python is a high-level programming language that is widely used for web development, machine learning, scientific computing and more. In this blog post, we will be identify (and build) how to develop a simple python project with unit testing, publishing it finally as a binary and distribute it as source.

First, we will create a python module that contains a simple function. This function takes a number as an input and returns the square of that number. We will name this module as “square”.

```text
def square(x):
    return x * x
```

Next, we will write unit tests for this module. We will use the `unittest` module to write tests that check if the square function is working correctly.

```text
import unittest
import square

class TestSquare(unittest.TestCase):
    def test_square(self):
        self.assertEqual(square.square(2), 4)
        self.assertEqual(square.square(3), 9)

if __name__ == '__main__':
    unittest.main()
```

Once we have developed and tested our module, it’s time to distribute it. We will use the `pyinstaller` tool to generate a binary distribution of our module. Pyinstaller generates a standalone executable file that contains all the necessary dependencies, including python itself.

To generate a binary distribution, we need to run the following command:

```text
pyinstaller --onefile square.py
```

We can also publish our module as a source distribution. This is useful if the users want to modify the code or want to see how it works. To create a source distribution, we will use the `setup` module.

```text
from setuptools import setup

setup(
    name='square',
    version='1.0',
    description='A simple module to square a number',
    author='Your Name',
    author_email='your.email@example.com',
    py_modules=['square'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
```

To create a source distribution, we need to run the following command:

```text
python3 setup.py sdist
```

This will generate a source distribution archive in the dist directory. The users can download this archive, extract it, and install the module using the following command:

```text
pip3 install dist/square-1.0.tar.gz
```

### Conclusion

In this blog post, we have discussed how to develop a simple python project with unit testing, and publishing it as both a binary and source distribution. We have used the `pyinstaller` tool to generate a binary distribution and the `setup` module to create a source distribution.

Code available in [github](https://github.com/samarthya/pysample-one).
