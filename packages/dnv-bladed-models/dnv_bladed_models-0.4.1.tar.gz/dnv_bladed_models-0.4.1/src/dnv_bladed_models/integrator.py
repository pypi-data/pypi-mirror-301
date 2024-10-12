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



class Integrator_IntegratorTypeEnum(str, Enum):
    EXPLICIT_NEWMARK_BETA_FIXED_STEP = "ExplicitNewmarkBetaFixedStep"
    GENERALISED_ALPHA_FIXED_STEP = "GeneralisedAlphaFixedStep"
    IMPLICIT_NEWMARK_BETA_FIXED_STEP = "ImplicitNewmarkBetaFixedStep"
    MIDPOINT_METHOD_FIXED_STEP = "MidpointMethodFixedStep"
    RUNGE_KUTTA4TH_ORDER_FIXED_STEP = "RungeKutta4thOrderFixedStep"
    RUNGE_KUTTA_VARIABLE_STEP = "RungeKuttaVariableStep"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Integrator(BladedModel, ABC):
    r"""
    Settings for the integrator.
    
    Not supported yet.
    
    Attributes:
    ----------
    IntegratorType : Integrator_IntegratorTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - ExplicitNewmarkBetaFixedStep
        - GeneralisedAlphaFixedStep
        - ImplicitNewmarkBetaFixedStep
        - MidpointMethodFixedStep
        - RungeKutta4thOrderFixedStep
        - RungeKuttaVariableStep
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/Integrator/common/Integrator.json')
    
    IntegratorType: Optional[Integrator_IntegratorTypeEnum] = Field(alias="IntegratorType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, IntegratorType=None):
        cls._subtypes_[IntegratorType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("IntegratorType")
            if data_type is None:
                raise ValueError("Missing 'IntegratorType' in Integrator")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'Integrator'")
            return sub(**data)
        return data


Integrator.update_forward_refs()
