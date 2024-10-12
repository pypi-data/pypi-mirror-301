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

from dnv_bladed_models.vector3_d import Vector3D



class NacelleSensor_NacelleSensorTypeEnum(str, Enum):
    ACCELEROMETER = "Accelerometer"
    INCLINOMETER = "Inclinometer"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class NacelleSensor(BladedModel, ABC):
    r"""
    The common properties of a sensor mounted on the nacelle.  This can be mounted anywhere on the structure.
    
    Not supported yet.
    
    Attributes:
    ----------
    NacelleSensorType : NacelleSensor_NacelleSensorTypeEnum, Not supported yet
        Defines the specific type of model in use.

    OffsetFromOrigin : Vector3D

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - NacelleAccelerometer
        - NacelleInclinometer
    
    """
    _relative_schema_path: str = PrivateAttr('Components/DrivetrainAndNacelle/NacelleSensors/NacelleSensor/common/NacelleSensor.json')
    
    NacelleSensorType: Optional[NacelleSensor_NacelleSensorTypeEnum] = Field(alias="NacelleSensorType", default=None) # Not supported yet
    OffsetFromOrigin: Optional[Vector3D] = Field(alias="OffsetFromOrigin", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, NacelleSensorType=None):
        cls._subtypes_[NacelleSensorType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("NacelleSensorType")
            if data_type is None:
                raise ValueError("Missing 'NacelleSensorType' in NacelleSensor")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'NacelleSensor'")
            return sub(**data)
        return data


NacelleSensor.update_forward_refs()
