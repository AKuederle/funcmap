import re
import traceback

# Define some custom errors


class NotSupportedError(Exception):
    """Error indicating, that a certion functionality is not supported by the software."""
    pass


class FuncMapper:
    def __init__(self):
        self._mapped_functions = {}
        self._mapped_regex = {}

    def __call__(self, *args, **kwargs):
        return self.call_function_with_string(*args, **kwargs)

    def map(self, regex):
        """Decorate a function to map it to a regex expression.

        Decorator that allows to map a Python function to a regex expression provided as argument. The regex expression
        is parsed using the 're' module (https://docs.python.org/3/library/re.html). Therefore, all regex syntax that
        this module supports is also supported by this regex matcher. To encapsulate arguments for the function in the
        regex expression use named capture groups (see examples).

        Inspired by the URL mapping of the Flask microframework (http://flask.pocoo.org/)

        Args:
            regex: An Python raw string (r'I am a raw string') that can be interpreted as regular expression

        Returns:
            func: The input function without modfication

        Example:
            The simplest case just maps a function to a name:

                >>> mapper = FuncMapper()
                >>> @mapper.map(r'a name')
                ... def my_func():
                ...    return 'I, my_func, have been called'
                >>> mapper('a name')
                'I, my_func, have been called'

            But you can also use variables by adding regex capture groups:
            (Note: Only named match groups are supported!)

                >>> mapper = FuncMapper()
                >>> @mapper.map(r'(?P<first>\d+)\+(?P<second>\d+)')
                ... def adder(first, second):
                ...    return '{} + {} = {}'.format(first, second, int(first) + int(second))
                >>> mapper('3+5')
                '3 + 5 = 8'
        """

        def wrapper(f):
            self._mapped_functions[regex] = f
            compiled_regex = re.compile(regex)
            if compiled_regex.groups > 0 and len(compiled_regex.groupindex) < compiled_regex.groups:
                raise NotSupportedError("Only named matched groups are Supported!")
            self._mapped_regex[regex] = compiled_regex
            return f

        return wrapper

    def _get_func_from_string(self, string):
        """Return the function matched to a regex.

        Args:
            string (str): The string to regex-expressions are matched against

        Returns:
            func: The function mapped to the respective regex
            dict: The dictionary of named capture groups of the regex
        """
        for name, regex in self._mapped_regex.items():
            match = regex.fullmatch(string)
            if match:
                return self._mapped_functions[name], match.groupdict()
        return None, None

    def call_function_with_string(self, string):
        """Call a mapped function based on an input string that is parsed by regex.

        The first function mapped to the first regex that matches the string is returned. Because dictionaries are used
        to store the regex-expressions, the output is not deterministic, if multiple regex match the string! Please
        ensure, that your regex expressions are unique. (This might change in the future)

        TODO: Handel multiple regex matching

        Args:
            string: input

        Returns:
            The return value of the called function
        """
        f, kwargs = self._get_func_from_string(string)
        if not f:
            raise KeyError("This string maps to no function!")
        return f(**kwargs)

    def start_input_loop(self, message=True, catch_exceptions=False):
        """Start a simple infinite input loop, which can be used to test the mappings.

        Note: There is a little bug, that if an exception occures with catch_exception=True, the new input line is
        sometimes not shown correctly. Press Enter after an error, if the new '>>>' is not showing.

        Args:
            message: If True a little startup message is printed
            catch_exceptions: If True all exceptions will be printed out, but will not stop the execution
        """
        # TODO: Add function logging
        if message:
            print('Infinite Input loop started!')
        while True:
            string = input('>>> ')
            try:
                if string:
                    print(self.call_function_with_string(string))
            except Exception as e:
                if catch_exceptions is True:
                    traceback.print_exc()
                    continue
                else:
                    raise e
