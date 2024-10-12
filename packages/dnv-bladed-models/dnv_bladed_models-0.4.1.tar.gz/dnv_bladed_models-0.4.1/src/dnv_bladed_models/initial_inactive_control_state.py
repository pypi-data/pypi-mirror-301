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

from dnv_bladed_models.initial_control_state import InitialControlState



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class InitialInactiveControlState(InitialControlState, ABC):
    r"""
    Base class for all initial control states.
    
    Not supported yet.
    
    Attributes:
    ----------
    IsControllerActive : bool, Not supported yet
        If true, the controller is active and can change the state of the turbine.

    PitchAngle : float, Not supported yet
        The pitch angle of all the blades of an idling or parked turbine.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/InitialCondition/common/InitialInactiveControlState.json')
    
    IsControllerActive: Optional[bool] = Field(alias="IsControllerActive", default=None) # Not supported yet
    PitchAngle: Optional[float] = Field(alias="PitchAngle", default=None) # Not supported yet





InitialInactiveControlState.update_forward_refs()
