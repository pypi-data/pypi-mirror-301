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

from dnv_bladed_models.timed_event import TimedEvent



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ControlledOperation(TimedEvent, ABC):
    r"""
    An operation occuring at a specified time.  This will be implemented by the controller, and Bladed will send it a signal at the time it should occur.
    
    Not supported yet.
    
    Attributes:
    ----------
    OnComponentInAssembly : str, Not supported yet
        A reference to the component in the assembly to which this applies.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Event/common/ControlledOperation.json')
    
    OnComponentInAssembly: Optional[str] = Field(alias="OnComponentInAssembly", default=None) # Not supported yet



    @validator("OnComponentInAssembly")
    def OnComponentInAssembly_pattern(cls, value):
        if value is not None and not re.match(r"^#\/ComponentDefinitions\/(.+)$", value):
            raise ValueError(f"OnComponentInAssembly did not match the expected format (found {value})")
        return value



ControlledOperation.update_forward_refs()
