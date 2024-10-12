# coding: utf-8

from __future__ import annotations

from abc import ABC

from datetime import date, datetime  # noqa: F401
from enum import Enum, IntEnum

import re  # noqa: F401
from typing import Any, Dict, List, Optional, Type, Union, Callable  # noqa: F401
from pathlib import Path
from typing import TypeVar
Model = TypeVar('Model', bound='BaseModel')
StrBytes = Union[str, bytes]

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator, root_validator, Extra,PrivateAttr  # noqa: F401
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.utils import ROOT_KEY
from json import encoder



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladedModel(CommonBaseModel, ABC):
    r"""
    The base schema for all Bladed schema objects, allowing $insert and $insertAndOverride behaviour.
    
    Attributes:
    ----------
    Schema : str
        The location of the JSON schema used to validate this object and enable enhanced tooling support.

    insert : str, Not supported yet
        If the $insert keyword is provided, ALL properties will be taken from the referenced object, and no additional properties can be specified.

    insertAndOverride : str, Not supported yet
        If the $insertAndOverride keyword is provided, properties will be taken from the referenced object, but any properties specified alongside it will be taken in preference to it.

    DerivedType : str
        Not used

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('common/BladedModel.json')
    
    Schema: Optional[str] = Field(alias="$schema", default=None)
    insert: Optional[str] = Field(alias="$insert", default=None) # Not supported yet
    insertAndOverride: Optional[str] = Field(alias="$insertAndOverride", default=None) # Not supported yet
    DerivedType: Optional[str] = Field(alias="DerivedType", default=None)





BladedModel.update_forward_refs()
