"""**Integration**:

- The module relies on custom utilities from the `kalib` package, such as:
  - `kalib.datastructures` for JSON handling.
  - `kalib.descriptors` for caching and property management.
  - `kalib.importer` for dynamic imports.
  - `kalib.internals` for introspection utilities.
  - `kalib.logging` for logging capabilities.
  - `kalib.misc` and `kalib.text` for miscellaneous utilities.

- It integrates with standard Python modules like `dataclasses`, `enum`,
`typing`, and `datetime` to provide enhanced functionality while maintaining
compatibility with standard data class features.
"""

from kalib import (
    cvs,
    dataclasses,
    datastructures,
    descriptors,
    importer,
    internals,
    logging,
    misc,
    monkey,
    text,
)
from kalib._internal import to_ascii, to_bytes
from kalib.cvs import (
    Git,
)
from kalib.dataclasses import (
    autoclass,
    dataclass,
)
from kalib.datastructures import (
    dumps,
    json,
    loads,
    pack,
    serializer,
    unpack,
)
from kalib.descriptors import (
    cache,
    pin,
    prop,
)
from kalib.exceptions import (
    exception,
)
from kalib.http import (
    HTTP,
    Cookies,
)
from kalib.importer import (
    optional,
    required,
    sort,
)
from kalib.internals import (
    Nothing,
    Who,
    about,
    class_of,
    is_class,
    issubstance,
    sourcefile,
    stacktrace,
    unique,
)
from kalib.logging import (
    Logging,
    logger,
)
from kalib.misc import (
    Now,
    Partial,
    Timer,
    lazy_proxy_to,
    stamp,
    tty,
)
from kalib.monkey import (
    Monkey,
)
from kalib.text import (
    Str,
)

__all__ = (
    'Cookies',
    'Git',
    'HTTP',
    'Logging',
    'Monkey',
    'Nothing',
    'Now',
    'Partial',
    'Str',
    'Time',
    'Who',
    'about',
    'autoclass',
    'cache',
    'class_of',
    'cvs',
    'dataclass',
    'dataclasses',
    'datastructures',
    'descriptors',
    'dumps',
    'exception',
    'importer',
    'internals',
    'is_class',
    'issubstance',
    'json',
    'lazy_proxy_to',
    'loads',
    'logger',
    'logging',
    'misc',
    'monkey',
    'optional',
    'pack',
    'pin',
    'prop',
    'required',
    'serializer',
    'sort',
    'sourcefile',
    'stacktrace',
    'stamp',
    'text',
    'to_ascii',
    'to_bytes',
    'tty',
    'unique',
    'unpack',
)

Time = Timer()
__version__ = Git.version
