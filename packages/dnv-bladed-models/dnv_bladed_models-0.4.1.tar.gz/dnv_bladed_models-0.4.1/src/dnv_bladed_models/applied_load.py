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

from dnv_bladed_models.vector3_d import Vector3D



class AppliedLoad_AppliedLoadTypeEnum(str, Enum):
    BLADE_POINT_LOADING = "BladePointLoading"
    TOWER_POINT_LOADING = "TowerPointLoading"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class AppliedLoad(BladedModel, ABC):
    r"""
    The common properties of a point loading time history.
    
    Not supported yet.
    
    Attributes:
    ----------
    AppliedLoadType : AppliedLoad_AppliedLoadTypeEnum, Not supported yet
        Defines the specific type of model in use.

    StartTime : float, Not supported yet
        The time into the simulation at which to start applying the loading (excluding the lead-in time).

    LoadingFilepath : str, Not supported yet
        A filepath or URI containing one or six degree of loading data.  In the case of the six degrees of freedom, these will be applied in the component's coordinate system.  Where a single degree of freedom is provided, SingleDirectionLoading must also be specified.

    DirectionOfLoading : Vector3D

    OnComponentInAssembly : str, Not supported yet
        An assembly reference to the specific component to which to apply the force.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - BladePointLoading
        - TowerPointLoading
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/AppliedLoad/common/AppliedLoad.json')
    
    AppliedLoadType: Optional[AppliedLoad_AppliedLoadTypeEnum] = Field(alias="AppliedLoadType", default=None) # Not supported yet
    StartTime: Optional[float] = Field(alias="StartTime", default=None) # Not supported yet
    LoadingFilepath: Optional[str] = Field(alias="LoadingFilepath", default=None) # Not supported yet
    DirectionOfLoading: Optional[Vector3D] = Field(alias="DirectionOfLoading", default=None)
    OnComponentInAssembly: Optional[str] = Field(alias="OnComponentInAssembly", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, AppliedLoadType=None):
        cls._subtypes_[AppliedLoadType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("AppliedLoadType")
            if data_type is None:
                raise ValueError("Missing 'AppliedLoadType' in AppliedLoad")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'AppliedLoad'")
            return sub(**data)
        return data
    @validator("OnComponentInAssembly")
    def OnComponentInAssembly_pattern(cls, value):
        if value is not None and not re.match(r"^#\/ComponentDefinitions\/(.+)$", value):
            raise ValueError(f"OnComponentInAssembly did not match the expected format (found {value})")
        return value



AppliedLoad.update_forward_refs()
