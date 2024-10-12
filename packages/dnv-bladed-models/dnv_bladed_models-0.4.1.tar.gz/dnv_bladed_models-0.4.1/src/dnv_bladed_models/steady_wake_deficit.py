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

from dnv_bladed_models.bladed_model import BladedModel



class SteadyWakeDeficit_SteadyWakeDeficitTypeEnum(str, Enum):
    GAUSSIAN = "Gaussian"
    USER_DEFINED = "UserDefined"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class SteadyWakeDeficit(BladedModel, ABC):
    r"""
    A simple model for the reduced velocity of the wind behind another turbine.  This deficit will be applied across a certain region, and this region will not move around during the simulation.
    
    Not supported yet.
    
    Attributes:
    ----------
    SteadyWakeDeficitType : SteadyWakeDeficit_SteadyWakeDeficitTypeEnum, Not supported yet
        Defines the specific type of model in use.

    HorizontalOffsetFromHub : float, Not supported yet
        The horizontal (global Y) offset of the upwind turbine from the turbine being simulated.

    VerticalOffsetFromHub : float, Not supported yet
        The vertical (global Z) offset of the upwind turbine from the turbine being simulated.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - Gaussian
        - UserDefinedWakeDeficit
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/SteadyWakeDeficit/common/SteadyWakeDeficit.json')
    
    SteadyWakeDeficitType: Optional[SteadyWakeDeficit_SteadyWakeDeficitTypeEnum] = Field(alias="SteadyWakeDeficitType", default=None) # Not supported yet
    HorizontalOffsetFromHub: Optional[float] = Field(alias="HorizontalOffsetFromHub", default=None) # Not supported yet
    VerticalOffsetFromHub: Optional[float] = Field(alias="VerticalOffsetFromHub", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, SteadyWakeDeficitType=None):
        cls._subtypes_[SteadyWakeDeficitType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("SteadyWakeDeficitType")
            if data_type is None:
                raise ValueError("Missing 'SteadyWakeDeficitType' in SteadyWakeDeficit")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'SteadyWakeDeficit'")
            return sub(**data)
        return data


SteadyWakeDeficit.update_forward_refs()
