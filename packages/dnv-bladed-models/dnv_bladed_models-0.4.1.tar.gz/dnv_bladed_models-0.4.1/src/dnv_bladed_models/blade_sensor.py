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



class BladeSensor_BladeSensorTypeEnum(str, Enum):
    ACCELEROMETER = "Accelerometer"
    STRAIN_GAUGE = "StrainGauge"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladeSensor(BladedModel, ABC):
    r"""
    The common properties of all sensors on the blade.
    
    Not supported yet.
    
    Attributes:
    ----------
    BladeSensorType : BladeSensor_BladeSensorTypeEnum, Not supported yet
        Defines the specific type of model in use.

    DistanceFromBladeRoot : float, Not supported yet
        The distance along the blade, measured from the root of the blade component.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - BladeAccelerometer
        - BladeStrainGauge
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeSensors/BladeSensor/common/BladeSensor.json')
    
    BladeSensorType: Optional[BladeSensor_BladeSensorTypeEnum] = Field(alias="BladeSensorType", default=None) # Not supported yet
    DistanceFromBladeRoot: Optional[float] = Field(alias="DistanceFromBladeRoot", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, BladeSensorType=None):
        cls._subtypes_[BladeSensorType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("BladeSensorType")
            if data_type is None:
                raise ValueError("Missing 'BladeSensorType' in BladeSensor")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'BladeSensor'")
            return sub(**data)
        return data


BladeSensor.update_forward_refs()
