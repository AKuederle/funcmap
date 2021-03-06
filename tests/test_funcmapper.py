# -*- coding: utf-8 -*-
"""Base Tests for the FuncMapper Class"""
import unittest

import re

try:
    from mock import MagicMock
except ImportError:
    from unittest.mock import MagicMock

from funcmap import FuncMapper
from funcmap.mapper import NotSupportedError


class BaseMappingTest:
    def _mapper_func(self, regex, func):
        NotImplementedError('Implement in Child class')

    def test_simple_map(self):
        """Test that simple mapping of a function works."""

        def test_func(): pass

        self._mapper_func('test', test_func)
        self.assertEqual(self.mapper._mapped_functions['test'], test_func)
        self.assertEqual(self.mapper._mapped_regex['test'], re.compile('test'))

    def test_kwargs_map(self):
        """Test that mapping with kwargs works."""

        def test_func(kwarg1, kwarg2): pass

        regex = r'test (?P<kwarg1>.+) (?P<kwarg2>.+)'
        self._mapper_func(regex, test_func)
        self.assertEqual(self.mapper._mapped_functions[regex], test_func)
        self.assertEqual(self.mapper._mapped_regex[regex], re.compile(regex))

    def test_args_map_failed(self):
        """Test that mapping with unnamed capture groups fails."""

        def test_func(arg1, arg2): pass

        regex = r'test (.+) (.+)'
        with self.assertRaises(NotSupportedError):
            self._mapper_func(regex, test_func)

    def test_args_and_kwargs_map_failed(self):
        """Test that mapping with unnamed capture groups and named captured groups fails."""

        def test_func(arg1, arg2): pass

        regex = r'test (?P<kwarg1>.+) (.+)'
        with self.assertRaises(NotSupportedError):
            self._mapper_func(regex, test_func)


class TestFunctionalMapping(unittest.TestCase, BaseMappingTest):
    """All tests for mapping a function using the functional syntax."""

    def _mapper_func(self, regex, func):
        self.mapper.map(regex, func)

    def setUp(self):
        """Set up."""
        self.mapper = FuncMapper()


class TestDecoratorMapping(unittest.TestCase, BaseMappingTest):
    """All tests for mapping a function using the decorator syntax."""

    def _mapper_func(self, regex, func):
        self.mapper.map(regex)(func)

    def setUp(self):
        """Set up."""
        self.mapper = FuncMapper()


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


class TestAdditionalArguments(unittest.TestCase):
    """Test to call the functions with additional arguments"""

    def setUp(self):
        """Set up."""
        self.mapper = FuncMapper()

    def test_additional_args_no_string_kwargs(self):
        simple_test_func = MagicMock(return_value='simple_test_func1 called')
        args = ['test_arg_1', 'test_arg_2']
        kwargs = dict(test_kwarg_1='test_kwarg_1', test_kwarg_2='test_kwarg_2')
        self.mapper.map('test')(simple_test_func)
        self.mapper('test', *args, **kwargs)
        simple_test_func.assert_called_once_with(*args, **kwargs)

    def test_additional_args_with_string_kwargs(self):
        simple_test_func = MagicMock(return_value='simple_test_func1 called')
        args = ['test_arg_1', 'test_arg_2']
        kwargs = dict(test_kwarg_1='test_kwarg_1', test_kwarg_2='test_kwarg_2')
        self.mapper.map(r'test (?P<string_kwarg_1>.+) (?P<string_kwarg_2>.+)')(simple_test_func)
        self.mapper('test string_kwarg_1 string_kwarg_2', *args, **kwargs)
        simple_test_func.assert_called_once_with(*args, string_kwarg_1='string_kwarg_1',
                                                 string_kwarg_2='string_kwarg_2', **kwargs)

    def test_additional_kwargs_overwrite_string_kwargs(self):
        simple_test_func = MagicMock(return_value='simple_test_func1 called')
        args = ['test_arg_1', 'test_arg_2']
        kwargs = dict(test_kwarg_1='test_kwarg_1', overwrite_kwarg='test_kwarg_2')
        self.mapper.map(r'test (?P<string_kwarg_1>.+) (?P<overwrite_kwarg>.+)')(simple_test_func)
        self.mapper('test string_kwarg_1 string_kwarg_2', *args, **kwargs)
        simple_test_func.assert_called_once_with(*args, string_kwarg_1='string_kwarg_1', **kwargs)
