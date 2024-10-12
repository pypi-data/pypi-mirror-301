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

from dnv_bladed_models.initial_condition import InitialCondition



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class InitialControlState(InitialCondition, ABC):
    r"""
    The initial operational state of the turbine.
    
    Not supported yet.
    
    Attributes:
    ----------
    OnComponentInAssembly : str, Not supported yet
        The rotor which is in this state.  If omitted, all rotors on the turbine will be in this state.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/InitialCondition/common/InitialControlState.json')
    
    OnComponentInAssembly: Optional[str] = Field(alias="OnComponentInAssembly", default=None) # Not supported yet



    @validator("OnComponentInAssembly")
    def OnComponentInAssembly_pattern(cls, value):
        if value is not None and not re.match(r"^#\/ComponentDefinitions\/(.+)$", value):
            raise ValueError(f"OnComponentInAssembly did not match the expected format (found {value})")
        return value



InitialControlState.update_forward_refs()
