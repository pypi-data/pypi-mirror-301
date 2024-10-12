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



class CurrentHorizontalShearVariation_HorizontalShearVariationTypeEnum(str, Enum):
    PRESET_TRANSIENT = "PresetTransient"
    TIME_HISTORY = "TimeHistory"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class CurrentHorizontalShearVariation(BladedModel, ABC):
    r"""
    A defined variation in the current&#39;s horizontal shear.
    
    Not supported yet.
    
    Attributes:
    ----------
    HorizontalShearVariationType : CurrentHorizontalShearVariation_HorizontalShearVariationTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - PresetCurrentHorizontalShearTransient
        - CurrentHorizontalShearTimeHistory
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Current/CurrentHorizontalShearVariation/common/CurrentHorizontalShearVariation.json')
    
    HorizontalShearVariationType: Optional[CurrentHorizontalShearVariation_HorizontalShearVariationTypeEnum] = Field(alias="HorizontalShearVariationType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, HorizontalShearVariationType=None):
        cls._subtypes_[HorizontalShearVariationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("HorizontalShearVariationType")
            if data_type is None:
                raise ValueError("Missing 'HorizontalShearVariationType' in CurrentHorizontalShearVariation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'CurrentHorizontalShearVariation'")
            return sub(**data)
        return data


CurrentHorizontalShearVariation.update_forward_refs()
