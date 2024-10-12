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

from dnv_bladed_models.fault import Fault



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class PitchFault(Fault, ABC):
    r"""
    A fault in a single pitch system occuring at a specified time.
    
    Not supported yet.
    
    Attributes:
    ----------
    IsAmenableToSafetySystem : bool, Not supported yet
        If true, the safety system is able to intervene and take any specified action.  If false, the safety system will not respond to this event.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Event/common/PitchFault.json')
    
    IsAmenableToSafetySystem: Optional[bool] = Field(alias="IsAmenableToSafetySystem", default=None) # Not supported yet





PitchFault.update_forward_refs()
