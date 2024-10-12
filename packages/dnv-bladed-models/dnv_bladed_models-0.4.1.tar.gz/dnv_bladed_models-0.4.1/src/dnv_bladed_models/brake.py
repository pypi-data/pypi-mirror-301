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



class Brake_BrakeTypeEnum(str, Enum):
    NON_LINEAR_SHAFT_BRAKE = "NonLinearShaftBrake"
    SIMPLE_SHAFT_BRAKE = "SimpleShaftBrake"

class Brake_BrakePositionEnum(str, Enum):
    LOW_SPEED_SHAFT_ROTOR_END = "LOW_SPEED_SHAFT_ROTOR_END"
    LOW_SPEED_SHAFT_GEARBOX_END = "LOW_SPEED_SHAFT_GEARBOX_END"
    HIGH_SPEED_SHAFT_GEARBOX_END = "HIGH_SPEED_SHAFT_GEARBOX_END"
    HIGH_SPEED_SHAFT_GENERATOR_END = "HIGH_SPEED_SHAFT_GENERATOR_END"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Brake(BladedModel, ABC):
    r"""
    The common properties of all brakes in the drivetrain.
    
    Attributes:
    ----------
    BrakeType : Brake_BrakeTypeEnum
        Defines the specific type of model in use.

    BrakePosition : Brake_BrakePositionEnum
        Which shaft the brake is acting on.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - NonLinearShaftBrake
        - SimpleShaftBrake
    
    """
    _relative_schema_path: str = PrivateAttr('Components/DrivetrainAndNacelle/Brake/common/Brake.json')
    
    BrakeType: Optional[Brake_BrakeTypeEnum] = Field(alias="BrakeType", default=None)
    BrakePosition: Optional[Brake_BrakePositionEnum] = Field(alias="BrakePosition", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, BrakeType=None):
        cls._subtypes_[BrakeType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("BrakeType")
            if data_type is None:
                raise ValueError("Missing 'BrakeType' in Brake")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'Brake'")
            return sub(**data)
        return data


Brake.update_forward_refs()
