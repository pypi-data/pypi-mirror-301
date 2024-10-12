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



class ActuatorResponse_ActuatorResponseTypeEnum(str, Enum):
    FIRST_ORDER_ACTUATOR_RESPONSE = "FirstOrderActuatorResponse"
    INSTANTANEOUS_ACTUATOR_RESPONSE = "InstantaneousActuatorResponse"
    SECOND_ORDER_ACTUATOR_RESPONSE = "SecondOrderActuatorResponse"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ActuatorResponse(BladedModel, ABC):
    r"""
    The common properties of all control responses.
    
    Attributes:
    ----------
    ActuatorResponseType : ActuatorResponse_ActuatorResponseTypeEnum
        Defines the specific type of model in use.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - FirstOrderActuatorResponse
        - InstantaneousActuatorResponse
        - SecondOrderActuatorResponse
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchActuator/ActuatorResponse/common/ActuatorResponse.json')
    
    ActuatorResponseType: Optional[ActuatorResponse_ActuatorResponseTypeEnum] = Field(alias="ActuatorResponseType", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, ActuatorResponseType=None):
        cls._subtypes_[ActuatorResponseType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("ActuatorResponseType")
            if data_type is None:
                raise ValueError("Missing 'ActuatorResponseType' in ActuatorResponse")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'ActuatorResponse'")
            return sub(**data)
        return data


ActuatorResponse.update_forward_refs()
