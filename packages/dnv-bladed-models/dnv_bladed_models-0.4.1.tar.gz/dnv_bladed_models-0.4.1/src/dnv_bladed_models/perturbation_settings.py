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



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class PerturbationSettings(BladedModel, ABC):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    NumberOfPerturbationPoints : int, default=5, Not supported yet
        The number of values that each state gets perturbed to either side of the equilibrium point.  Larger numbers provide more robustness; smaller numbers provide faster analysis and lower memory usage.

    AbsoluteTolerancePerturbationScale : float, default=100, Not supported yet
        The zero value states have a perturbation magnitude of this value multiplied by the absolute tolerance of the state

    StateRelativePerturbation : float, default=0.005, Not supported yet
        The magnitude of the state perturbations relative to the absolute steady-state state values

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/common/PerturbationSettings.json')
    
    NumberOfPerturbationPoints: Optional[int] = Field(alias="NumberOfPerturbationPoints", default=5) # Not supported yet
    AbsoluteTolerancePerturbationScale: Optional[float] = Field(alias="AbsoluteTolerancePerturbationScale", default=100) # Not supported yet
    StateRelativePerturbation: Optional[float] = Field(alias="StateRelativePerturbation", default=0.005) # Not supported yet





PerturbationSettings.update_forward_refs()
