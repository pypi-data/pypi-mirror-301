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



class PitchActuator_ActuatorDriveTypeEnum(str, Enum):
    IDEALISED_ACTUATOR = "IdealisedActuator"
    LINEAR_ACTUATOR = "LinearActuator"
    ROTARY_DRIVE = "RotaryDrive"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class PitchActuator(BladedModel, ABC):
    r"""
    The common properties of an pitch system&#39;s actuation mechanism.
    
    Attributes:
    ----------
    ActuatorDriveType : PitchActuator_ActuatorDriveTypeEnum
        Defines the specific type of model in use.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - IdealisedPitchActuator
        - LinearPitchActuator
        - PitchSystemRotaryDrive
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchActuator/common/PitchActuator.json')
    
    ActuatorDriveType: Optional[PitchActuator_ActuatorDriveTypeEnum] = Field(alias="ActuatorDriveType", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, ActuatorDriveType=None):
        cls._subtypes_[ActuatorDriveType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("ActuatorDriveType")
            if data_type is None:
                raise ValueError("Missing 'ActuatorDriveType' in PitchActuator")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'PitchActuator'")
            return sub(**data)
        return data


PitchActuator.update_forward_refs()
