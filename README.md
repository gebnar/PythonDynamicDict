A dictionary wrapper that allows attribute access and mutation using both dot notation and dictionary-style indexing.

## Installation

`pip install DynamicDict`

## Simple Usage

```python
from DynamicDict import Dynamic
dyn = Dynamic()
dyn.key = "Value"
print(dyn.key) # Output: Value

dyn2 = Dynamic({'key':'value'},_strict_typing = True) # Initialize with optional setting
dyn._strict_subtraction = False # Set optional setting
```

## Parameters

These are safe to set after instantiation using normal dot notation (e.g. `dyn._dict = some_dict`).

- `_dict: Optional[Dict[str, Any]]` -- Stores the attribute data.
    - `{}` (default): `None` will be initialized to an empty dictionary.
- `_strict_typing: Optional[bool]` -- Specifies whether attributes should have strict or dynamic typing.
    - `False` (default): Attributes can be reassigned to anything, like any other python variable.
    - `True`: A TypeError will be thrown when updating an attribute value to something that doesn't match the current value's type.
- `_strict_subtraction: Optional[bool]` -- Specifies how subtraction operations will behave.
    - `True` (default): Subtraction operations will only remove matching keys if the corresponding values also match.
    - `False`: Subtraction operations will remove any matching keys found, regardless of value.

## Namespace Usage

Care has been taken to avoid polluting the attribute namespace more than necessary. Here is the complete list of internal parameters used by the class.

- These attributes are "safe" / intended to be modified directly
    - `_dict`
    - `_strict_subtraction`
    - `_strict_typing`
- These attributes should not be modified.
    - `_dict_types`
    - `_bind_self`

## Features

- Automatic Nesting -- Any dictionary added to a dynamic is automatically converted to a dynamic, allowing seamless nesting of dynamic objects.
- Strict Typing -- By enabling the optional `_strict_typing` parameter, you can force type matching during attribute reassignment.
- Keys as Attributes -- Keys and Values can be accessed and set using dot notation or key notation.
    - Any non-alphanumeric characters in dictionary keys will be replaced with underscores to be usable as attributes. Please note: this renaming could result in duplicate keys. Behavior of duplicate keys is undefined (the last one evaluated will be set, but ordering isn't guaranteed).
- Callable Integration -- Keys can be assigned to anything, including functions, which allows calling them directly using dot notation.
    - Functions called from a dynamic object context are wrapped to give optional access to `self`. If the first parameter of a function is `self` then the parent dynamic instance is prepended to the arguments when the function is called.
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

dyn = Dynamic(data)
# or
dyn2 = Dynamic()
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

def get_name(self):
    return self.name
dd = Dynamic({'name':'John'})
dd.get_name = get_name
assert dd.get_name() == 'John'
```

Check out the unit tests for even more thorough usage examples.