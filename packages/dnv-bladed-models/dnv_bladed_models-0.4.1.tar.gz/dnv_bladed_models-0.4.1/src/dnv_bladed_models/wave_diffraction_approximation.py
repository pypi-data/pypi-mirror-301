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



class WaveDiffractionApproximation_WaveDiffractionApproximationTypeEnum(str, Enum):
    AUTOMATIC_MAC_CAMY_FUCHS = "AutomaticMacCamyFuchs"
    AUTOMATIC_SIMPLE_CUTOFF_FREQUENCY = "AutomaticSimpleCutoffFrequency"
    MAC_CAMY_FUCHS = "MacCamyFuchs"
    SIMPLE_CUTOFF_FREQUENCY = "SimpleCutoffFrequency"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class WaveDiffractionApproximation(BladedModel, ABC):
    r"""
    The method used for wave diffraction approximation and the option for parameters to be auto-defined.
    
    Not supported yet.
    
    Attributes:
    ----------
    WaveDiffractionApproximationType : WaveDiffractionApproximation_WaveDiffractionApproximationTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - AutomaticMacCamyFuchs
        - AutomaticSimpleCutoffFrequency
        - MacCamyFuchs
        - SimpleCutoffFrequency
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Waves/WaveDiffractionApproximation/common/WaveDiffractionApproximation.json')
    
    WaveDiffractionApproximationType: Optional[WaveDiffractionApproximation_WaveDiffractionApproximationTypeEnum] = Field(alias="WaveDiffractionApproximationType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, WaveDiffractionApproximationType=None):
        cls._subtypes_[WaveDiffractionApproximationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("WaveDiffractionApproximationType")
            if data_type is None:
                raise ValueError("Missing 'WaveDiffractionApproximationType' in WaveDiffractionApproximation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'WaveDiffractionApproximation'")
            return sub(**data)
        return data


WaveDiffractionApproximation.update_forward_refs()
