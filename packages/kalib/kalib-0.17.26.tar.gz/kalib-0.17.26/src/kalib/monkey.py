"""This module defines the `Monkey` class, providing utilities for dynamic
modification of modules and classes—commonly known as monkey patching. The
functionalities include:

- **Exception Suppression with `expect`**: A class method decorator factory
  that creates decorators to suppress specified exceptions within class methods.
  This allows methods to fail silently without interrupting program flow.

- **Attribute Patching with `patch`**: A class method to replace or override
  attributes (functions, methods, variables) in modules or classes with new
  implementations. It maintains a mapping of original attributes for reference
  or restoration, facilitating safe and trackable modifications.

- **Dynamic Binding with `bind`**: A class method to bind new methods or functions
  to existing classes or modules at runtime. It supports optional renaming and
  decorating (e.g., making a method a `classmethod`), enabling flexible extension
  of existing code structures.

- **Function Wrapping with `wrap`**: A class method that wraps existing functions
  or methods with additional functionality. It replaces the original function with
  a wrapper that can modify inputs, outputs, or side effects, using the `patch`
  method for seamless integration.

The `Monkey` class leverages the `Logging.Mixin` for detailed logging of operations,
aiding in debugging and ensuring transparency of modifications. It utilizes utilities
from the `kalib` library for importing and introspection.

Overall, the `Monkey` class serves as a powerful tool for developers needing to
modify or extend the behavior of existing codebases without altering the original
source code.
"""

from contextlib import suppress
from functools import wraps
from typing import ClassVar

from kalib.importer import required
from kalib.internals import Who, is_module
from kalib.logging import Logging


class Monkey(Logging.Mixin):

    mapping: ClassVar[dict] = {}

    @classmethod
    def expect(cls, *exceptions):
        def make_wrapper(func):
            @wraps(func)
            def wrapper(klass, *args, **kw):
                with suppress(exceptions):
                    return func(klass, *args, **kw)
            return classmethod(wrapper)
        return make_wrapper

    @classmethod
    def patch(cls, module, new):

        if isinstance(module, tuple):
            node, name = module

        elif is_module(module):
            node, name = module, new.__name__

        else:
            path, name = module.rsplit('.', 1)
            try:
                node = required(path)
            except ImportError:
                cls.log.error(f'{module=} import error')  # noqa: TRY400
                raise

        if getattr(node, name, None) is new:
            return new

        old = required(node, name) if Who(node, full=False) != name else node

        setattr(node, name, new)
        new = getattr(node, name)
        if old is new:
            raise RuntimeError

        cls.mapping[new] = old
        cls.log.debug(f'{Who(old, addr=True)} -> {Who(new, addr=True)}')
        return new

    @classmethod
    def bind(cls, node, name=None, decorator=None):
        node = required(node) if isinstance(node, str) else node

        def bind(func):
            @wraps(func)
            def wrapper(*args, **kw):
                if decorator is classmethod:
                    return func(node, *args, **kw)
                return func(*args, **kw)

            local = name or func.__name__
            setattr(node, local, wrapper)
            cls.log.verbose(f'{Who(node)}.{local} <- {Who(func, addr=True)}')
            return wrapper

        return bind

    @classmethod
    def wrap(cls, node, name=None, decorator=None):
        node = required(node) if isinstance(node, str) else node

        def wrap(func):

            wrapped_name = name or func.__name__
            if Who(node, full=False) != wrapped_name:
                wrapped_func = required(node, wrapped_name)
            else:
                wrapped_func = node

            @wraps(func)
            def wrapper(*args, **kw):
                return func(wrapped_func, *args, **kw)

            cls.log.verbose(
                f'{Who(node)}.{wrapped_name} <- '
                f'{Who(func, addr=True)}')

            wrapped = decorator(wrapper) if decorator else wrapper
            cls.patch((node, wrapped_name), wrapped)
            return wrapper

        return wrap
