# Cache Toolz

[![License GPLv3+](https://img.shields.io/pypi/l/cachetoolz?label=License&color=%234B78E6)](https://codeberg.org/taconi/cachetoolz/src/branch/main/LICENSE)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/cachetoolz.svg?logo=python&label=Python&color=%234B78E6)](https://pypi.python.org/pypi/cachetoolz/)
[![PyPI version](https://img.shields.io/pypi/v/cachetoolz.svg?logo=pypi&label=PyPI&color=%23FA9BFA)](https://pypi.org/project/cachetoolz/)
[![Downloads](https://img.shields.io/pypi/dm/cachetoolz?logo=pypi&label=Downloads&color=%2373DC8C)](https://pypi.org/project/cachetoolz/)
[![Documentation](https://img.shields.io/badge/Documentation-1769AA?color=%234B78E6)](https://cachetoolz.readthedocs.io)
[![Changelog](https://img.shields.io/badge/Changelog-1769AA?color=%2373DC8C)](https://cachetoolz.readthedocs.io/changelog)
[![Issue Tracker](https://img.shields.io/badge/Issue%20Tracker-1769AA?color=%23FA9BFA)]("https://codeberg.org/taconi/cachetoolz/issues")
[![Contributing](https://img.shields.io/badge/Contributing-1769AA?color=%234B78E6)](https://cachetoolz.readthedocs.io/contributing)
[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)

This library offers a decorator that enhances the functionality of caching functions.

Caching is a technique commonly used in software development to improve performance by storing the results of expensive or time-consuming function calls. With this library, you can easily apply caching to your functions using a decorator.

The decorator provided by this library automatically checks if the function has been called with the same set of arguments before. If it has, instead of executing the function again, it returns the cached result, saving valuable processing time. However, if the function is called with new or different arguments, it will execute normally and cache the result for future use.

By incorporating this caching decorator into your code, you can optimize the execution of functions that involve complex computations, database queries, API calls, or any other operations that could benefit from caching.

Overall, this library simplifies the implementation of caching in your applications, allowing you to enhance performance and reduce resource consumption effectively.

# Installation

Install and update using [pip](https://pip.pypa.io/en/stable/getting-started/):

```{.sh linenums=0}
pip install cachetoolz
```

# A Example

```python title="todo.py" hl_lines="16-17 25-26 30-31 35-36"
from dataclasses import asdict, dataclass, field
from datetime import timedelta
from uuid import UUID, uuid4

from cachetoolz import cache
from cachetoolz.coder import coder

TODOS: list['Todo'] = []

@dataclass
class Todo:
    title: str
    status: bool = field(default=False, compare=False)
    id: UUID = field(default_factory=uuid4, compare=False)

# Registering an object coder
@coder.register
class TodoSerializer:
    def encode(self, value: Todo):  # Need type annotated
        return asdict(value)

    def decode(self, value):
        return Todo(**value)

# Adding cache to function with expiry time in seconds
@cache(ttl=120, namespace='todo')
def get_one(id: UUID):
    return next(filter(lambda todo: todo.id == id, TODOS), None)

# Adding expiry time using timedelta
@cache(ttl=timedelta(minutes=30), namespace='todo')
def get_all():
    return TODOS

# Clear all caches on given namesoaces
@cache.clear(namespaces=['todo'])
def add_one(title, status=False):
    if (todo := Todo(title=title, status=status)) not in TODOS:
        TODOS.append(todo)
```
