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

from dnv_bladed_models.response_to_demand import ResponseToDemand



class PitchSystemDemand_PitchSystemDemandTypeEnum(str, Enum):
    POSITION = "Position"
    RATE = "Rate"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class PitchSystemDemand(BladedModel, ABC):
    r"""
    The common properties of the pitch and rate demand responses.
    
    Attributes:
    ----------
    PitchSystemDemandType : PitchSystemDemand_PitchSystemDemandTypeEnum
        Defines the specific type of model in use.

    ResponseToDemand : ResponseToDemand, abstract

    Notes:
    -----
    ResponseToDemand has the following concrete types:
        - FirstOrderResponse
        - ImmediateResponse
        - ProportionalIntegralDeriviative
        - SecondOrderResponse
    
    This class is an abstraction, with the following concrete implementations:
        - PitchPositionDemand
        - PitchRateDemand
    
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchController/PitchSystemDemand/common/PitchSystemDemand.json')
    
    PitchSystemDemandType: Optional[PitchSystemDemand_PitchSystemDemandTypeEnum] = Field(alias="PitchSystemDemandType", default=None)
    ResponseToDemand: Optional[ResponseToDemand] = Field(alias="ResponseToDemand", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, PitchSystemDemandType=None):
        cls._subtypes_[PitchSystemDemandType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("PitchSystemDemandType")
            if data_type is None:
                raise ValueError("Missing 'PitchSystemDemandType' in PitchSystemDemand")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'PitchSystemDemand'")
            return sub(**data)
        return data


PitchSystemDemand.update_forward_refs()
