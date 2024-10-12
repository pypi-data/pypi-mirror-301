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



class AddedInertia_AddedInertiaTypeEnum(str, Enum):
    POINT_INERTIA = "PointInertia"
    SIX_BY_SIX_INERTIA = "SixBySixInertia"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class AddedInertia(BladedModel, ABC):
    r"""
    The common properties of inertias added to the tower component.
    
    Attributes:
    ----------
    AddedInertiaType : AddedInertia_AddedInertiaTypeEnum
        Defines the specific type of model in use.

    IgnoreGravityLoads : bool, default=False
        If true, the loads due to gravity on this inertia will be ignored.

    HeightUpTower : float, default=0
        The height measured from the bottom of the tower, assuming that the tower is mounted vertically.

    SnapToNearestNode : bool
        If true, the inertias will be added to the nearest structural node, which may be at a significantly different height to that specified.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - PointInertia
        - SixBySixInertia
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Tower/AddedInertia/common/AddedInertia.json')
    
    AddedInertiaType: Optional[AddedInertia_AddedInertiaTypeEnum] = Field(alias="AddedInertiaType", default=None)
    IgnoreGravityLoads: Optional[bool] = Field(alias="IgnoreGravityLoads", default=False)
    HeightUpTower: Optional[float] = Field(alias="HeightUpTower", default=0)
    SnapToNearestNode: Optional[bool] = Field(alias="SnapToNearestNode", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, AddedInertiaType=None):
        cls._subtypes_[AddedInertiaType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("AddedInertiaType")
            if data_type is None:
                raise ValueError("Missing 'AddedInertiaType' in AddedInertia")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'AddedInertia'")
            return sub(**data)
        return data


AddedInertia.update_forward_refs()
