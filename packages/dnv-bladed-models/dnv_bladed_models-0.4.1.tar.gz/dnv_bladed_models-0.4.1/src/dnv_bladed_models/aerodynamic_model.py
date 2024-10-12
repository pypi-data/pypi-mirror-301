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

from dnv_bladed_models.sequential_timestep_adaptation import SequentialTimestepAdaptation



class AerodynamicModel_AerodynamicModelTypeEnum(str, Enum):
    BLADE_ELEMENT_MOMENTUM = "BladeElementMomentum"
    VORTEX_LINE = "VortexLine"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class AerodynamicModel(BladedModel, ABC):
    r"""
    Common properties for all aerodynamics models.
    
    Attributes:
    ----------
    AerodynamicModelType : AerodynamicModel_AerodynamicModelTypeEnum
        Defines the specific type of model in use.

    SequentialTimestepAdaptation : SequentialTimestepAdaptation, Not supported yet

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - BladeElementMomentum
        - VortexLine
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/AerodynamicModel/common/AerodynamicModel.json')
    
    AerodynamicModelType: Optional[AerodynamicModel_AerodynamicModelTypeEnum] = Field(alias="AerodynamicModelType", default=None)
    SequentialTimestepAdaptation: Optional[SequentialTimestepAdaptation] = Field(alias="SequentialTimestepAdaptation", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, AerodynamicModelType=None):
        cls._subtypes_[AerodynamicModelType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("AerodynamicModelType")
            if data_type is None:
                raise ValueError("Missing 'AerodynamicModelType' in AerodynamicModel")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'AerodynamicModel'")
            return sub(**data)
        return data


AerodynamicModel.update_forward_refs()
