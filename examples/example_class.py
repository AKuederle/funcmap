# -*- coding: utf-8 -*-
"""When using funcmapper with instance methods, you can ot use the decorator syntax.
Instead you need to perform the mapping after the instance is created.
The best place to do this is the init method of your class.
This ensures, that each instance has its own funcmap and the self context is available inside the methods.
"""
from funcmap import FuncMapper


class TestClass:
    def __init__(self):
        self.mapper = FuncMapper() # initialise the funcmapper

        # Map the class methods using functional mapping
        self.mapper.map(r'call my_func', self.my_func)
        self.mapper.map(r'(?P<first>\d+)\+(?P<second>\d+)', self.adder)
        self.mapper.map(r'I am Fred', self.multi_name)
        self.mapper.map(r'No, I am Joe', self.multi_name)

    def my_func(self):
        """We can map simple functions.

        Just pass a phrase to the map decorator.
        """
        return 'I, my_func, have been called'

    def adder(self, first, second):
        """We can map functions with arguments.

        All named capture groups (this is a capture group named first: (?P<first>\d+)) are passed as keyword-arguments to
        function. So make sure the names of your capture groups fit the names of your function arguments.
        Unnamed capture groups as positional arguments are NOT supported to avoid some edge-cases!
        """
        return '{} + {} = {}'.format(first, second, int(first) + int(second))

    def multi_name(self):
        """We can map multiple Regex-expressions to the same function."""
        return 'I have multiple names!'


if __name__ == '__main__':
    # get the function output by calling the mapper
    test = TestClass()
    print(test.mapper('call my_func'))
    print(test.mapper('3+5'))
    print(test.mapper('10+2'))
    print(test.mapper('I am Fred'))
    print(test.mapper('No, I am Joe'))