from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union, Literal
from pydantic import BaseModel as BaseModel, Field
from linkml_runtime.linkml_model import Decimal

metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'
    
class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True, 
                validate_all = True, 
                underscore_attrs_are_private = True, 
                extra = 'forbid', 
                arbitrary_types_allowed = True):
    pass                    


class NamedThing(ConfiguredBaseModel):
    """
    Anything with a name and an ID
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:NamedThing"] = Field("pydanticgen-demo:NamedThing")
    


class Person(NamedThing):
    """
    A person
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Person"] = Field("pydanticgen-demo:Person")
    


class Ontologist(Person):
    """
    A person who builds ontologies
    """
    favorite_animals: Optional[Dict[str, Animal]] = Field(default_factory=dict)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Ontologist"] = Field("pydanticgen-demo:Ontologist")
    


class Programmer(Person):
    """
    A person who used to search stackoverflow a lot
    """
    favorite_plants: Optional[List[str]] = Field(default_factory=list)
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Programmer"] = Field("pydanticgen-demo:Programmer")
    


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
    


class Container(ConfiguredBaseModel):
    """
    A top level wrapper around a Person list
    """
    people: Optional[List[Union[Person,Ontologist,Programmer,Chef]]] = Field(default_factory=list)
    


class Animal(ConfiguredBaseModel):
    """
    A living thing that is not a plant
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Animal"] = Field("pydanticgen-demo:Animal")
    


class Plant(ConfiguredBaseModel):
    """
    A living thing that is not an animal
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Plant"] = Field("pydanticgen-demo:Plant")
    


class Fungi(ConfiguredBaseModel):
    """
    A living thing that is not an animal or a plant
    """
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    category: Literal["pydanticgen-demo:Fungi"] = Field("pydanticgen-demo:Fungi")
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
NamedThing.update_forward_refs()
Person.update_forward_refs()
Ontologist.update_forward_refs()
Programmer.update_forward_refs()
Chef.update_forward_refs()
Container.update_forward_refs()
Animal.update_forward_refs()
Plant.update_forward_refs()
Fungi.update_forward_refs()

