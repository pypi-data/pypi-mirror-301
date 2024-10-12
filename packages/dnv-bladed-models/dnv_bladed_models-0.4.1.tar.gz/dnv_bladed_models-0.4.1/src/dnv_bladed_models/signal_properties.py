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

from dnv_bladed_models.transducer_behaviour import TransducerBehaviour



class SignalProperties_SignalQualityEnum(str, Enum):
    RAW = "Raw"
    TRANSDUCER = "Transducer"
    MEASURED = "Measured"

class SignalProperties_SignalNoiseEnum(str, Enum):
    NONE = "None"
    UNIFORM = "Uniform"
    GAUSSIAN = "Gaussian"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class SignalProperties(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    SignalQuality : SignalProperties_SignalQualityEnum, default='Raw', Not supported yet
        The representation of the signal quality - whether it has transducer lag and signal noise.

    SignalNoise : SignalProperties_SignalNoiseEnum, default='None', Not supported yet
        The type of noise on the measured signal.

    NoiseMagnitude : float, default=0, Not supported yet
        The magnitude of the signal noise.

    SamplingPeriod : float, default=0, Not supported yet
        The time step at which the input (continuous) signal is discretised at.

    DiscretisationStep : float, default=0, Not supported yet
        The intervals at which values can be represented.

    Transducer : TransducerBehaviour, abstract, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    Transducer has the following concrete types:
        - FirstOrderTransducerResponse
        - InstantaneousTransducerResponse
        - PassiveTransducerResponse
        - PositionProportionalIntegralDeriviative
        - RateProportionalIntegralDeriviative
        - SecondOrderTransducerResponse
        - UseSetpointTrajectoryPlanning
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/MeasuredSignalProperties/common/SignalProperties.json')
    
    SignalQuality: Optional[SignalProperties_SignalQualityEnum] = Field(alias="SignalQuality", default='Raw') # Not supported yet
    SignalNoise: Optional[SignalProperties_SignalNoiseEnum] = Field(alias="SignalNoise", default='None') # Not supported yet
    NoiseMagnitude: Optional[float] = Field(alias="NoiseMagnitude", default=0) # Not supported yet
    SamplingPeriod: Optional[float] = Field(alias="SamplingPeriod", default=0) # Not supported yet
    DiscretisationStep: Optional[float] = Field(alias="DiscretisationStep", default=0) # Not supported yet
    Transducer: Optional[TransducerBehaviour] = Field(alias="Transducer", default=None) # Not supported yet





SignalProperties.update_forward_refs()
