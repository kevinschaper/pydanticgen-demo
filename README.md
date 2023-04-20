# pydanticgen-demo
A small demonstration of LinkML's pydantic code generator


## Overview

Pydanticgen is one of two LinkML tools for generating Python classes from a LinkML schema. 

## Differences from Pythongen
- Checks constraints both when you create an instance and when you update it 
- Works with FastAPI
- No runtime linkml dependency

## Installation

The `gen-pydantic` command is bundled with linkml, which can be included as a python dependency in a project, or installed within a pipx sandbox:

```bash
pipx install linkml
```

Within this demo, you can get started with
```bash
pipx install poetry # if you don't have it already
poetry install # to create the virtual environment and install required packages
poetry shell # to launch the virtual environment
```


## Basic Usage

`gen-pydantic` runs as a standalone script that takes the schema yaml as an argument, and prints the generated code to stdout.

```bash
gen-pydantic simple-model.yaml > simple_model.py
```

The generated code can then be imported and used in python:
```python
from simple_model import Person

p = Person(id="P:1", name="John Doe")
p2 = Person(id="P:2", name="Jane Doe")
```

Trying to set a property that doesn't exist in the schema will trigger a validation error
```python
from simple_model import Person

p = Person(id="P:1", name="John Doe", age=42)
```
```
pydantic.error_wrappers.ValidationError: 1 validation error for Person
age
  extra fields not permitted (type=value_error.extra)
```
(The `Person` class and the `age` field are the key things to find in that error message. It's notable and intentional that values that fail to validate aren't shown in pydantic error messages.)

As will trying to set a property after initialization
```python
from simple_model import Person

p = Person(id="P:1", name="John Doe")
p.age = 42
```
```
ValueError: "Person" object has no field "age"
```

## Inheritance and type designators

Pydanticgen supports inheritance by flattening

```bash
gen-pydantic inherited-model.yaml > inherited_model.py
```

This will produce the following representation of the inherited Person classes in the schema:

```python
class Person(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Person"] = Field("pydanticgen-demo:Person")
    


class Ontologist(Person):
    """
    A person who builds ontologies
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Ontologist"] = Field("pydanticgen-demo:Ontologist")
    favorite_animals: Optional[List[str]] = Field(default_factory=list)
    


class Programmer(Person):
    """
    A person who used to search stackoverflow a lot
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Programmer"] = Field("pydanticgen-demo:Programmer")
    favorite_plants: Optional[List[str]] = Field(default_factory=list)

```

The inherited slots are flattened in the generated code, which has an advantage for readability - because you can look at a class and see all available properties. 

Adding the `category` slot with `type_designator: true` allows for instantiating classes based on an ancestor class and having the python type still be correct. Also, the prepopulated value of the field will vary based on the type provided, with support for uri, uriorcurie, and string. If a default_prefix is provided, uriorcurie will generate a curie, and a uri otherwise. With the range set to string, the class name itself will be used.

```python
import yaml
from typing import List
from pydantic import parse_obj_as
from inherited_model import Container, Person, Ontologist, Programmer

people_json = \
"""
{    
    "people": [
        {
            "id": "P:1",
            "name": "John Doe",
            "category": "pydanticgen-demo:Ontologist",
            "favorite_animals": [
                "cat",
                "dog"
            ]
        },
        {
            "id": "P:2",
            "name": "Jane Doe",
            "category": "pydanticgen-demo:Programmer",
            "favorite_plants": [
                "cactus",
                "succulent"
            ]
        }
    ]    
}
"""

people = Container.parse_raw(people_json).people

assert isinstance(people[0], Ontologist)
assert isinstance(people[1], Programmer)

print(people[0])
```

## Inlining for dict vs list, tweaking with slot_usage

```bash
gen-pydantic inlining-model.yaml > inlining_model.py
```

In this schema, Plants and Animals have graduated to being represented with classes that are collections on the Person classes. 

When `inlined: true` on a class range, the python produced will be a Dict mapping from the identifier type (a string in this case) to the class type.

```linkml
  favorite_animals:
    range: Animal
    multivalued: true
    inlined: true
```

produces:
```python
    favorite_animals: Optional[Dict[str, Animal]] = Field(default_factory=dict)
```

With inlined as list, a list of the class type will be generated:
```linkml
  favorite_fungi:
    range: Fungi
    multivalued: true
    inlined_as_list: true
```
```python
    favorite_fungi: Optional[List[Fungi]] = Field(default_factory=list)
```

`inlined: false` will represent a class using the range of its identifier slot

```linkml
  favorite_plants:
    range: Plant
    multivalued: true
    inlined: false
```

```python
    favorite_plants: Optional[List[str]] = Field(default_factory=list)
```


Additionally, `slot_usage` can be used to change inlining behavior for a slot for a class (and its descendants):

```linkml
  Chef:
      description: A person who cooks
      is_a: Person
      slots:
        - favorite_animals
        - favorite_plants
        - favorite_fungi
      slot_usage:
        favorite_animals:
          inlined_as_list: true
        favorite_plants:
          inlined_as_list: true
```
produces a Chef class with all the favorites inlined as lists:
```python
class Chef(Person):
    """
    A person who cooks
    """
    favorite_animals: Optional[List[Animal]] = Field(default_factory=list)
    favorite_plants: Optional[List[Plant]] = Field(default_factory=list)
    favorite_fungi: Optional[List[Fungi]] = Field(default_factory=list)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Chef"] = Field("pydanticgen-demo:Chef")

```

Putting it all together

```python
from inlining_model import Programmer, Ontologist, Chef, Plant, Animal, Fungi

c = Chef(id="P:1", name="Julia")
p = Programmer(id="P:2", name="John")
o = Ontologist(id="P:3", name="Jane")

p1 = Plant(id="PL:1", name="cactus")
p2 = Plant(id="PL:2", name="succulent")
a1 = Animal(id="A:1", name="cat")
a2 = Animal(id="A:2", name="dog")
f1 = Fungi(id="F:1", name="mushroom")
f2 = Fungi(id="F:2", name="yeast")

o.favorite_animals = {a1.id: a1, a2.id: a2}
p.favorite_plants = [p1.id, p2.id]

c.favorite_plants = [p1, p2]
c.favorite_animals = [a1, a2]
c.favorite_fungi = [f1, f2]
```