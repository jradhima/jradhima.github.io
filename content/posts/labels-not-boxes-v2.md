+++
date = '2025-08-26T22:00:19+02:00'
title = 'Labels, not boxes: v2'
tags = ['programming', 'python', 'basics']
+++
Simple stuff is simple but chain a lot of simple stuff together and you definitely reach a point where the complexity builds up. Continuing on the [previous post]({{< ref "posts/labels-not-boxes.md" >}}) where I showed the basics, I want to give a more advanced example that will showcase how some interesting cases.

### Containers

With the term `containers` I refer to data structures that contain other objects: lists, tuples, dictionaries, etc. Python imposes no limits to what you can achieve: any possible combination will do and you can nest objects in objects for days. As a matter of fact, a container object can contain itself!

Let's see.

```python
# create a list
l = [1, 2]

print(f"The ID of the list that variable 'l' references is: {id(l)}")
# The ID of the list that variable 'l' references is: 4351720640

# append the list to itself
l.append(l)

# let's see the elements of the list
for i in range(len(l)):
    print(f"Element {l[i]} with id: {id(l[i])}")

# Element 1 with id: 4348600480
# Element 2 with id: 4348600512
# Element [1, 2, [...]] with id: 4351720640

print(l[-1][0])  # 1
print(l[-1][-1])  # [1, 2, [...]]
```

Pointer logic works more or less the same in all languages so the above is not very surprising, but it showcases whats possible when working with references.

-----

### Mutable containers

Take a look at the following code. It's a simple python function that expects a list of dictionaries as it's argument. Keep in mind that the `sorted` function returns a copy of the original list rather than sorting it inplace. You have to use `list.sort()` for that.

```python
def process_and_modify(dict_list: list[dict]) -> list[dict]:
    # Sort the list (creates new ordering)
    sorted_list = sorted(dict_list, key=lambda d: d["name"])
    
    # Modify the dicts in-place
    for d in sorted_list:
        d["processed"] = True
        d["score"] = d.get("score", 0) * 2
    
    return sorted_list

# Original data
original_list = [
    {"name": "Charlie", "score": 10},
    {"name": "Alice", "score": 20}, 
    {"name": "Bob", "score": 15}
]

# Call function
sorted_result = process_and_modify(original_list)
```

We expect that `sorted_result` now contains the people sorted by their name, a new `processed` key, and doubled age. Has anything happened to `original_list`? Let's see.

```python
# Sorted result: just as expected
print([d for d in sorted_result])

# Original list: modified items, still in original order
print([d for d in original_list])
```

The result is not **that** surprising but in case you wonder, here's what's happening:
- copying a container object only copies the references
- the order of the references is an attribute of the container, not the objects
- modifications to the shared data persist regardless of what the function returns
- modifications to the containers (obviously) do not affect the contained data

The lesson here is that by copying by object reference, Python greatly minimizes the memory overhead that could happen. However, it also maximizes the risk of unintentional modifications to the data.

-----

### A (slightly) more complex example

A large part of what **pythonic** means, to me at least, is knowing and using the tools the language provides to streamline and perform certain operations. I will talk about this in a future post but for now, let me introduce `itertools.groupby`. 

Function `itertools.groupby` is part of the standard library and does what the name suggests: it expects an iterator, i.e. objects where you can use `for item in X`,  and groups the items based on a key function. People with experience in data analysis and/or SQL are for sure familiar with the concept of grouping records by values.

Here's a short example of how it works:

```python {linenos=inline hl_lines=[10,11]}
from itertools import groupby

data = [
    {"category": "A", "value": 10},
    {"category": "B", "value": 20},
    {"category": "A", "value": 15},
    {"category": "B", "value": 25},
]

# Sort by the grouping key, groupby requires sorted data to work
data.sort(key=lambda d: d["category"])

for category, group_items in groupby(data, key=lambda d: d["category"]):
    items_list = list(group_items)  # Convert iterator to list
    print(f"Items in group {category}: {items_list}")

# Items in group A: [{'category': 'A', 'value': 10}, {'category': 'A', 'value': 15}]
# Items in group B: [{'category': 'B', 'value': 20}, {'category': 'B', 'value': 25}]
```

So now let's imagine a scenario where we want to modify our user data but instead of outright doubling the scores, we double them for users with short hair and triple them for ones with long hair. It just makes sense!

```python
users = [
    {"name": "Charlie", "score": 10, "hair": "short"},
    {"name": "Alice", "score": 20, "hair": "long"}, 
    {"name": "Bob", "score": 15, "hair": "short"},
    {"name": "Daphne", "score": 30, "hair": "long"},
    {"name": "Elena", "score": 35, "hair": "long"}
]

def update_scores(users: list[dict]) -> list[dict]:
    # sort the users once more
    users.sort(key=lambda d: d["hair"])

    users_updated = [] # we will keep the updated users here

    for hair_length, group_members in groupby(users, key=lambda d: d["hair"]):
        members = list(group_members)
        for member in members:
            member["score"] *= 3 if hair_length == "long" else 2
        
        users_updated += members # add the modified users to the results
    
    return users_updated # return the results

new_users = update_scores(users.copy()) # pass a copy to the function

# New users list is as expected
print(new_users)

# [
#     {'name': 'Alice', 'score': 60, 'hair': 'long'},
#     {'name': 'Daphne', 'score': 90, 'hair': 'long'},
#     {'name': 'Elena', 'score': 105, 'hair': 'long'},
#     {'name': 'Charlie', 'score': 20, 'hair': 'short'},
#     {'name': 'Bob', 'score': 30, 'hair': 'short'}
# ]
```
This all seems like standard stuff:
- sort the items (necessary)
- make a result list to keep the items
- groupby the key
- receive the items that belong to a group
- update and append them to the result list
- return the updated records

However, depending on what you want to achieve this implementation does a lot of things that are not necessary. If maintaining the order of your users list is not important, it can be simplified a lot!

```python {linenos=inline}
from itertools import groupby

# same users list as before...

def update_scores(users: list[dict]) -> None:
    users.sort(key=lambda d: d["hair"])
    for hair_length, group in groupby(users, key=lambda d: d["hair"]):
        for member in group:
            member["score"] *= 3 if hair_length == "long" else 2

update_scores(users)  # modifies in place

print(users)
# scores updated, order changed by hair length
```

Since everything is a reference and we are working with mutable data, we do not need to create new structures. Even if we do not explicitly modify the `users` list, since python always shares the underlying objects we end up modifying them inplace!

Even the groupby function that receives the original list and returns parts of it, it simply returns small groups of references to the same dictionaries. It is rare for a python function to copy the objects it works with, at least not implicitly.

### Wrapping up

Working with containers in Python boils down to a simple but powerful principle: everything is a reference. Once you internalize that, a lot of Python’s behavior feels less "weird" and more "logical".

The lessons to keep are:
- containers don’t hold values, they hold references
- copying a container doesn’t duplicate the underlying objects, it duplicates references to them
- mutability means changes propagate across references unless you explicitly create deep copies
- most built-in functions and libraries (like sorted, groupby, etc.) operate in ways that emphasize references over values

Thanks for reading.
