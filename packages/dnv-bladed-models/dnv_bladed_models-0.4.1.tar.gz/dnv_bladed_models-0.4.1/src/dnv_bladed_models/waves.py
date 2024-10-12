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



class Waves_WavesTypeEnum(str, Enum):
    JONSWAP_PIERSON_MOSKOWITZ = "JonswapPiersonMoskowitz"
    LINEAR_AIRY = "LinearAiry"
    STREAM_FUNCTION = "StreamFunction"
    USER_DEFINED = "UserDefined"
    WAVE_SPECTRUM = "WaveSpectrum"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Waves(BladedModel, ABC):
    r"""
    The definition of a wave field to apply to this analysis
    
    Not supported yet.
    
    Attributes:
    ----------
    WavesType : Waves_WavesTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - JonswapPiersonMoskowitz
        - LinearAiry
        - StreamFunction
        - UserDefinedWaves
        - WaveSpectrum
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Waves/common/Waves.json')
    
    WavesType: Optional[Waves_WavesTypeEnum] = Field(alias="WavesType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, WavesType=None):
        cls._subtypes_[WavesType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("WavesType")
            if data_type is None:
                raise ValueError("Missing 'WavesType' in Waves")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'Waves'")
            return sub(**data)
        return data


Waves.update_forward_refs()
