# -*- coding: utf-8 -*-
from funcmap.mapper import FuncMapper

mapper = FuncMapper()  # initialise the funcmapper


@mapper.map(r'call my_func')
def my_func():
    """A simple function"""
    return 'I, my_func, have been called'


@mapper.map(r'(?P<first>\d+)\+(?P<second>\d+)')
def adder(first, second):
    """A simple function that adds numbers"""
    return '{} + {} = {}'.format(first, second, int(first) + int(second))


@mapper.map(r'name1')
@mapper.map(r'name2')
def multi_name():
    """A short demonstration of multiple decorators on one function."""
    return 'I have multiple names!'

if __name__ == '__main__':
    # get the function output by calling the mapper
    print(mapper('call my_func'))
    print(mapper('3+5'))
    print(mapper('10+2'))
    print(mapper('10+2'))
    print(mapper('name1'))
    print(mapper('name2'))