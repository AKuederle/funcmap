funcmap
=======

.. image:: https://img.shields.io/pypi/v/funcmap.svg
    :target: https://pypi.python.org/pypi/funcmap
    :alt: Latest PyPI version

.. image:: https://img.shields.io/travis/AKuederle/funcmap.png
   :target: 'https://travis-ci.org/AKuederle/funcmap'
   :alt: Latest Travis CI build status

A small Python module to provide convenient mapping between Python functions and text input.

Usage
-----
You know Flask_, right? You love the decorator-routing they use, right? - This is exactly the same, but for any text and
not URLs and with REGEX!

.. _Flask: http://flask.pocoo.org/

**Here is how you use it:**

First you need to create an instance of the FuncMapper:

.. code-block:: python

    from funcmap import FuncMapper

    mapper = FuncMapper()

And now you map, map, map:

.. code-block:: python

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

Not enough mapping? - Than map some more! Double-Map-Time!

.. code-block:: python

    @mapper.map(r'I am Fred')
    @mapper.map(r'No, I am Joe')
    def multi_name():
        """We can map multiple Regex-expressions to the same function."""
        return 'I have multiple names!'

And no we have a function with some self esteem:

.. code-block:: python

    >>> print(mapper('call my_func'))
    'I, my_func, have been called'

A silly calculator:

.. code-block:: python

    >>> print(mapper('3+5'))
    '3 + 5 = 8'
    >>> print(mapper('10+2'))
    '10 + 2 = 12'

And this schizophrenic guy:

.. code-block:: python

    >>> print('I am Fred')
    'I have multiple names!'
    >>> print('No, I am Joe')
    'I have multiple names!'

For more guidance check the examples folder and the method docstrings.

Why the heck do I need that?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Because it uses some awesome Python stuff, of course! - But seriously, the idea is to use it as tiny helper-framework
when some simple language logic is needed. A prime example would be something like a chatbot or some kind of AI-Assistant.

I developed this little thing, because I am planning on building like a very dumb language-shortcut engine to make some
simple tasks voice or SMS/Message controllable. I currently don't have time for that, but I wanted to start somewhere.
If you have the time, STEAL MY IDEA, MAKE IT, SHARE IT, AND BE AWESOME!

Can it do ...?
^^^^^^^^^^^^^^
Probably not... yet! Currently I only implemented the bare minimum I needed. If I will do more work with this library I
will very likely find more stuff I need. Till then, it is your turn! If you are missing a feature let me know! I will
try my best to make it work for you!

What is this RegEx you are talking about?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Regular Expressions (RegEx) are super cool language-processing-magic, if one understands them. I do... sometimes. If you want to
master the RegEx `learn here <https://regexone.com/references/python>`_ and `test your skills here <https://regex101.com/>`_.


Installation
------------

.. code-block:: bash

    pip install funcmap

or if you want to develop an awesome new feature (yes, I know you want to!):

.. code-block:: bash

    git clone https://github.com/AKuederle/funcmap.git
    cd funcmap
    pip install -e .


What do I need?! (Requirements)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Na Na Na Nothing

But, does it work?! (Tests)
^^^^^^^^^^^^^^^^^^^^^^^^^^^
YES! I hope. If in doubt, run

.. code-block:: bash

    python setup.py test

Compatibility
-------------

The module is compatible with Python 3 only. It uses `re.fullmatch`, which is not backwards compatible. If you really
need a version that is compatible with Python 2.7, let me know. I guess it should be possible to fix that.

Licence
-------
This package is licenced under a MIT licence (Copyright (c) 2017 Arne Küderle)

Authors
-------

`funcmap` was written by `Arne Küderle <a.kuederle@gmail.com>`_.
