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

from dnv_bladed_models.steady_calculation import SteadyCalculation

from dnv_bladed_models.steady_calculation_outputs import SteadyCalculationOutputs



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class LinearisationCalculation(SteadyCalculation, ABC):
    r"""
    The common properties of calculations which use small perturbations to generate system responses, from which the dynamics of the fully coupled system can be analysed.
    
    Not supported yet.
    
    Attributes:
    ----------
    MinimumCorrelationCoefficient : float, default=0.8, Not supported yet
        The minimum acceptable correlation coefficient for the relationship between a state value and a state derivative.  If it is below the minimum, the relationship is disregarded and a zero value is taken.

    Outputs : SteadyCalculationOutputs

    TransformRotorModesToNonRotating : bool, default=False, Not supported yet
        If true, a multi-blade coordinate (MBC) transform will be performed to transform the rotating modes into the stationary frame of reference.  This will generate forward and backward whirling modes in a Campbell diagram.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/common/LinearisationCalculation.json')
    
    MinimumCorrelationCoefficient: Optional[float] = Field(alias="MinimumCorrelationCoefficient", default=0.8) # Not supported yet
    Outputs: Optional[SteadyCalculationOutputs] = Field(alias="Outputs", default=None)
    TransformRotorModesToNonRotating: Optional[bool] = Field(alias="TransformRotorModesToNonRotating", default=False) # Not supported yet





LinearisationCalculation.update_forward_refs()
