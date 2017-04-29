# -*- coding: utf-8 -*-
"""A simple demonstration how to start the infinite input loop to test the function calls.

It reuses all the functions from the example_functions.py file.
"""
from funcmap.examples.example_functions import mapper

if __name__ == '__main__':
    mapper.start_input_loop(catch_exceptions=True)