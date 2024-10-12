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

from dnv_bladed_models.pitch_acceleration_limits import PitchAccelerationLimits

from dnv_bladed_models.pitch_rate_limits import PitchRateLimits



class ResponseToDemand_ResponseToDemandTypeEnum(str, Enum):
    FIRST_ORDER_RESPONSE = "FirstOrderResponse"
    IMMEDIATE_RESPONSE = "ImmediateResponse"
    PROPORTIONAL_INTEGRAL_DERIVIATIVE = "ProportionalIntegralDeriviative"
    SECOND_ORDER_RESPONSE = "SecondOrderResponse"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ResponseToDemand(BladedModel, ABC):
    r"""
    The common properties of all control responses.
    
    Attributes:
    ----------
    ResponseToDemandType : ResponseToDemand_ResponseToDemandTypeEnum
        Defines the specific type of model in use.

    RateLimits : PitchRateLimits

    AccelerationLimits : PitchAccelerationLimits

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - FirstOrderResponse
        - ImmediateResponse
        - ProportionalIntegralDeriviative
        - SecondOrderResponse
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchController/PitchSystemDemand/ResponseToDemand/common/ResponseToDemand.json')
    
    ResponseToDemandType: Optional[ResponseToDemand_ResponseToDemandTypeEnum] = Field(alias="ResponseToDemandType", default=None)
    RateLimits: Optional[PitchRateLimits] = Field(alias="RateLimits", default=None)
    AccelerationLimits: Optional[PitchAccelerationLimits] = Field(alias="AccelerationLimits", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, ResponseToDemandType=None):
        cls._subtypes_[ResponseToDemandType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("ResponseToDemandType")
            if data_type is None:
                raise ValueError("Missing 'ResponseToDemandType' in ResponseToDemand")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'ResponseToDemand'")
            return sub(**data)
        return data


ResponseToDemand.update_forward_refs()
