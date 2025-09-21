+++
date = '2025-09-21T16:05:20+02:00'
title = 'Decorators explained'
tags = ['programming', 'python', 'metaprogramming', 'intermediate']
+++

Programming languages provide a way of writing code about code, what is known as metaprogramming. A well known, nice and elegant metaprogramming feature in Python is the decorator. Metaprogramming is usually a tool for library authors, not application developers.

However, knowing how decorators work is worth it. It makes debugging easier, explains a lot of "magic" and shows just how powerful functions and the dynamic nature of Python are. You may never use them in your own code but decorators are a nice example of how Python works.

-----

### How decorators work

Let's assume you are writing a performance sensitive function in your application. Let's also hope that it doesn't do what the example below shows.
```python {linenos=inline}
def counter(n: int) -> int:
    """counts the elements of a list it creates! not great!"""
    l = list(range(n))
    n = 0
    for _ in l:
        n += 1
    return n

print(counter(10))  # 10
```
We already established that it is a performance sensitive part so you are curious about how it scales with larger lists. You begin timing it but soon the code seems really ugly and copy-paste-y.
```python {linenos=inline}
import time

start = time.perf_counter()
counter(10)
end = time.perf_counter()
print(end-start)

start = time.perf_counter()
counter(10000)
end = time.perf_counter()
print(end-start)

start = time.perf_counter()
counter(1000000)
end = time.perf_counter()
print(end-start)
```
You could put your code in a loop and skip the copy pasting. However, you realise that this timing code is something you could use in other projects, so maybe you want to write something more portable!

Instead of duplicating this across projects, you take advantage of the fact that functions are first-class citizens in Python and can be passed around like any other object. They can even be returned as values from functions, so you try and write the code below.
```python {linenos=inline hl_lines=[11]}
def timer(func):
    """wraps func and reports execution time"""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(end-start)
        return result
    return wrapper

counter = timer(counter)
counter(1000000)
```
This is already pretty good. Portable code and a nice programming pattern where you don't need to copy-paste timing functions all around. In fact, it's such a nice pattern that Python provides some syntactic sugar for it, in the form of `@`. Line 11 in the previous sample is equivalent to lines 1 and 2 in this one.
```python {linenos=inline hl_lines=[1,2]}
@timer
def counter(n: int) -> int:
    """counts the elements of a list it creates! not great!"""
    l = list(range(n))
    n = 0
    for _ in l:
        n += 1
    return n

counter(1000000)
```
Decorators can also be chained, there is nothing stopping you from decorating a function many times. In fact this is (usually) how web frameworks implement middleware. Even if they're not explicitly decorating, they are certainly chaining functions together by wrapping them and returning the end result.
```python {linenos=inline hl_lines=[10,11]}
def logger(func):
    """wraps func and logs information"""
    def wrapper(*args, **kwargs):
        print(f"starting execution with {args=} and {kwargs=}")
        result = func(*args, **kwargs)
        print("finished execution")
        return result
    return wrapper

@logger
@timer
def counter(n: int) -> int:
    """counts the elements of a list it creates! not great!"""
    l = list(range(n))
    n = 0
    for _ in l:
        n += 1
    return n

counter(1000000)
```
It is important to note that the last line is equivalent to `logger(timer(counter))(1000000)` and **not** `logger(timer(counter(1000000)))`. The decorator first wraps the function and returns it, so you are calling the end result of this chain which is `logger(timer(counter))`, where counter is just the function object and not called yet. Think `counter` vs `counter()`.

-----

### A minor issue and a nice solution

As you already know, objects in python have a ton of interesting and helpful attributes and metadata. Functions are another type of object, therefore they have their own set of attributes. Take this example:
```python {linenos=inline}
def add_one(n: int) -> int:
    """returns the number incremented by one"""
    return n + 1

print(add_one) # <function add_one at 0x1037bb1a0>
print(add_one.__doc__)  # returns the number incremented by one
print(add_one.__name__)  # add_one
print(add_one.__annotations__)  # {'n': <class 'int'>, 'return': <class 'int'>}
```
We see that we can access the docstring, the name of the function, its type annotations, etc... Now let's decorate it and try the same thing:
```python {linenos=inline}
@timer
def add_one(n: int) -> int:
    """returns the number incremented by one"""
    return n + 1

print(add_one)  # <function timer.<locals>.wrapper at 0x1037bb420>
print(add_one.__doc__)  # None
print(add_one.__name__)  # wrapper
print(add_one.__annotations__)  # {}

```
The result is not nice. We've lost a lot of information. It might not seem super useful but for authors of libraries, this sort of thing can be an issue because experienced users expect and utilize such attributes.

One solution is to modify the decorator function to keep these attributes and not overwrite them. This would require modifying the code and keeping track of attributes manually, not an elegant solution. If you are interested, you can attempt doing it and see how it affects your code.

The actual solution comes from the standard library. Take a look at this example:
```python {linenos=inline hl_lines=[5]}
from functools import wraps

def logger(func):
    """wraps func and logs information"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"starting execution with {args=} and {kwargs=}")
        result = func(*args, **kwargs)
        print("finished execution")
        return result
    return wrapper

@logger
def add_one(n: int) -> int:
    """returns the number incremented by one"""
    return n + 1

print(add_one)  # <function add_one at 0x1037bb420>
print(add_one.__doc__)  # returns the number incremented by one
print(add_one.__name__)  # add_one
print(add_one.__annotations__)  # {'n': <class 'int'>, 'return': <class 'int'>}
```
It is interesting how we solve the issue by decorating our decorator, but if you consider what metaprogramming is (programming with code instead of values) it makes total sense! Python handles the reference logistics behind the scenes for us and our code remains as close to the original as possible.

-----

### An interesting edge case

Just as an excuse to introduce some extra depth into the discussion, let's work with a recursive function.
```python {linenos=inline}
def factorial(n: int) -> int:
    """calculates the factorial"""
    if n < 0:
        raise ValueError("Number must be positive")

    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(10))  # 3628800
```
Assume you try to benchmark it, you will see that things get noisy very quickly!
```python {linenos=inline}
@logger
@timer
def factorial(n: int) -> int:
    """calculates the factorial"""
    if n < 0:
        raise ValueError("Number must be positive")

    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial(n-1)

print(factorial(10))
# starting execution with args=(10,) and kwargs={}
# starting execution with args=(9,) and kwargs={}
# starting execution with args=(8,) and kwargs={}
# ...
# finished execution
# 3628800
```
A whole bunch of print statements and information. Did we ask for this, or did we assume a single pair would show up? More importantly, why does this happen?

We are essentially executing `factorial = logger(timer(factorial))` so now `factorial` points to the decorated function, not the original one. Each recursive call goes through the wrapped version of the function, not the original. That’s why you see logs for every single step of recursion.

Just thinking out loud here, since the non-wrapped function gets executed it means it must be somewhere in memory and accessible, otherwise it would have been garbage collected. If you dig into the closure attribute of the function, you can find the original function object buried inside. 
```python {linenos=inline}
print(factorial)
# <function logger.<locals>.wrapper at 0x105a474c0>
# this is not what we want!

print(factorial.__closure__[0].cell_contents.__closure__[0].cell_contents)
# <function factorial at 0x105a47420>
# this is it!
```
It’s possible, but hacky, to call it directly. Beware that this approach is brittle. Even if you do, you'll see that it's not what you (might have) expected to happen:
```python {linenos=inline}
# calling the wrapped function
factorial(3)

# starting execution with args=(3,) and kwargs={}
# starting execution with args=(2,) and kwargs={}
# starting execution with args=(1,) and kwargs={}
# 9.5367431640625e-07
# finished execution
# 3.0040740966796875e-05
# finished execution
# 4.9114227294921875e-05
# finished execution
# 6


# attempting to call the original
factorial.__closure__[0].cell_contents.__closure__[0].cell_contents(3)

# starting execution with args=(2,) and kwargs={}
# starting execution with args=(1,) and kwargs={}
# 7.152557373046875e-07
# finished execution
# 3.0040740966796875e-05
# finished execution
# 6
```
You get 1 less pair of logs because the initial invocation of your function is this monstrosity. The function code, however, calls `n * factorial(n-1)` so after the first invocation, it's back to referencing the wrapped function! You would need to write the code with the closure references inside the original implementation to actually get this to work, which is not really an option. Here it is just as an example of what **not** to do.
```python {linenos=inline}
def logger(func):
    """wraps func and logs information"""
    def wrapper(*args, **kwargs):
        print(f"starting execution with {args=} and {kwargs=}")
        result = func(*args, **kwargs)
        print("finished execution")
        return result
    return wrapper

@logger
def factorial(n: int) -> int:
    """calculates the factorial"""
    if n < 0:
        raise ValueError("Number must be positive")

    if n == 1 or n == 0:
        return 1
    else:
        return n * factorial.__closure__[0].cell_contents(n-1)

factorial(5)
```
An acceptable workaround would be to keep a separate helper function that we will wrap and separate the recursive logic from the entry-point:
```python {linenos=inline}
def logger(func):
    """wraps func and logs information"""
    def wrapper(*args, **kwargs):
        print(f"starting execution with {args=} and {kwargs=}")
        result = func(*args, **kwargs)
        print("finished execution")
        return result
    return wrapper

def _factorial(n: int) -> int:
    """internal recursive helper"""
    if n < 0:
        raise ValueError("Number must be positive")
    if n == 1 or n == 0:
        return 1
    return n * _factorial(n-1)

@logger
def factorial(n: int) -> int:
    """calculates the factorial"""
    return _factorial(n)

factorial(5)
```
The end result is what we want, one set of logging statements. We had to keep a separate reference to the original function but this is a consequence of how variables and scope works in python.
-----

### Wrapping up
As already mentioned, metaprogramming is a niche topic and you can have a lengthy career without having to actively use it much. Make no mistake, you are probably using it every day as an end user but I have rarely, if ever, had to make my own decorator so far.

However, the focus of this post (and this blog) is not about teaching and learning how to do things, but rather about how things are done. It pays dividends to know the underlying mechanisms, what is possible and the extent of the tools and possibilities provided by a language.

You will probably (and hopefully) never need to use `.__closure__[0].cell_contents.__closure__[0].cell_contents(3)` but this works as an interesting example of how functions are objects, have attributes, can hold data and metadata and so much more.
