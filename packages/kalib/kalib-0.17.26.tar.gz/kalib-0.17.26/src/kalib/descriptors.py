"""This module provides advanced property descriptors for Python classes,
allowing the creation of instance, class, and mixed properties with optional
caching capabilities. It includes decorators and base classes to facilitate the
definition of properties that can behave differently depending on whether they
are accessed through an instance or a class. The module supports both
synchronous and asynchronous functions.

**Key Components:**

- **Decorator `cache(limit=None)`**: A decorator that applies `functools.lru_cache`
  to a function, enabling result caching with an optional size limit.

- **Function `call_descriptor(descriptor)`**: Retrieves the underlying callable
  from a descriptor. It handles custom descriptors derived from `BaseProperty`
  and standard descriptors, ensuring compatibility with different property types.

- **Decorator `parent_call(func)`**: A decorator for methods within descriptor
  classes to facilitate calling the parent implementation of a property method.
  It is useful when overriding property methods and needing to access the
  superclass's implementation.

- **Exceptions**:
  - **`InvalidContextError`**: Raised when a property is accessed in an invalid
    context, such as accessing an instance-only property from a class.

- **Alias `prop(Property)`**: Provides predefined property descriptors:

  - `cls`: A descriptor for class-level properties. It ensures the property is
    accessed through the class and not an instance, allowing for properties that
    pertain to the class as a whole.

  - `any`: Combines `MixedProperty` and `Property` to provide a property accessible
    through both the class and the instance.

- **Alias `pin(Cached)`**: Provides cached property descriptors:

  - `bind`: Simple replace calculated value instead self data-descriptor.

  - `cls`: Combines `ClassProperty` and `Cached` to provide a cached class-level
    property. It caches the result at the class level, avoiding redundant computations.

  - `root`: Same as cls, but binds to the class where decorator used instead of
    child class where call registered.

  - `any`: Combines `MixedProperty` and `Cached` to provide a cached property accessible
    through both the class and the instance. It intelligently caches the result
    based on the access context.
"""

from asyncio import ensure_future, iscoroutinefunction
from dataclasses import is_dataclass
from functools import cached_property, lru_cache, partial, wraps
from inspect import iscoroutine, isfunction, ismethod

from kalib.internals import (
    Nothing,
    Who,
    class_of,
    get_attr,
    get_owner,
    is_class,
    issubstance,
)

__all__ = 'cache', 'pin', 'prop'



try:
    from pydantic.main import BaseModel as PydanticModel

except ImportError:
    PydanticModel = None


def cache(limit=None):

    function = partial(lru_cache, maxsize=None, typed=False)
    if isfunction(limit) or iscoroutine(limit) or ismethod(limit):
        return function()(limit)

    if limit is not None and (not isinstance(limit, float | int) or limit <= 0):
        msg = f'limit must be None or positive integer, not {Who.Is(limit)}'
        raise TypeError(msg)

    return function(maxsize=limit) if limit else function()


def call_descriptor(descriptor):
    if issubstance(descriptor, BaseProperty):
        return descriptor.call

    func = getattr(descriptor, 'fget', Nothing)
    if func is Nothing:
        head = f'expected descriptor derived from {Who(BaseProperty)}'

        if class_of(descriptor) is not cached_property:
            raise TypeError(f'{head}, but got {Who(descriptor)} instead')

        raise TypeError(
            f'{head}, but got {Who(descriptor)}, '
            f'may be you use primitive @pin.bind instead full-featured @pin?')

    return func


def parent_call(func):

    @wraps(func)
    def parent_caller(node, *args, **kw):
        try:
            desc = get_attr(
                class_of(node), func.__name__, exclude_self=True,
                index=bool(func.__name__ not in class_of(node).__dict__))
            return func(node, call_descriptor(desc)(node, *args, **kw), *args, **kw)

        except RecursionError as e:
            raise RecursionError(
                f'{Who(node)}.{func.__name__} call real {Who(func)}, '
                f"couldn't reach parent descriptor; "
                f"maybe {Who(func)} it's mixin of {Who(node)}?") from e

    return parent_caller


class PropertyError(Exception):
    ...


class InvalidContextError(PropertyError):
    ...


def wrapped_instance_checker(func):

    @wraps(func)
    def type_checker(self, node, *args, **kw):
        if (
            self.klass is not None and
            (node is None or self.klass != is_class(node))
        ):
            msg = (
                f'{Who(func)} exception, '
                f'{self.header_with_context(node)}, {node=}')

            if node is None and not self.klass:
                msg = f'{msg}; looks like as non-instance invokation'
            raise InvalidContextError(msg)

        return func(self, node, *args, **kw)
    return type_checker


class BaseProperty:

    klass = False
    readonly = False

    def __init__(self, function):
        self.function = function

    @cached_property
    def name(self):
        return self.function.__name__

    @cached_property
    def is_data(self):
        return bool(hasattr(self, '__set__') or hasattr(self, '__delete__'))

    @cached_property
    def title(self):
        mode = 'kalib' if self.klass is None else ('instance', 'class')[self.klass]
        prefix = ('', 'data ')[self.is_data]
        return (
            f'{mode} {prefix}descriptor '
            f'{Who(self, addr=True)}'.strip())

    @cached_property
    def header(self):
        try:
            return f'{self.title}({self.function!a})'
        except Exception:  # noqa: BLE001
            return f'{self.title}({Who(self.function)})'

    def header_with_context(self, node):
        if node is None:
            mode = 'kalib' if self.klass is None else 'undefined'
        else:
            mode = ('instance', 'class')[is_class(node)]
        return f'{self.header} with {mode} ({Who(node, addr=True)}) call'


    @wrapped_instance_checker
    def get_node(self, node):
        return node

    @wrapped_instance_checker
    def call(self, node):
        value = self.function(node)
        if iscoroutinefunction(self.function):
            value = ensure_future(value)
        return value


    def __get__(self, instance, klass):
        if instance is None and self.klass is False:
            msg = f'{self.header_with_context(klass)}'
            raise InvalidContextError(msg)
        return self.call((instance, klass)[self.klass])

    def __str__(self):
        return f'<{self.header}>'

    def __repr__(self):
        return f'<{self.title}>'


class Cached(BaseProperty):

    def is_dicted_class(self, node):
        if is_dataclass(node) or isinstance(self, Child):
            return True

        if PydanticModel is not None:
            return issubclass(class_of(node), PydanticModel)

        return False

    @wrapped_instance_checker
    def get_cache(self, node):
        name = f'__{("instance", "class")[is_class(node)]}_memoized__'
        try:
            return node.__dict__[name]

        except KeyError:
            cell = {}
            setattr(node, name, cell)
            return cell

    @wrapped_instance_checker
    def call(self, obj):
        node = self.get_node(obj)

        if self.is_dicted_class(node):
            try:
                return self.get_cache(node)[self.name]
            except KeyError:
                ...

        return self.save(node, super().call(obj))

    @wrapped_instance_checker
    def save(self, node, value):

        if self.is_dicted_class(node):
            self.get_cache(node)[self.name] = value

        else:
            setattr(node, self.name, value)

        return value


class ClassProperty(BaseProperty):
    klass = True

    @wrapped_instance_checker
    def get_node(self, node):
        return get_owner(node, self.name) if is_class(node) else node


class MixedProperty(ClassProperty):
    klass = None
    def __get__(self, instance, klass):
        return self.call(instance or klass)


class ClassPin(ClassProperty, Cached):
    ...


class MixedPin(MixedProperty, Cached):
    ...


class Child(BaseProperty):

    @wrapped_instance_checker
    def get_node(self, node):
        return node

    @classmethod
    def wrap(cls, klass):
        name = Who(klass, full=False)
        return type(
            f'{name}_child' if name == name.lower() else f'{name}Child',
            (cls, klass), {})


class_pin = Child.wrap(ClassPin)


class BaseMixin:
    @class_pin
    def base(cls):
        return cls


class Pin(Cached, BaseMixin):

    bind = cached_property
    root = ClassPin
    cls = class_pin

    any = Child.wrap(MixedPin)
    any.cls = any
    any.root = MixedPin


class Property(BaseProperty, BaseMixin):

    cls = ClassProperty
    any = MixedProperty

pin, prop = Pin, Property
