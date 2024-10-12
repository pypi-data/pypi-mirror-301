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



class VerticalShear_VerticalShearTypeEnum(str, Enum):
    EXPONENTIAL_SHEAR_MODEL = "ExponentialShearModel"
    LOGARITHMIC_SHEAR_MODEL = "LogarithmicShearModel"
    LOOK_UP_SHEAR_MODEL = "LookUpShearModel"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class VerticalShear(BladedModel, ABC):
    r"""
    The vertical wind shear to apply to the wind field.  This will vary the wind speed from 100% at the reference height (usually the hub height) down to 0% at ground level.
    
    Not supported yet.
    
    Attributes:
    ----------
    VerticalShearType : VerticalShear_VerticalShearTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - ExponentialShearModel
        - LogarithmicShearModel
        - LookUpShearModel
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/VerticalShear/common/VerticalShear.json')
    
    VerticalShearType: Optional[VerticalShear_VerticalShearTypeEnum] = Field(alias="VerticalShearType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, VerticalShearType=None):
        cls._subtypes_[VerticalShearType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("VerticalShearType")
            if data_type is None:
                raise ValueError("Missing 'VerticalShearType' in VerticalShear")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'VerticalShear'")
            return sub(**data)
        return data


VerticalShear.update_forward_refs()
