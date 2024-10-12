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



class TransducerBehaviour_TransducerBehaviourTypeEnum(str, Enum):
    FIRST_ORDER_TRANSDUCER_RESPONSE = "FirstOrderTransducerResponse"
    INSTANTANEOUS_TRANSDUCER_RESPONSE = "InstantaneousTransducerResponse"
    PASSIVE_TRANSDUCER_RESPONSE = "PassiveTransducerResponse"
    POSITION_PROPORTIONAL_INTEGRAL_DERIVIATIVE = "PositionProportionalIntegralDeriviative"
    RATE_PROPORTIONAL_INTEGRAL_DERIVIATIVE = "RateProportionalIntegralDeriviative"
    SECOND_ORDER_TRANSDUCER_RESPONSE = "SecondOrderTransducerResponse"
    USE_SETPOINT_TRAJECTORY_PLANNING = "UseSetpointTrajectoryPlanning"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TransducerBehaviour(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    TransducerBehaviourType : TransducerBehaviour_TransducerBehaviourTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - FirstOrderTransducerResponse
        - InstantaneousTransducerResponse
        - PassiveTransducerResponse
        - PositionProportionalIntegralDeriviative
        - RateProportionalIntegralDeriviative
        - SecondOrderTransducerResponse
        - UseSetpointTrajectoryPlanning
    
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/MeasuredSignalProperties/common/TransducerBehaviour.json')
    
    TransducerBehaviourType: Optional[TransducerBehaviour_TransducerBehaviourTypeEnum] = Field(alias="TransducerBehaviourType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, TransducerBehaviourType=None):
        cls._subtypes_[TransducerBehaviourType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("TransducerBehaviourType")
            if data_type is None:
                raise ValueError("Missing 'TransducerBehaviourType' in TransducerBehaviour")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'TransducerBehaviour'")
            return sub(**data)
        return data


TransducerBehaviour.update_forward_refs()
