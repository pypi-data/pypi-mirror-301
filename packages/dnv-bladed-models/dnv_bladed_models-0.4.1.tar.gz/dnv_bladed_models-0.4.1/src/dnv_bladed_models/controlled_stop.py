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

from dnv_bladed_models.controlled_operation import ControlledOperation



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ControlledStop(ControlledOperation, ABC):
    r"""
    A stop operation  occuring at a specified time.
    
    Not supported yet.
    
    Attributes:
    ----------
    ExtraSimulationTimeAfterFullStop : float, Not supported yet
        The time after all rotors come to a complete stop at which to terminate the simulation.  If this occurs after the simulation duration has completed, it will have no effect.  This parameter is to allow a simulation to stop earlier if all the required data has been collected.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Event/common/ControlledStop.json')
    
    ExtraSimulationTimeAfterFullStop: Optional[float] = Field(alias="ExtraSimulationTimeAfterFullStop", default=None) # Not supported yet





ControlledStop.update_forward_refs()
