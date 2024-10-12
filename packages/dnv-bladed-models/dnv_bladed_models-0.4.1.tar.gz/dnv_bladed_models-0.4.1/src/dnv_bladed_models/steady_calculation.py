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



class SteadyCalculation_SteadyCalculationTypeEnum(str, Enum):
    AERODYNAMIC_INFORMATION = "AerodynamicInformation"
    BLADE_STABILITY_ANALYSIS = "BladeStabilityAnalysis"
    CAMPBELL_DIAGRAM = "CampbellDiagram"
    MODEL_LINEARISATION = "ModelLinearisation"
    PERFORMANCE_COEFFICIENTS = "PerformanceCoefficients"
    STEADY_OPERATIONAL_LOADS = "SteadyOperationalLoads"
    STEADY_PARKED_LOADS = "SteadyParkedLoads"
    STEADY_POWER_CURVE = "SteadyPowerCurve"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class SteadyCalculation(BladedModel, ABC):
    r"""
    The common properties of the steady calculations in Bladed.
    
    Attributes:
    ----------
    SteadyCalculationType : SteadyCalculation_SteadyCalculationTypeEnum
        Defines the specific type of model in use.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - AerodynamicInformationCalculation
        - BladeStabilityAnalysis
        - CampbellDiagram
        - ModelLinearisation
        - PerformanceCoefficientsCalculation
        - SteadyOperationalLoadsCalculation
        - SteadyParkedLoadsCalculation
        - SteadyPowerCurveCalculation
    
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/common/SteadyCalculation.json')
    
    SteadyCalculationType: Optional[SteadyCalculation_SteadyCalculationTypeEnum] = Field(alias="SteadyCalculationType", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, SteadyCalculationType=None):
        cls._subtypes_[SteadyCalculationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("SteadyCalculationType")
            if data_type is None:
                raise ValueError("Missing 'SteadyCalculationType' in SteadyCalculation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'SteadyCalculation'")
            return sub(**data)
        return data


SteadyCalculation.update_forward_refs()
