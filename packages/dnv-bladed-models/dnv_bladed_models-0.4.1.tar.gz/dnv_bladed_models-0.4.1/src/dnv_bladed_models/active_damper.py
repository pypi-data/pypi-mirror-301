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

from dnv_bladed_models.damper import Damper



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ActiveDamper(Damper, ABC):
    r"""
    An active damper, applying a force which is specified by the controller.
    
    Not supported yet.
    
    Attributes:
    ----------
    ForceLag : float, Not supported yet
        The force lag for the force signal's transfer function.

    AccelerationLag : float, Not supported yet
        The time lag for the acceleration signal's transfer function.

    ForceTransferFunction : float, Not supported yet
        Transfer function for active damper

    PerturbationForLinearisationCalculation : float, Not supported yet
        The perturbation step to use during linearisation calculation.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Damper/common/ActiveDamper.json')
    
    ForceLag: Optional[float] = Field(alias="ForceLag", default=None) # Not supported yet
    AccelerationLag: Optional[float] = Field(alias="AccelerationLag", default=None) # Not supported yet
    ForceTransferFunction: Optional[float] = Field(alias="ForceTransferFunction", default=None) # Not supported yet
    PerturbationForLinearisationCalculation: Optional[float] = Field(alias="PerturbationForLinearisationCalculation", default=None) # Not supported yet





ActiveDamper.update_forward_refs()
