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

from dnv_bladed_models.dynamic_stall import DynamicStall



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BeddoesLeishmanModel(DynamicStall, ABC):
    r"""
    The common properties for the Beddoes Leishman dynamic stall models.
    
    Attributes:
    ----------
    UseKirchoffFlow : bool, default=False
        If true,the normal force coefficient is computed using the dynamic separation position in Kirchoff's equation directly.  If false, the dynamic separation position is used to linearly interpolate between fully separated and fully attached flow. In normal operating conditions this setting will not lead to significant differences, but it has been found that in parked/idling cases (where the blade experiences high angles of attack) this option will improve the aerodynamic damping of the blade. The explanation for the damping differences is given in the aerodynamic validation document on the User Portal.

    UseImpulsiveContributions : bool, default=False
        Enabling the impulsive contributions in lift and moment coefficient.

    PressureLagTimeConstant : float, default=1.7
        The lag between the pressure and the lift.

    VortexLiftTimeConstant : float, default=6
        The rate of decay of the vortex induced lift that is generated when airfoils undergo a rapid change in angle of attack towards positive or negative stall.

    VortexTravelTimeConstant : float, default=7.5
        The time constant that controls the duration of the vortex induced lift that is generated when airfoils undergo a rapid change in angle of attack towards positive or negative stall.

    AttachedFlowConstantA1 : float, default=0.165
        The constant A1 for the Beddoes-Leishman type dynamic stall model to control the attached flow states.

    AttachedFlowConstantA2 : float, default=0.335
        The constant A2 for the Beddoes-Leishman type dynamic stall model to control the attached flow states.

    AttachedFlowConstantB1 : float, default=0.0455
        The constant B1 for the Beddoes-Leishman type dynamic stall model to control the attached flow states.

    AttachedFlowConstantB2 : float, default=0.3
        The constant B2 for the Beddoes-Leishman type dynamic stall model to control the attached flow states.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/DynamicStall/common/BeddoesLeishmanModel.json')
    
    UseKirchoffFlow: Optional[bool] = Field(alias="UseKirchoffFlow", default=False)
    UseImpulsiveContributions: Optional[bool] = Field(alias="UseImpulsiveContributions", default=False)
    PressureLagTimeConstant: Optional[float] = Field(alias="PressureLagTimeConstant", default=1.7)
    VortexLiftTimeConstant: Optional[float] = Field(alias="VortexLiftTimeConstant", default=6)
    VortexTravelTimeConstant: Optional[float] = Field(alias="VortexTravelTimeConstant", default=7.5)
    AttachedFlowConstantA1: Optional[float] = Field(alias="AttachedFlowConstantA1", default=0.165)
    AttachedFlowConstantA2: Optional[float] = Field(alias="AttachedFlowConstantA2", default=0.335)
    AttachedFlowConstantB1: Optional[float] = Field(alias="AttachedFlowConstantB1", default=0.0455)
    AttachedFlowConstantB2: Optional[float] = Field(alias="AttachedFlowConstantB2", default=0.3)





BeddoesLeishmanModel.update_forward_refs()
