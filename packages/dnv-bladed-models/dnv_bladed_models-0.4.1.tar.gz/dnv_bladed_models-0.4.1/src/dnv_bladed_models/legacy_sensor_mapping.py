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



class LegacySensorMapping_LegacySensorMappingTypeEnum(str, Enum):
    LEGACY_BLADE_SENSOR_MAPPING = "LegacyBladeSensorMapping"
    LEGACY_NACELLE_SENSOR_MAPPING = "LegacyNacelleSensorMapping"
    LEGACY_TOWER_SENSOR_MAPPING = "LegacyTowerSensorMapping"

class LegacySensorMapping_SensorTypeEnum(str, Enum):
    ACCELEROMETER = "ACCELEROMETER"
    INCLINOMETER = "INCLINOMETER"
    STRAIN_GAUGE = "STRAIN_GAUGE"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class LegacySensorMapping(BladedModel, ABC):
    r"""
    The controller interface used by 4.X compatible controllers need to have a mapping between how they are referenced now, and how they used to be referenced.
    
    Not supported yet.
    
    Attributes:
    ----------
    LegacySensorMappingType : LegacySensorMapping_LegacySensorMappingTypeEnum, Not supported yet
        Defines the specific type of model in use.

    SensorType : LegacySensorMapping_SensorTypeEnum, Not supported yet
        The type of the sensor on the component.  These are stored in separate lists, and the mapping will need to know which list to look in.

    SensorIndex : int, Not supported yet
        The index of the sensor, as the controller would access it.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - LegacyBladeSensorMapping
        - LegacyNacelleSensorMapping
        - LegacyTowerSensorMapping
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/SensorsUsed/LegacySensorMapping/common/LegacySensorMapping.json')
    
    LegacySensorMappingType: Optional[LegacySensorMapping_LegacySensorMappingTypeEnum] = Field(alias="LegacySensorMappingType", default=None) # Not supported yet
    SensorType: Optional[LegacySensorMapping_SensorTypeEnum] = Field(alias="SensorType", default=None) # Not supported yet
    SensorIndex: Optional[int] = Field(alias="SensorIndex", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, LegacySensorMappingType=None):
        cls._subtypes_[LegacySensorMappingType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("LegacySensorMappingType")
            if data_type is None:
                raise ValueError("Missing 'LegacySensorMappingType' in LegacySensorMapping")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'LegacySensorMapping'")
            return sub(**data)
        return data


LegacySensorMapping.update_forward_refs()
