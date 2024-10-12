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



class InitialCondition_InitialConditionTypeEnum(str, Enum):
    GL2010_ICING = "GL2010Icing"
    IEC4_ICING = "IEC4Icing"
    INITIAL_AZIMUTH_POSITION = "InitialAzimuthPosition"
    INITIAL_FLOATING_POSITION = "InitialFloatingPosition"
    INITIAL_PITCH_POSITION = "InitialPitchPosition"
    INITIAL_ROTOR_SPEED = "InitialRotorSpeed"
    INITIAL_YAW_ANGLE = "InitialYawAngle"
    ROTOR_IDLING = "RotorIdling"
    ROTOR_IN_POWER_PRODUCTION = "RotorInPowerProduction"
    ROTOR_PARKED = "RotorParked"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class InitialCondition(BladedModel, ABC):
    r"""
    A condition of the turbine or a component at the beginning of the simulation.  This may change during the simulation.
    
    Not supported yet.
    
    Attributes:
    ----------
    InitialConditionType : InitialCondition_InitialConditionTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - GL2010Icing
        - IEC4Icing
        - InitialAzimuthPosition
        - InitialFloatingPosition
        - InitialPitchPosition
        - InitialRotorSpeed
        - InitialYawAngle
        - RotorIdlingControlState
        - RotorInPowerProduction
        - RotorParkedControlState
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/InitialCondition/common/InitialCondition.json')
    
    InitialConditionType: Optional[InitialCondition_InitialConditionTypeEnum] = Field(alias="InitialConditionType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, InitialConditionType=None):
        cls._subtypes_[InitialConditionType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("InitialConditionType")
            if data_type is None:
                raise ValueError("Missing 'InitialConditionType' in InitialCondition")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'InitialCondition'")
            return sub(**data)
        return data


InitialCondition.update_forward_refs()
