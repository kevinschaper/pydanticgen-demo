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

## Usage

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

```python

class Person(ConfiguredBaseModel):
    
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["Person"] = Field("Person")
    
class Ontologist(Person):
    """
    A person who builds ontologies
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["Ontologist"] = Field("Ontologist")
    favorite_animals: Optional[List[str]] = Field(default_factory=list)

class Programmer(Person):
    """
    A person who used to search stackoverflow a lot
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["Programmer"] = Field("Programmer")
    favorite_plants: Optional[List[str]] = Field(default_factory=list)

```
