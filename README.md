A dictionary wrapper that allows attribute access and mutation using both dot notation and dictionary-style indexing.

## Installation

`pip install DynamicDict`

## Simple Usage

```python
from DynamicDict import dynamic
dyn = dynamic()
dyn.key = "Value"
print(dyn.key) # Output: Value

dyn2 = dynamic({'key':'value'},False) # Initialize with lax subtraction
dyn._strict_subtraction = False # Set lax subtraction
```

## Parameters

Note: These are also 'reserved' keys on the instance. They can be directly set and referenced.

- `_dict: Optional[Dict[str, Any]]` -- Stores all of the instance data.
    - `{}` (default): `None` will be initialized to an empty dictionary.
- `_strict_subtraction: Optional[bool]` -- Specifies how subtraction operations will behave.
    - `True` (default): Subtraction operations will only remove matching keys if the corresponding values also match.
    - `False`: Subtraction operations will remove any matching keys found, regardless of value.

## Features

- Dynamic Nesting -- Any dictionary added to a dynamic is automatically converted to a dynamic, allowing seamless nesting of dynamic objects.
- Keys as Attributes -- Keys and Values can be accessed and set using dot notation or key notation.
    - Any non-alphanumeric characters in dictionary keys will be replaced with underscores to be usable as attributes. Please note: this renaming could result in duplicate keys. Behavior of duplicate keys is undefined (the last one evaluated will be set, but ordering isn't guaranteed).
- Direct Callables -- Keys can be assigned to functions, which allows calling them directly using dot notation.
    - Functions added to a dynamic object are not class methods, and do not have access to the `self` instance context.
- Dictionary Compatibility -- Dynamic objects support common pythonic dictionary operations like iteration, item retrieval, and containment checks.
    - To preserve namespace availability, dictionary methods like `get`/`add`/`keys`/`pop`/`clear`/etc. are not implemented directly. You can use the `_dict` element to access them directly on the underlying dictionary `dyn._dict.get('key1')`.
    - Iteration uses the dictionary tuple `.items()` iterator. E.g. `for key, val in some_dynamic...`.
- Arithmetic Operations -- Use addition `+`/`+=` or subtraction `-`/`-=` operations for set-like operations to add or remove attributes.
    - Strict Substraction: By default, subtraction only removes matching keys and values. This can be changed to just check keys. See `_strict_subtraction` parameter above for details.
- String Representation -- Casting to a string returns the string representation of the internal dictionary.
- Attribute Deletion -- Allows for the deletion of attributes using the `del` keyword. This also works for nested keys.
- Equality Comparison -- Supports equality checks with both dictionaries and other dynamic objects.
- Boolean Context -- Evaluates to `False` if the internal dictionary is empty.
- No Dependencies -- Only uses features available in the Python Standard Library!

## More Examples

```python
data = {
    "name": "John",
    "age": 30,
    "address": {
        "city": "New York",
        "zip": "10001"
    }
}

dyn = dynamic(data)
# or
dyn2 = dynamic()
dyn2 += data

assert dyn == dyn2 # True
assert dyn == data # True
assert "name" in dyn # True

print(dyn.name)  # Output: John
print(dyn.address.city)  # Output: New York

dyn.job = "Engineer"
print(dyn.job)  # Output: Engineer

s = ""
for key, value in dyn.address:
    s += f"{key}:{value},"
print(s) # Output: city:New York,zip:10001,

dyn += {"hobby": "Photography"}
print(dyn.hobby)  # Output: Photography

del dyn.age
print(dyn.age)  # Raises AttributeError

def f():
    print("Hello World")
dyn.f = f
dyn.f() # Output Hello World
```

Check out the unit tests for even more thorough usage examples.