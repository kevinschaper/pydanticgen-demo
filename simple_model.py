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
    
    id: str = Field(None)
    name: Optional[str] = Field(None)
    



# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
Person.update_forward_refs()

