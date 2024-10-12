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



class LidarFocalDistanceControl_FocalDistanceControlTypeEnum(str, Enum):
    CONTROLLER = "Controller"
    MULTIPLE_FOCAL_DISTANCES = "MultipleFocalDistances"
    SINGLE_FOCAL_DISTANCE = "SingleFocalDistance"

class LidarFocalDistanceControl_FocussingModeEnum(str, Enum):
    PULSED = "Pulsed"
    CONTINUOUS = "Continuous"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class LidarFocalDistanceControl(BladedModel, ABC):
    r"""
    The common properties of the different focal distance control methods.
    
    Not supported yet.
    
    Attributes:
    ----------
    FocalDistanceControlType : LidarFocalDistanceControl_FocalDistanceControlTypeEnum, Not supported yet
        Defines the specific type of model in use.

    FocussingMode : LidarFocalDistanceControl_FocussingModeEnum, Not supported yet
        The focussing mode of the Lidar beam.  Continuous beam that focuses at single point or pulsed beam measures velocities at multiple distances

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - ControllerLidarSettings
        - MultipleLidarFocalDistances
        - SingleLidarFocalDistance
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Lidar/LidarFocalDistanceControl/common/LidarFocalDistanceControl.json')
    
    FocalDistanceControlType: Optional[LidarFocalDistanceControl_FocalDistanceControlTypeEnum] = Field(alias="FocalDistanceControlType", default=None) # Not supported yet
    FocussingMode: Optional[LidarFocalDistanceControl_FocussingModeEnum] = Field(alias="FocussingMode", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, FocalDistanceControlType=None):
        cls._subtypes_[FocalDistanceControlType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("FocalDistanceControlType")
            if data_type is None:
                raise ValueError("Missing 'FocalDistanceControlType' in LidarFocalDistanceControl")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'LidarFocalDistanceControl'")
            return sub(**data)
        return data


LidarFocalDistanceControl.update_forward_refs()
