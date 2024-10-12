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



class DynamicWake_DynamicWakeTypeEnum(str, Enum):
    EQUILIBRIUM_WAKE_MODEL = "EquilibriumWakeModel"
    FREE_FLOW_MODEL = "FreeFlowModel"
    FROZEN_WAKE_MODEL = "FrozenWakeModel"
    OYE_DYNAMIC_WAKE = "OyeDynamicWake"
    PITT_AND_PETERS_MODEL = "PittAndPetersModel"

class DynamicWake_AreaAveragingMethodEnum(str, Enum):
    OVER_ANNULUS = "OVER_ANNULUS"
    NONE = "NONE"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class DynamicWake(BladedModel, ABC):
    r"""
    Common properties for all dynamic wake models.
    
    Attributes:
    ----------
    DynamicWakeType : DynamicWake_DynamicWakeTypeEnum
        Defines the specific type of model in use.

    AreaAveragingMethod : DynamicWake_AreaAveragingMethodEnum, default='OVER_ANNULUS'
        With the \"over annulus\" method, the dynamic wake is calculated over the entire annular ring.  Induced velocities are averaged over the number of blades.  If \"none\" is selected, the annulus is divided into segments to which separate dynamic wakes are applied.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - EquilibriumWakeModel
        - FreeFlowModel
        - FrozenWakeModel
        - OyeDynamicWake
        - PittAndPetersModel
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/AerodynamicModel/MomentumTheoryCorrections/DynamicWake/common/DynamicWake.json')
    
    DynamicWakeType: Optional[DynamicWake_DynamicWakeTypeEnum] = Field(alias="DynamicWakeType", default=None)
    AreaAveragingMethod: Optional[DynamicWake_AreaAveragingMethodEnum] = Field(alias="AreaAveragingMethod", default='OVER_ANNULUS')



    _subtypes_ = dict()

    def __init_subclass__(cls, DynamicWakeType=None):
        cls._subtypes_[DynamicWakeType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("DynamicWakeType")
            if data_type is None:
                raise ValueError("Missing 'DynamicWakeType' in DynamicWake")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'DynamicWake'")
            return sub(**data)
        return data


DynamicWake.update_forward_refs()
