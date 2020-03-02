### compose
```python
import functools
def compose(*functions):
    return functools.reduce(lambda f, g: lambda x: f(g(x)), functions, lambda x: x)
```
### curry
```python
def curry(x, argc=None):
    if argc is None:
        argc = x.__code__.co_argcount
    def p(*a):
        if len(a) == argc:
            return x(*a)
        def q(*b):
            return x(*(a + b))
        return curry(q, argc - len(a))
    return p
```
### replace
```python
import re
replace = curry(lambda what, replacement, s: re.sub(what, replacement, s))
```
### to_lower_case
```python
to_lower_case = lambda x: x.lower()
```
