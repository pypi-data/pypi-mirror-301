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



class CurrentVerticalShearVariation_VerticalShearVariationTypeEnum(str, Enum):
    PRESET_TRANSIENT = "PresetTransient"
    TIME_HISTORY = "TimeHistory"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class CurrentVerticalShearVariation(BladedModel, ABC):
    r"""
    A defined variation in the current&#39;s vertical shear.
    
    Not supported yet.
    
    Attributes:
    ----------
    VerticalShearVariationType : CurrentVerticalShearVariation_VerticalShearVariationTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - PresetCurrentVerticalShearTransient
        - CurrentVerticalShearTimeHistory
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Current/CurrentVerticalShearVariation/common/CurrentVerticalShearVariation.json')
    
    VerticalShearVariationType: Optional[CurrentVerticalShearVariation_VerticalShearVariationTypeEnum] = Field(alias="VerticalShearVariationType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, VerticalShearVariationType=None):
        cls._subtypes_[VerticalShearVariationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("VerticalShearVariationType")
            if data_type is None:
                raise ValueError("Missing 'VerticalShearVariationType' in CurrentVerticalShearVariation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'CurrentVerticalShearVariation'")
            return sub(**data)
        return data


CurrentVerticalShearVariation.update_forward_refs()
