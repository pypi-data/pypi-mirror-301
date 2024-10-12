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

from dnv_bladed_models.velocity_range import VelocityRange



class CampbellDiagramModeOfOperation_CampbellDiagramModeOfOperationTypeEnum(str, Enum):
    IDLING = "Idling"
    PARKED = "Parked"
    POWER_PRODUCTION = "PowerProduction"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class CampbellDiagramModeOfOperation(BladedModel, ABC):
    r"""
    The common properties of the operating mode of a Campbell diagram calculation.
    
    Not supported yet.
    
    Attributes:
    ----------
    CampbellDiagramModeOfOperationType : CampbellDiagramModeOfOperation_CampbellDiagramModeOfOperationTypeEnum, Not supported yet
        Defines the specific type of model in use.

    WindSpeedRange : VelocityRange

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - CampbellIdling
        - CampbellParked
        - CampbellPowerProduction
    
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/CampbellDiagramModeOfOperation/common/CampbellDiagramModeOfOperation.json')
    
    CampbellDiagramModeOfOperationType: Optional[CampbellDiagramModeOfOperation_CampbellDiagramModeOfOperationTypeEnum] = Field(alias="CampbellDiagramModeOfOperationType", default=None) # Not supported yet
    WindSpeedRange: Optional[VelocityRange] = Field(alias="WindSpeedRange", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, CampbellDiagramModeOfOperationType=None):
        cls._subtypes_[CampbellDiagramModeOfOperationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("CampbellDiagramModeOfOperationType")
            if data_type is None:
                raise ValueError("Missing 'CampbellDiagramModeOfOperationType' in CampbellDiagramModeOfOperation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'CampbellDiagramModeOfOperation'")
            return sub(**data)
        return data


CampbellDiagramModeOfOperation.update_forward_refs()
