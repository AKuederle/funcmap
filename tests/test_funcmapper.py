# -*- coding: utf-8 -*-
"""Base Tests for the FuncMapper Class"""
import unittest

import re
try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from funcmap.mapper import FuncMapper, NotSupportedError


class TestMapping(unittest.TestCase):
    """All tests for mapping a function."""

    def setUp(self):
        """Set up."""
        self.mapper = FuncMapper()

    def test_simple_map(self):
        """Test that simple mapping of a function works."""
        def test_func(): pass
        self.mapper.map('test')(test_func)
        self.assertEqual(self.mapper._mapped_functions['test'], test_func)
        self.assertEqual(self.mapper._mapped_regex['test'], re.compile('test'))

    def test_kwargs_map(self):
        """Test that mapping with kwargs works."""
        def test_func(kwarg1, kwarg2): pass
        regex = r'test (?P<kwarg1>.+) (?P<kwarg2>.+)'
        self.mapper.map(regex)(test_func)
        self.assertEqual(self.mapper._mapped_functions[regex], test_func)
        self.assertEqual(self.mapper._mapped_regex[regex], re.compile(regex))

    def test_args_map_failed(self):
        """Test that mapping with unnamed capture groups fails."""
        def test_func(arg1, arg2): pass
        regex = r'test (.+) (.+)'
        with self.assertRaises(NotSupportedError):
            self.mapper.map(regex)(test_func)

    def test_args_and_kwargs_map_failed(self):
        """Test that mapping with unnamed capture groups and named captured groups fails."""
        def test_func(arg1, arg2): pass
        regex = r'test (?P<kwarg1>.+) (.+)'
        with self.assertRaises(NotSupportedError):
            self.mapper.map(regex)(test_func)


class TestRetrieve(unittest.TestCase):
    """Test Cases for retrieving and calling mapped functions."""

    def setUp(self):
        """Set up."""
        self.mapper = FuncMapper()

    def test_simple_function_call(self):
        """Test a simple function call."""
        simple_test_func = MagicMock(return_value='simple_test_func called')
        self.mapper.map('test')(simple_test_func)
        return_value = self.mapper('test')
        self.assertEqual(return_value, 'simple_test_func called')
        simple_test_func.assert_called_once_with()

    def test_kwargs_function_call(self):
        """Test a function call with kwargs."""
        simple_test_func = MagicMock(return_value='kwargs_test_func called')
        self.mapper.map(r'test (?P<kwarg1>.+) (?P<kwarg2>.+)')(simple_test_func)
        return_value = self.mapper('test 1 foo')
        self.assertEqual(return_value, 'kwargs_test_func called')
        simple_test_func.assert_called_once_with(kwarg1='1', kwarg2='foo')

    def test_multiple_function_calls(self):
        """Test to register and retrive multiple functions"""
        simple_test_func1 = MagicMock(return_value='simple_test_func1 called')
        self.mapper.map('test1')(simple_test_func1)
        simple_test_func2 = MagicMock(return_value='simple_test_func2 called')
        self.mapper.map('test2')(simple_test_func2)
        return_value1 = self.mapper('test1')
        return_value2 = self.mapper('test2')
        self.assertEqual(return_value1, 'simple_test_func1 called')
        self.assertEqual(return_value2, 'simple_test_func2 called')
        simple_test_func1.assert_called_once_with()
        simple_test_func2.assert_called_once_with()

    def test_raise_no_function_exception(self):
        """Test that an exception is raised if no match is found."""
        with self.assertRaises(KeyError):
            self.mapper('test1')


