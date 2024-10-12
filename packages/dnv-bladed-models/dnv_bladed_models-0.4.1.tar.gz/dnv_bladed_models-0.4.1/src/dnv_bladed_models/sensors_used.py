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



class SensorsUsed_SensorsUsedTypeEnum(str, Enum):
    LEGACY_SENSOR_MAPPINGS = "LegacySensorMappings"
    SENSOR_MAPPING = "SensorMapping"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class SensorsUsed(BladedModel, ABC):
    r"""
    This section references all of the sensors that can be used by the external controller.
    
    Not supported yet.
    
    Attributes:
    ----------
    SensorsUsedType : SensorsUsed_SensorsUsedTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - LegacySensorMappings
        - SensorMapping
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/SensorsUsed/common/SensorsUsed.json')
    
    SensorsUsedType: Optional[SensorsUsed_SensorsUsedTypeEnum] = Field(alias="SensorsUsedType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, SensorsUsedType=None):
        cls._subtypes_[SensorsUsedType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("SensorsUsedType")
            if data_type is None:
                raise ValueError("Missing 'SensorsUsedType' in SensorsUsed")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'SensorsUsed'")
            return sub(**data)
        return data


SensorsUsed.update_forward_refs()
