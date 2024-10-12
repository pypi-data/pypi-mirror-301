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

from dnv_bladed_models.current import Current

from dnv_bladed_models.current_direction_variation import CurrentDirectionVariation



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TimeDomainCurrent(Current, ABC):
    r"""
    The definition of a current field that varies throughout a time domain simulation.
    
    Not supported yet.
    
    Attributes:
    ----------
    ReferenceHeight : float, Not supported yet
        The reference height for the current field, above which the free-field current conditions take over.  If this is omitted, the hub height will be used, and if there is more than one the *highest* hub height.

    Inclination : float, default=0, Not supported yet
        The inclination of the flow relative to the horizontal plane.

    Direction : float, Not supported yet
        The (constant) direction of the current relative to the global X axis.

    DirectionVariation : CurrentDirectionVariation, abstract, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    DirectionVariation has the following concrete types:
        - PresetCurrentDirectionTransient
        - CurrentDirectionTimeHistory
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Current/common/TimeDomainCurrent.json')
    
    ReferenceHeight: Optional[float] = Field(alias="ReferenceHeight", default=None) # Not supported yet
    Inclination: Optional[float] = Field(alias="Inclination", default=0) # Not supported yet
    Direction: Optional[float] = Field(alias="Direction", default=None) # Not supported yet
    DirectionVariation: Optional[CurrentDirectionVariation] = Field(alias="DirectionVariation", default=None) # Not supported yet





TimeDomainCurrent.update_forward_refs()
