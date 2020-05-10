import re
import functools

# id :: a -> a
id = lambda x: x


class Nothing:
    pass

def compose(*functions):
    return functools.reduce(lambda f, g: lambda *x: f(g(*x)), functions, lambda x: x)

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

replace = curry(lambda what, replacement, s: re.sub(what, replacement, s))
to_lower_case = lambda x: x.lower()
head = curry(lambda xs: xs[0])
add = curry(lambda x,y: x+y)


class Container:
  def __init__(self, value):
    self.value = value

  def __repr__(self):
    return f'Container({self.value.__repr__()})'

  def map(self, f):
    return Container(f(self.value))

  def join(self):
    return self.value
    
  # chain :: Monad m => (a -> m b) -> m a -> m b
  def chain(self, fn):
    return self.map(fn).join()

  def ap(self, other):
    return other.map(self.value)


class Maybe:
  def __init__(self, value):
    self.value = value
    
  def __repr__(self):
    return f'Maybe({self.value.__repr__()})'
    
  def is_nothing(self):
    return isinstance(self.value, Nothing)
    
  def map(self, f):
    if self.is_nothing():
        return self
    return Maybe(f(self.value))

  def join(self):
    return Maybe(Nothing()) if self.is_nothing() else self.value
    
  # chain :: Monad m => (a -> m b) -> m a -> m b
  def chain(self, fn):
    return self.map(fn).join()

# capitalize :: String -> String
capitalize = lambda s: to_upper_case(head(s)) + to_lower_case(tail(s))

# str_length :: String -> Number
str_length = lambda s:  len(s)

# join :: String -> [String] -> String
join = curry(lambda what, xs:  what.join(xs))

# findall :: Regex -> String -> [String]
findall = curry(lambda reg, s: re.findall(reg, s))

# replace :: Regex -> String -> String -> String
replace = curry(lambda reg, sub, s: s.replace(reg, sub))

# Analogous to built-in map function
fmap = curry(lambda f, xs: [f(x) for x in xs])

# map :: Functor f => (a -> b) -> f a -> f b
map = curry(lambda f, any_functor: any_functor.map(f))

# prop :: Dictionary -> a -> b
prop = curry(lambda k,d: d[k])

class Either:

    def __new__(cls, *args, **kwargs):
        return Right.__new__(Right, *args, **kwargs)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.__class__.__name__}({self.value.__repr__()})'


class Left(Either):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def map(self, f):
        return self


class Right(Either):

    def __new__(cls, *args, **kwargs):
        return object.__new__(cls)

    def map(self, f):
        return Right(f(self.value))

@curry
def either(f, g, e):
    if isinstance(e, Left):
        return f(e.value)
    if isinstance(e, Right):
        return g(e.value)

#############################
class IO:
  def __init__(self, fn):
    self.unsafe_perform_IO = fn

  def map(self, fn):
    return IO(compose(fn, self.unsafe_perform_IO))

  def __repr__(self):
    return f'IO({self.unsafe_perform_IO.__repr__()})'

  def join(self):
    return self.unsafe_peform_IO()

#####################################
append = curry(lambda s0, s1: s1+s0)
Task = Maybe

class Compose:
  def __init__(self, fgx):
    self.get_compose = fgx
  def map(self, fn):
    return Compose(map(map(fn), self.get_compose))
  def __repr__(self):
    return f'Compose({self.get_compose.__repr__()})'


# chain :: Monad m => (a -> m b) -> m a -> m b
chain = lambda f: compose(join, map(f))
