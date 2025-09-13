+++
date = '2025-08-26T22:00:19+02:00'
title = 'Labels, not boxes: v2'
tags = ['programming', 'python', 'basics']
+++
Simple stuff is simple but chain a lot of simple stuff together and you definitely reach a point where the complexity builds up. Continuing on the [previous post]({{< ref "posts/labels-not-boxes.md" >}}), here’s a more advanced look at Python containers.

### Containers

With the term `containers` I refer to data structures that contain other objects: lists, tuples, dictionaries, etc. They can hold any objects, even themselves!
```python {linenos=inline}
l = [1, 2]
print(id(l))  # list ID

l.append(l)   # append list to itself

for i in range(len(l)):
    print(f"Element {l[i]} with id: {id(l[i])}")

print(l[-1][0])   # 1
print(l[-1][-1])  # [1, 2, [...]]
```
Pointer logic works more or less the same in all languages so the above is not very surprising, but it showcases whats possible when working with references.

-----

### Mutable containers

Consider a function that sorts and modifies a list of dicts:
```python {linenos=inline}
def process_and_modify(dict_list: list[dict]) -> list[dict]:
    sorted_list = sorted(dict_list, key=lambda d: d["name"])
    for d in sorted_list:
        d["processed"] = True
        d["score"] = d.get("score", 0) * 2
    
    return sorted_list

original_list = [
    {"name": "Charlie", "score": 10},
    {"name": "Alice", "score": 20}, 
    {"name": "Bob", "score": 15}
]

sorted_result = process_and_modify(original_list)

print(sorted_result)
print(original_list)
```

We see that `sorted_result` comes out sorted and modified. In addition, `original_list` is also modified. Why?

The result is not **that** surprising but in case you wonder, here's what's happening:
- copying a container object copies references
- the order of the references is an attribute of the container, not the objects
- modifications to the shared data persist regardless of what the function returns

The lesson here is that by copying by object reference, Python minimizes the memory overhead while also maximizing the risk of unintentional modifications to the data.

-----

### A (slightly) more complex example

A large part of what **pythonic** means, to me at least, is knowing and using the tools the language provides to streamline and perform certain operations. I will talk about this in a future post but for now, let me introduce `itertools.groupby`. Here's a short example of how it works:

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

```python {linenos=inline}
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
There is no need for new structures or containers! The list and the items are modified in place because `groupby` simply returns references to the underlying dicts.

### Wrapping up

Working with containers in Python boils down to a simple idea: everything is a reference. Knowing this, a lot of Python’s behavior feels less "weird" and more "logical".

The key takeaways are:
- containers don’t hold values, they hold references
- copying a container doesn’t duplicate the underlying objects, it duplicates references to them
- mutability means changes propagate across references unless you explicitly create deep copies
- most built-in functions (like `sorted`, `groupby`, etc.) rarely copy data

Thanks for reading.
