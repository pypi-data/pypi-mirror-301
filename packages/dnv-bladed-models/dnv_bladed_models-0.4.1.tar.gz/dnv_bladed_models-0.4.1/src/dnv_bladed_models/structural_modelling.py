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



class StructuralModelling_StructuralModellingTypeEnum(str, Enum):
    MODAL_STRUCTURAL_MODELLING = "ModalStructuralModelling"
    RIGID_STRUCTURAL_MODELLING = "RigidStructuralModelling"

class StructuralModelling_GeometricStiffnessModelEnum(str, Enum):
    AXIAL_LOADS_ONLY = "AxialLoadsOnly"
    INTERNAL_LOADS_ONLY = "InternalLoadsOnly"
    DISABLED = "Disabled"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class StructuralModelling(BladedModel, ABC):
    r"""
    The modelling options for a component with flexibility.  This is primarily the blade and the support structure.
    
    Attributes:
    ----------
    StructuralModellingType : StructuralModelling_StructuralModellingTypeEnum
        Defines the specific type of model in use.

    MaximumNodeSpacing : float
        The maximum node spacing allowed on the component.  If any two nodes are further spaced apart than this, an additional node or nodes will be added inbetween them.  If omite, no additional nodes will be added.

    GeometricStiffnessModel : StructuralModelling_GeometricStiffnessModelEnum, default='AxialLoadsOnly'
        The geometric stiffness model to use for the support structure

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - ModalStructuralModelling
        - RigidStructuralModelling
    
    """
    _relative_schema_path: str = PrivateAttr('Components/StructuralModelling/common/StructuralModelling.json')
    
    StructuralModellingType: Optional[StructuralModelling_StructuralModellingTypeEnum] = Field(alias="StructuralModellingType", default=None)
    MaximumNodeSpacing: Optional[float] = Field(alias="MaximumNodeSpacing", default=None)
    GeometricStiffnessModel: Optional[StructuralModelling_GeometricStiffnessModelEnum] = Field(alias="GeometricStiffnessModel", default='AxialLoadsOnly')



    _subtypes_ = dict()

    def __init_subclass__(cls, StructuralModellingType=None):
        cls._subtypes_[StructuralModellingType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("StructuralModellingType")
            if data_type is None:
                raise ValueError("Missing 'StructuralModellingType' in StructuralModelling")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'StructuralModelling'")
            return sub(**data)
        return data


StructuralModelling.update_forward_refs()
