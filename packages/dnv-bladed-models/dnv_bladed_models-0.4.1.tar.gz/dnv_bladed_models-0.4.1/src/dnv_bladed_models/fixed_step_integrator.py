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

from dnv_bladed_models.integrator import Integrator



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class FixedStepIntegrator(Integrator, ABC):
    r"""
    Common settings for the fixed step integrators.
    
    Not supported yet.
    
    Attributes:
    ----------
    TimeStep : float, Not supported yet
        The fixed time step used by the integrator.  It must be set as a divisor of the output time-step and external controller communication interval.

    Tolerance : float, default=0.005, Not supported yet
        When the \"Maximum number of iterations\" > 1, the integrator relative tolerance is used to control how many iterations are carried out when integrating the first order and prescribed second order states.  Iterations are carried out until the maximum number of iterations is reached, or until the change in all first order and prescribed state derivatives between successive iterations is less than the relative tolerance multiplied by the state derivative absolute value.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/Integrator/common/FixedStepIntegrator.json')
    
    TimeStep: Optional[float] = Field(alias="TimeStep", default=None) # Not supported yet
    Tolerance: Optional[float] = Field(alias="Tolerance", default=0.005) # Not supported yet





FixedStepIntegrator.update_forward_refs()
