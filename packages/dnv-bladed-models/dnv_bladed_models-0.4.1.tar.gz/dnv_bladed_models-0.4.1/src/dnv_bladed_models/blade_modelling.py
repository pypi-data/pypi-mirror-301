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



class BladeModelling_BladeModellingTypeEnum(str, Enum):
    FINITE_ELEMENT_BLADE_MODELLING = "FiniteElementBladeModelling"
    MODAL_BLADE_MODELLING = "ModalBladeModelling"
    RIGID_BLADE_MODELLING = "RigidBladeModelling"

class BladeModelling_GeometricStiffnessModelEnum(str, Enum):
    AXIAL_LOADS_ONLY = "AxialLoadsOnly"
    FULL_MODEL_WITH_ORIENTATION_CORRECTION = "FullModelWithOrientationCorrection"
    INTERNAL_LOADS_ONLY = "InternalLoadsOnly"
    DISABLED = "Disabled"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladeModelling(BladedModel, ABC):
    r"""
    Common properties for all blade modelling methods.
    
    Attributes:
    ----------
    BladeModellingType : BladeModelling_BladeModellingTypeEnum
        Defines the specific type of model in use.

    GeometricStiffnessModel : BladeModelling_GeometricStiffnessModelEnum, default='AxialLoadsOnly'
        The geometric stiffness model to use for the blades. For blades with 1 part, the \"axial loads only\" model is recommended. This configuration is only appropriate for relatively stiff blades, undergoing small deflection.  For more flexible blade models, a multi-part blade model is more appropriate. In this case, the \"full with orientation correction\" is the recommended option, as long as deflection remains small within each blade part.

    IgnoreAxesOrientationDifferencesForShear : bool, default=False
        With this option selected, the effect of orientation difference between the neutral axis and shear axis on the blade elements are not taken into account. Please refer to the Bladed documentation \"Bend-twist coupling in Bladed beam elements\" doc No. 110052-UKBR-T-30 for further information.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - FiniteElementBladeModelling
        - ModalBladeModelling
        - RigidBladeModelling
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeModelling/common/BladeModelling.json')
    
    BladeModellingType: Optional[BladeModelling_BladeModellingTypeEnum] = Field(alias="BladeModellingType", default=None)
    GeometricStiffnessModel: Optional[BladeModelling_GeometricStiffnessModelEnum] = Field(alias="GeometricStiffnessModel", default='AxialLoadsOnly')
    IgnoreAxesOrientationDifferencesForShear: Optional[bool] = Field(alias="IgnoreAxesOrientationDifferencesForShear", default=False)



    _subtypes_ = dict()

    def __init_subclass__(cls, BladeModellingType=None):
        cls._subtypes_[BladeModellingType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("BladeModellingType")
            if data_type is None:
                raise ValueError("Missing 'BladeModellingType' in BladeModelling")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'BladeModelling'")
            return sub(**data)
        return data


BladeModelling.update_forward_refs()
