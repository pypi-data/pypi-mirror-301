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

from dnv_bladed_models.tower_can_modelling import TowerCanModelling



class TowerCan_TowerCanTypeEnum(str, Enum):
    EXPLICIT_TOWER_CAN = "ExplicitTowerCan"
    SIMPLE_TOWER_CAN = "SimpleTowerCan"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TowerCan(BladedModel, ABC):
    r"""
    The common properties for a single can in the tower
    
    Attributes:
    ----------
    TowerCanType : TowerCan_TowerCanTypeEnum
        Defines the specific type of model in use.

    Modelling : TowerCanModelling, Not supported yet

    CanHeight : float
        The height of the tower can, assuming that it is mounted vertically.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - ExplicitTowerCan
        - SimpleTowerCan
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Tower/TowerCan/common/TowerCan.json')
    
    TowerCanType: Optional[TowerCan_TowerCanTypeEnum] = Field(alias="TowerCanType", default=None)
    Modelling: Optional[TowerCanModelling] = Field(alias="Modelling", default=None) # Not supported yet
    CanHeight: Optional[float] = Field(alias="CanHeight", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, TowerCanType=None):
        cls._subtypes_[TowerCanType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("TowerCanType")
            if data_type is None:
                raise ValueError("Missing 'TowerCanType' in TowerCan")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'TowerCan'")
            return sub(**data)
        return data


TowerCan.update_forward_refs()
