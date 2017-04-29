# -*- coding: utf-8 -*-
from funcmap.mapper import FuncMapper

mapper = FuncMapper()  # initialise the funcmapper


@mapper.map(r'call my_func')
def my_func():
    """We can map simple functions.

    Just pass a phrase to the map decorator.
    """
    return 'I, my_func, have been called'


@mapper.map(r'(?P<first>\d+)\+(?P<second>\d+)')
def adder(first, second):
    """We can map functions with arguments.

    All named capture groups (this is a capture group named first: (?P<first>\d+)) are passed as keyword-arguments to
    function. So make sure the names of your capture groups fit the names of your function arguments.
    Unnamed capture groups as positional arguments are NOT supported to avoid some edge-cases!
    """
    return '{} + {} = {}'.format(first, second, int(first) + int(second))


@mapper.map(r'I am Fred')
@mapper.map(r'No, I am Joe')
def multi_name():
    """We can map multiple Regex-expressions to the same function."""
    return 'I have multiple names!'

if __name__ == '__main__':
    # get the function output by calling the mapper
    print(mapper('call my_func'))
    print(mapper('3+5'))
    print(mapper('10+2'))
    print(mapper('I am Fred'))
    print(mapper('No, I am Joe'))