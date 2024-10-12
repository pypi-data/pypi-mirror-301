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



class Event_EventTypeEnum(str, Enum):
    CONTROLLER_FAULT = "ControllerFault"
    EMERGENCY_STOP_OPERATION = "EmergencyStopOperation"
    GRID_LOSS = "GridLoss"
    NETWORK_FREQUENCY_DISTURBANCE = "NetworkFrequencyDisturbance"
    NETWORK_VOLTAGE_DISTURBANCE = "NetworkVoltageDisturbance"
    NORMAL_STOP_OPERATION = "NormalStopOperation"
    PERMANENTLY_STUCK_PITCH_SYSTEM = "PermanentlyStuckPitchSystem"
    PITCH_FAULT_CONSTANT_RATE = "PitchFaultConstantRate"
    PITCH_FAULT_CONSTANT_TORQUE = "PitchFaultConstantTorque"
    PITCH_FAULT_LIMP = "PitchFaultLimp"
    PITCH_FAULT_SEIZURE = "PitchFaultSeizure"
    PITCH_FAULT_SEIZURE_AT_ANGLE = "PitchFaultSeizureAtAngle"
    SHORT_CIRCUIT = "ShortCircuit"
    START_UP_OPERATION = "StartUpOperation"
    YAW_FAULT_CONSTANT_RATE = "YawFaultConstantRate"
    YAW_FAULT_CONSTANT_TORQUE = "YawFaultConstantTorque"
    YAW_FAULT_LIMP = "YawFaultLimp"
    YAW_MANOEVER = "YawManoever"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Event(BladedModel, ABC):
    r"""
    An event which may occur during the simulation.  These can either be timed events, or based on a set of conditions which may or may not occur.
    
    Not supported yet.
    
    Attributes:
    ----------
    EventType : Event_EventTypeEnum, Not supported yet
        Defines the specific type of model in use.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    This class is an abstraction, with the following concrete implementations:
        - ControllerFault
        - EmergencyStopOperation
        - GridLoss
        - NetworkFrequencyDisturbance
        - NetworkVoltageDisturbance
        - NormalStopOperation
        - PermanentlyStuckPitchSystem
        - PitchFaultConstantRate
        - PitchFaultConstantTorque
        - PitchFaultLimp
        - PitchFaultSeizure
        - PitchFaultSeizureAtAngle
        - ShortCircuit
        - StartUpOperation
        - YawFaultConstantRate
        - YawFaultConstantTorque
        - YawFaultLimp
        - YawManoever
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Event/common/Event.json')
    
    EventType: Optional[Event_EventTypeEnum] = Field(alias="EventType", default=None) # Not supported yet



    _subtypes_ = dict()

    def __init_subclass__(cls, EventType=None):
        cls._subtypes_[EventType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("EventType")
            if data_type is None:
                raise ValueError("Missing 'EventType' in Event")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'Event'")
            return sub(**data)
        return data


Event.update_forward_refs()
