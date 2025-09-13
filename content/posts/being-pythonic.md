+++
date = '2025-09-13T20:00:19+02:00'
title = 'Being pythonic'
tags = ['programming', 'statistics', 'python', 'basics']
+++
If you've been programming with python for more than a few months, or if you've ever read a tutorial or book or any other learning resource on the topic, chances are you've stumbled on the term `pythonic` or `idiomatic` code. In this post I will give my interpretation of the idea, why I do not think `pythonic` is yet another cringe keyword and how I try to remain `pythonic` when writing code.

-----

### Python is a tool and all tools are different

Ever seen an online discussion about how real programmers use Rust and oh-my-god-look-how-slow-Python-is? There are two takeaways from people who hold views like this:
- the person is very passionate and misses the big picture
- the person has no idea what he's talking about and misses the big picture

Python is a tool for a job, no more and no less. It is slow compared to low-level languages, it is also very fast about most tasks you will ever tackle, very easy to use and very expressive. You know how we have all sorts of knives, some for meat, others for smaller tasks? A butcher has a big knife that can cut bones, but a chef uses a smaller one to perform more delicate operations.

In the process of mastering a tool or a craft, you need to understand the differences between various tools and tasks. Python **is** on the slower end so it’s not the best fit for performance-critical software. Don't write a numerical analysis library with python. Feel free, however, to write wrapper code in Python. Write a machine learning library that makes it a breeze to interoperate and call the underlying C or Fortran implementations of numerical analysis libraries! This is how Numpy does it, how Pytorch does it.

The developers of Python know this. In fact, it is impossible for them to not know this since they actually write C code a lot of the time, not Python. The main Python implementation Python is called `CPython` and the C stands for C! To make your life easier, Python provides tools, trying to mask its weak points. This is what being pythonic is all about: understanding how you should use the language, play to its strengths and avoid its weak spots. In some ways, languages like C are easier than Python. Easy is probably the wrong word, simpler is more correct. The ease-of-use Python provides comes at a complexity cost, things hidden from you under many layers of abstraction. Python allows you to shoot yourself in the foot **very** easily, but thankfully being pythonic fixes this!

As an added bonus, the Python developers try to make the language feel as nice as possible so most of the time, the pythonic alternative will be shorter, look better and be more readable. It's not all that difficult to remain pythonic when writing code, so let's get to it.

-----

### Examples

#### List comprehensions

The example below is perfectly valid python code. It is also objectively bad python code. It will not matter if your code is a script that runs once in a while and handles a small amount of data but if it's serious code and the numbers list is large enough, you will notice the issues.

```python {linenos=inline}
# let's find the even numbers in this list
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers = []

for i in range(len(numbers)):
    if numbers[i] % 2 == 0:
        even_numbers.append(numbers[i])

print(even_numbers)
```
If you come from another, performant language like C or Java, you will probably not notice the problem. In fact, this is pretty much how you are expected to program this task! However, this code is garbage-level python code. The reasons are:
- a python list is **not** an array, it is a dynamic array - the `append` method adds an item to the end of the list but if at some point the list doesn't have enough space to fit the next element, python will have to copy the data to a new location in memory with more free space and this occasional resizing is costly
- in low-level statically-typed languages, the data types would be known at compile-time so the code would be (somewhat better) optimized for the operations that happen - incrementing the counter, checking if it's terminated, accessing `numbers[i]` and calling the `append` method
- there is a strong focus in python to use the expressiveness the language provides and write clean, minimal, "human-readable" code and we are not doing that here

The alternative is one of the most known python features, list comprehensions. The code above can be rewritten as:
```python {linenos=inline}
# let's find the even numbers in this list
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

even_numbers = [num for num in numbers if num % 2 == 0]

print(even_numbers)
```
What previously took 4 lines of code can be achieved with 1. In addition, it almost reads like human language. What's also great is that this operation is implemented in C and highly optimized. It is still a for-loop under the hood, but a fast, C for-loop. The performance difference can be about 3x on a sample of 1 million numbers which isn't a mind-boggling number but it is still 3 times faster **and** looks, reads and feels nicer. For 95% of the code people write, readability is more important than performance (source is me). The good thing is in our case, readability comes with a performance boost so there is no excuse!

#### Counter

This one is a great python party trick but also, another example of how Python tries to provide great tools for the most common use cases. You are tasked with counting the number of times each value in a list appears in that list. After a bit of thought, you may come up with the following implementation:
```python {linenos=inline}
counter = {}

for item in item_list:
    if item in counter:
        counter[item] += 1
    else:
        counter[item] = 1
```
There is not much wrong with this implementation. In fact, if this is all you need it works great and is pretty readable and maintainable. Then you get an extra requirement, you need the 3 most frequent values in the list. You are an experienced dev and love loops, so you quickly write some sound logic for it:
> disclaimer: this is LLM generated code, hence all the comments
```python {linenos=inline}
# Initialize the top_3 list with dummy values
 top_3 = []

for _ in range(3):
    top_3.append((None, -1))

for item, count in counter.items():
    # Iterate through the current top 3 to see where the new item fits
    for i in range(3):
        if count > top_3[i][1]:
            # Shift elements down to make room for the new item
            for j in range(2, i, -1):
                top_3[j] = top_3[j-1]
            
            # Insert the new item
            top_3[i] = (item, count)
            break  # Break the inner loop once the item is placed

# Filter out the dummy initial values
result = [item for item in top_3 if item[0] is not None]
```
We can all agree that this code just became a bit complex, maybe more complex than we would like! Fortunately, you remember that looping in Python is not great and look around for better options. Turns out the `sorted` function accepts a 2nd argument, a function that can be used to determine the correct order of the elements. You replace the complex logic with this nice 1-liner:
```python {linenos=inline}
sorted_items = sorted(counter.items(), key=lambda item: item[1], reverse=True)
result = sorted_items[:3]
```
Obviously much better than before. This implementation (let's call it implementation A) is already good enough - in just 11 lines of code (including whitespace) you have calculated the frequency counts and returned the 3 most popular items:
```python {linenos=inline}
# Implementation A

counter = {}

for item in item_list:
    if item in counter:
        counter[item] += 1
    else:
        counter[item] = 1

sorted_items = sorted(counter.items(), key=lambda item: item[1], reverse=True)

result = sorted_items[:3]
```
However, it can be even better than this. A coworker tells you about `collections.Counter`, you look it up and realise the solution can be even more concise. `collections.Counter` is a special python dictionary, custom-made for counting and performing related operations. One thing it provides is a default value equal to 0 if the value you look up is not present as a key. This means that the counting phase can be simplified like so:
```python {linenos=inline}
from collections import Counter

counter = Counter()

for item in item_list:
    counter[item] += 1
```
This is already a nice simplification, but it gets better. This pattern is so common that the `Counter` class can accept an iterable as an initialization argument and will run the dictionary with the calculated counts. You can therefore just do this:
```python {linenos=inline}
from collections import Counter

counter = Counter(item_list)
```
Remember how I said that `Counter` is custom-made for counting operations? It can help out with the 2nd part of the assignment too! The full solution to your problem (let's call this implementation B) can be as simple as this:
```python {linenos=inline}
# implementation B

from collections import Counter

counter = Counter(item_list)
result = counter.most_common(3)
```
I don't know about you but when I first learned about this object I found it pretty amazing! However, there is a cost to this ease-of-use and expressiveness: you need to know about it and so do others. Implementation A is barebones, can be read, understood, and implemented by almost everyone who knows basic python. Implementation B requires knowledge of the `collections` module's existence and its contents. 

This is not to say you should not use these tools! Something having a cost does not mean it's not worth paying for. This is just my personal point about implementation A having its own merits - it's still a perfectly fine and readable solution to the problem.

### Wrapping up

Python is easy to use but complicated to use and execute well. There is less need to be familiar with advanced algorithms but more need to be familiar with the contents of the standard library, the built-in functionality and the ecosystem of packages and libraries around it. You do not need to go inventing the wheel every time you have a task because the chances are there is already a good tool for you to use. However, you need to know about it or at least know how to find it.

Being pythonic is using the language the way it is intended to be used, what is also known as writing idiomatic code. By doing so, your code is cleaner and more readable, while also being more performant. It's just win-win!
