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



class BladeOutputsForLocation_BladeOutputsForLocationTypeEnum(str, Enum):
    OUTPUTS_FOR_POSITION = "OutputsForPosition"
    OUTPUTS_FOR_SECTION = "OutputsForSection"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladeOutputsForLocation(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    BladeOutputsForLocationType : BladeOutputsForLocation_BladeOutputsForLocationTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Loads : bool, default=False, Not supported yet
        An array of blade station indices to output loads for (exclusive with BLOADS_POS).

    Motion : bool, default=False, Not supported yet
        An array of blade station indices to output deflections for (exclusive with BDEFLS_POS).

    Aerodynamics : bool, Not supported yet
        Whether to output loads on this node

    Hydrodynamics : bool, default=False, Not supported yet
        An array of blade radii to output water kinematics for (tidal only).

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - BladeOutputsForPosition
        - BladeOutputsForSection
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeOutputGroupLibrary/BladeOutputGroup/BladeOutputsForLocation/common/BladeOutputsForLocation.json')
    
    BladeOutputsForLocationType: Optional[BladeOutputsForLocation_BladeOutputsForLocationTypeEnum] = Field(alias="BladeOutputsForLocationType", default=None) # Not supported yet
    Loads: Optional[bool] = Field(alias="Loads", default=False) # Not supported yet
    Motion: Optional[bool] = Field(alias="Motion", default=False) # Not supported yet
    Aerodynamics: Optional[bool] = Field(alias="Aerodynamics", default=None) # Not supported yet
    Hydrodynamics: Optional[bool] = Field(alias="Hydrodynamics", default=False) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, BladeOutputsForLocationType=None):
        cls._subtypes_[BladeOutputsForLocationType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("BladeOutputsForLocationType")
            if data_type is None:
                raise ValueError("Missing 'BladeOutputsForLocationType' in BladeOutputsForLocation")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'BladeOutputsForLocation'")
            return sub(**data)
        return data


BladeOutputsForLocation.update_forward_refs()
