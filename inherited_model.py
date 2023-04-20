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
    


class Container(ConfiguredBaseModel):
    """
    A top level wrapper around a Person list
    """
    people: Optional[List[Union[Person,Ontologist,Programmer]]] = Field(default_factory=list)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Person.update_forward_refs()
Ontologist.update_forward_refs()
Programmer.update_forward_refs()
Container.update_forward_refs()

