+++
date = '2025-08-12T22:31:19+02:00'
title = 'Labels, not boxes'
tags = ['programming', 'python', 'basics']
+++
One of my favourite topics is how variables work in Python. Python's variables don't store data directly, instead they act as references to objects in memory. Python doesn’t have pointers, but in reality, I’d argue it just hides them in plain sight!

> Disclaimer: This post is inspired by material from the excellent book by Luciano Ramalho, Fluent Python

### Variables as Labels 🏷️

Think of a variable as a **label** that you can attach to an object. When you write `x = 10`, you're not putting the number `10` into a box called `x`. Instead, you're creating an object in memory with the value `10` and then attaching the label `x` to it.

There’s nothing stopping you from attaching multiple labels to the same object. Doing so does not multiply the number of objects. It's still the same object, it just has multiple labels attached to it.

```python
# The variable 'a' is a reference to integer value 10
a = 10
print(f"The ID of the object that variable 'a' references is: {id(a)}")

# The variable 'b' is also a reference to the same integer object 10
b = a
print(f"The ID of the object that variable 'b' references is: {id(b)}")

# 'a' and 'b' point to the same object in memory
print(f"Is a the same object as b? {a is b}")
```

In the example above, `a` and `b` both reference the same object with the value `10`. The `id()` function returns the unique identifier of an object, specifically its memory address, proving the labels point to the same object.

-----

### Reassigning Variables

When you reassign a variable, you're not changing the original object. You're simply detaching the label from the old object and attaching it to a new one.

```python
a = 10
print(f"ID before reassigning: {id(a)}")

a = "another object"
print(f"ID after reassigning: {id(a)}")

# The ID has changed, because 'a' now points to a string object in a different memory address.
```

Why is this interesting or useful? So far it's really not, it's just an implementation detail. However, in combination with another aspect of Python it can have significant impact on the code you write, either in the form of bugs or performance. That aspect is object mutability.

-----

### Mutable vs. Immutable Objects 🗂️

The distinction between **mutable** and **immutable** objects is crucial here.

  * **Immutable objects** (like strings, integers, and tuples) cannot be changed after they are created. When you "modify" them, you are actually creating a new object and **reassigning** the variable.
  * **Mutable objects** (like lists, dictionaries, and sets) can be changed in place without creating a new object.

Let's see this with a list:

```python
list1 = [1, 2, 3]
list2 = list1  # list2 now references the *same* list object as list1

print(f"ID of list1: {id(list1)}")
print(f"ID of list2: {id(list2)}")

# Now, we modify the list through list1
list1.append(4)

print(f"list1: {list1}")
print(f"list2: {list2}") # list2 shows the change because they reference the same object

print(f"ID of list1 after modification: {id(list1)}")
print(f"ID of list2 after modification: {id(list2)}")

# The IDs are the same because the object was modified in place.
```

This behavior is why you have to be careful when working with mutable objects. Assigning a new variable doesn’t create a copy—it just adds another label to the same object. This is a good thing because it allows one to be efficient with memory. Imagine working with a very large list: referencing allows you to simply pass around the reference to the object instead of copying it all the time!

It is also something you need to be careful about because sharing data between functions can unintentionally modify them.

-----

### Passing by (object) reference ⬅️

Some languages have a split behaviour when passing arguments to functions: they do passing-by-value for certain types and passing-by-reference for other types. When passing-by-value, the function gets a copy of the data which it can modify or delete and it leaves the original value intact. When passing-by-reference, functions get a reference to the data which means they can access the original object. Modifying it changes the original object everywhere it’s referenced.

In Python, sometimes you can modify the value and other times you cannot. So does it follow the same split behaviour? Nope! Python mimics this split behavior with the combination of mutable/immutable types and always passing-by-reference.

Let's see a couple of examples that will make the above concrete. Below is a function that receives a dictionary, pops the last key-value pair inserted, then returns `None`.

```python
# this will modify the dictionary
def modify(d: dict) -> None:
    if d:
        d.popitem()
    return

obj = {"name": "john", "surname": "doe"}

modify(obj)

print(f"obj: {obj}")  # should print obj: {"name": "john"}
```
This function modifies the dictionary because a dictionary is mutable. When passed as an argument, the function gets a label to the underlying object as a variable so any action is happening against the underlying object. This makes the modification persistent.


Below is a similar function that receives an integer, increments it by one, then returns `None`.
```python
# this will modify the dictionary
def modify(d: int) -> None:
    d += 1
    return

obj = 1

modify(obj)

print(f"obj: {obj}")  # should print "obj: 1"
```
This function fails to modify the passed integer because an integer is immutable. The function again gets a label to the underlying object as a variable but when it tries to increment it, Python creates a new integer object with the value `d + 1` and assigns the label `d` to it. The original object still remains intact with the original `obj` variable still pointing to it.

-----

### Sometimes copying is good 🖨️

This doesn’t mean you can never modify immutable values or share mutable ones. Well... actually... it means **exactly** that, but at the same time there is a very simple solution to the problem and we're already almost at the end! The first part of the solution is understanding how variables and mutability work. The second, is working around the situation.

The example below shows that Python provides easy ways to create copies of mutable objects. This way, you take on the performance overhead of duplicating the object data but you get safety back!

```python {linenos=inline hl_lines=[9]}
# this will modify the dictionary
def modify_not(d: dict) -> None:
    if d:
        d.popitem()
    return

obj = {"name": "john", "surname": "doe"}

modify(obj.copy())  # pass a copy of the object!

print(f"obj: {obj}")  # should print obj: {"name": "john", "surname": "doe"}

modify(dict(obj))  # another way to make a copy is with the constructor functions!

print(f"obj: {obj}")  # should print obj: {"name": "john", "surname": "doe"}
```

To modify immutable values you simply have to store the reference to the newly created object. This way the label `obj` is now pointing to the new, incremented integer object and forgets about the original one. It is *as if* you modified an immutable object.

```python {linenos=inline hl_lines=[2, 4, 8]}
# this will modify the dictionary
def modify(d: int) -> int:
    d = d + 1
    return d

obj = 1

obj = modify(obj)

print(f"obj: {obj}")  # should print "obj: 2"
```

-----

### The devil is in the details 😈

The final boss of this topic is nested objects. In Python, anything is allowed and this means lists in lists in lists, lists of dictionaries, tuples with dictionaries and lists of strings, etc.

The copying techniques we've discussed so far, like list.copy() or dict.copy(), create shallow copies. This works great for simple lists of numbers or strings, but it can lead to unexpected behavior with nested mutable objects.

A shallow copy creates a new container object (e.g., a new list or dictionary) but populates it with references to the same nested objects from the original. This makes sense because these container objects are essentially a data structure of labels, not of actual data. Copying them only copies the top-level labels, not the objects they point to. If you modify a nested mutable object in the copied container, the original will also be affected because they both point to the same nested object.

```python {linenos=inline}
# A nested list, containing a mutable list inside
original_list = [[1, 2], [3, 4]]

shallow_copy = original_list.copy()

shallow_copy[0][0] = 99

print(f"Original list after shallow copy modification: {original_list}") # This should show [[99, 2], [3, 4]]!
```

To avoid this, you need a deep copy. A deep copy creates a completely new, independent object by recursively copying all the nested objects as well. No matter how many levels deep your data is, a deep copy ensures that every part of the new object is a unique instance. This is a surprisingly difficult task, because a list can contain itself!

You can easily create a deep copy using the copy module in the Python standard library. The copy.deepcopy() function handles the recursive copying for you, making your code safer and more predictable when dealing with complex nested data structures.

```python {linenos=inline hl_lines=[6]}
import copy

original_list = [[1, 2], [3, 4]]

# Create a deep copy
deep_copy = copy.deepcopy(original_list)

deep_copy[0][0] = 88

print(f"Original list after deep copy modification: {original_list}") # This should show [[1, 2], [3, 4]]!
```

### Final words
Understanding these nuances of Python's variable model is a big step in becoming proficient with the language. Think about the basic rules, follow the code and you'll see that most of the bugs you encounter can be solved with this line of thinking.

I hope you learned something while reading this!
