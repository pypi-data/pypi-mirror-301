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



class BladeStabilityAnalysisModeOfOperation_BladeStabilityAnalysisModeOfOperationTypeEnum(str, Enum):
    IDLING = "Idling"
    PARKED = "Parked"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladeStabilityAnalysisModeOfOperation(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    BladeStabilityAnalysisModeOfOperationType : BladeStabilityAnalysisModeOfOperation_BladeStabilityAnalysisModeOfOperationTypeEnum, Not supported yet
        Defines the specific type of model in use.

    PitchAngle : float, default=0, Not supported yet
        The constant pitch angle used in both parked and free spin case.  This value is only used for blade stability analysis and not for model linearisation or Campbell diagram.  Blade set angle or pitch angle imbalances are ignored, and any pitch limits are not used.

    WindSpeedRange : VelocityRange

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - BladeStabilityAnalysisIdling
        - BladeStabilityAnalysisParked
    
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/BladeStabilityAnalysisModeOfOperation/common/BladeStabilityAnalysisModeOfOperation.json')
    
    BladeStabilityAnalysisModeOfOperationType: Optional[BladeStabilityAnalysisModeOfOperation_BladeStabilityAnalysisModeOfOperationTypeEnum] = Field(alias="BladeStabilityAnalysisModeOfOperationType", default=None) # Not supported yet
    PitchAngle: Optional[float] = Field(alias="PitchAngle", default=0) # Not supported yet
    WindSpeedRange: Optional[VelocityRange] = Field(alias="WindSpeedRange", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, BladeStabilityAnalysisModeOfOperationType=None):
        cls._subtypes_[BladeStabilityAnalysisModeOfOperationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("BladeStabilityAnalysisModeOfOperationType")
            if data_type is None:
                raise ValueError("Missing 'BladeStabilityAnalysisModeOfOperationType' in BladeStabilityAnalysisModeOfOperation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'BladeStabilityAnalysisModeOfOperation'")
            return sub(**data)
        return data


BladeStabilityAnalysisModeOfOperation.update_forward_refs()
