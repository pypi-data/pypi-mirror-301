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



class TransducerFaults_FaultTypeEnum(str, Enum):
    NONE = "None"
    NOISE = "Noise"
    TO_CONSTANT = "ToConstant"
    CONSTANT_OFFSET = "ConstantOffset"
    GROWING_OFFSET = "GrowingOffset"
    HARMONIC_OFFSET = "HarmonicOffset"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TransducerFaults(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    ApplyOnlyToFirst : bool, default=True, Not supported yet
        If true, the fault will be aplied only to the first instance of this transducer.  If false, all sensors of this type will fail identically.

    MiscalibrationOffset : float, default=0, Not supported yet
        A constant value added to the sensor's output - for example, if the sensor had been incorrectly installed or poorly calibrated.

    InverseInstallation : bool, default=False, Not supported yet
        Whether the sensor was installed in reverse, resulting in its outputs being multiplied by -1.0.

    FailTime : float, default=0, Not supported yet
        The time at which any time-dependent failure occurs.  This will be from the beginning of the simulation, and not from the start of logging.  Please ensure that this time will equate to a period which is being clearly logged.

    FaultType : TransducerFaults_FaultTypeEnum, default='None', Not supported yet
        What fault occurs at a specified time in the simulation.

    NoiseMultiplier : float, default=1, Not supported yet
        The factor by which the noise on the signal increases (or decreases) by.

    FailureValue : float, default=0, Not supported yet
        The value which the sensor reverts to in the case of failure.

    FailureValueRampRate : float, default=0, Not supported yet
        The rate at which the signal reverts to its fail value.  A rate of 0.0 represents an instantaneous step change to the fail value.

    ConstantOffset : float, default=0, Not supported yet
        The value by which the signal is offset by.

    GrowingOffset : float, default=0, Not supported yet
        The rate at which the signal is deviating from its calibrated value.

    Magnitude : float, default=0, Not supported yet
        The greatest magnitude of the harmonic interference from the 'true' value.

    Period : float, default=1, Not supported yet
        The time period of the full sinusoidal interference pattern.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/MeasuredSignalProperties/common/TransducerFaults.json')
    
    ApplyOnlyToFirst: Optional[bool] = Field(alias="ApplyOnlyToFirst", default=True) # Not supported yet
    MiscalibrationOffset: Optional[float] = Field(alias="MiscalibrationOffset", default=0) # Not supported yet
    InverseInstallation: Optional[bool] = Field(alias="InverseInstallation", default=False) # Not supported yet
    FailTime: Optional[float] = Field(alias="FailTime", default=0) # Not supported yet
    FaultType: Optional[TransducerFaults_FaultTypeEnum] = Field(alias="FaultType", default='None') # Not supported yet
    NoiseMultiplier: Optional[float] = Field(alias="NoiseMultiplier", default=1) # Not supported yet
    FailureValue: Optional[float] = Field(alias="FailureValue", default=0) # Not supported yet
    FailureValueRampRate: Optional[float] = Field(alias="FailureValueRampRate", default=0) # Not supported yet
    ConstantOffset: Optional[float] = Field(alias="ConstantOffset", default=0) # Not supported yet
    GrowingOffset: Optional[float] = Field(alias="GrowingOffset", default=0) # Not supported yet
    Magnitude: Optional[float] = Field(alias="Magnitude", default=0) # Not supported yet
    Period: Optional[float] = Field(alias="Period", default=1) # Not supported yet





TransducerFaults.update_forward_refs()
