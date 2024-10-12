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



class TowerSensor_TowerSensorTypeEnum(str, Enum):
    ACCELEROMETER = "Accelerometer"
    INCLINOMETER = "Inclinometer"
    STRAIN_GAUGE = "StrainGauge"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TowerSensor(BladedModel, ABC):
    r"""
    The common properties for all tower sensors.
    
    Not supported yet.
    
    Attributes:
    ----------
    TowerSensorType : TowerSensor_TowerSensorTypeEnum, Not supported yet
        Defines the specific type of model in use.

    HeightUpTower : float, Not supported yet
        The height measured from the bottom of the tower, assuming that the tower is mounted vertically.

    SnapToNearestNode : bool, Not supported yet
        If true, the sensorwill be placed at the nearest structural node, which may be at a significantly different height to that specified.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - TowerAccelerometer
        - TowerInclinometer
        - TowerStrainGauge
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Tower/TowerSensors/TowerSensor/common/TowerSensor.json')
    
    TowerSensorType: Optional[TowerSensor_TowerSensorTypeEnum] = Field(alias="TowerSensorType", default=None) # Not supported yet
    HeightUpTower: Optional[float] = Field(alias="HeightUpTower", default=None) # Not supported yet
    SnapToNearestNode: Optional[bool] = Field(alias="SnapToNearestNode", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, TowerSensorType=None):
        cls._subtypes_[TowerSensorType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("TowerSensorType")
            if data_type is None:
                raise ValueError("Missing 'TowerSensorType' in TowerSensor")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'TowerSensor'")
            return sub(**data)
        return data


TowerSensor.update_forward_refs()
