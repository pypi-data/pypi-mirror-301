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



class Component_ComponentTypeEnum(str, Enum):
    BLADE = "Blade"
    DRIVETRAIN_AND_NACELLE = "DrivetrainAndNacelle"
    EXTERNAL_MODULE_COMPONENT = "ExternalModuleComponent"
    FIXED_SPEED_ACTIVE_DAMPER = "FixedSpeedActiveDamper"
    INDEPENDENT_PITCH_HUB = "IndependentPitchHub"
    LIDAR = "Lidar"
    LINEAR_FOUNDATION = "LinearFoundation"
    LINEAR_PASSIVE_DAMPER = "LinearPassiveDamper"
    PENDULUM_DAMPER = "PendulumDamper"
    PITCH_SYSTEM = "PitchSystem"
    ROTATION = "Rotation"
    SIMPLIFIED_LINEAR_FOUNDATION = "SimplifiedLinearFoundation"
    SUPERELEMENT = "Superelement"
    TOWER = "Tower"
    TRANSLATION = "Translation"
    VARIABLE_SPEED_ACTIVE_DAMPER = "VariableSpeedActiveDamper"
    VARIABLE_SPEED_GENERATOR = "VariableSpeedGenerator"
    YAW_SYSTEM = "YawSystem"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Component(BladedModel, ABC):
    r"""
    The common properties of all components.
    
    Attributes:
    ----------
    ComponentType : Component_ComponentTypeEnum
        Defines the specific type of model in use.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - Blade
        - DrivetrainAndNacelle
        - ExternalModuleComponent
        - FixedSpeedActiveDamper
        - IndependentPitchHub
        - Lidar
        - LinearFoundation
        - LinearPassiveDamper
        - PendulumDamper
        - PitchSystem
        - Rotation
        - SimplifiedLinearFoundation
        - Superelement
        - Tower
        - Translation
        - VariableSpeedActiveDamper
        - VariableSpeedGenerator
        - YawSystem
    
    """
    _relative_schema_path: str = PrivateAttr('Components/common/Component.json')
    
    ComponentType: Optional[Component_ComponentTypeEnum] = Field(alias="ComponentType", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, ComponentType=None):
        cls._subtypes_[ComponentType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("ComponentType")
            if data_type is None:
                raise ValueError("Missing 'ComponentType' in Component")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'Component'")
            return sub(**data)
        return data


Component.update_forward_refs()
