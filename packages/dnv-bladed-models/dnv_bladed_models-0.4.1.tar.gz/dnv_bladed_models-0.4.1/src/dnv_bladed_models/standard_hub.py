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

from dnv_bladed_models.hub import Hub

from dnv_bladed_models.rotor_imbalances import RotorImbalances



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class StandardHub(Hub, ABC):
    r"""
    The common properties of hubs with rotational symmetry and more than two blades.
    
    Attributes:
    ----------
    NumberOfBlades : int
        The number of blades on the hub.

    Imbalances : RotorImbalances

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/Hub/common/StandardHub.json')
    
    NumberOfBlades: Optional[int] = Field(alias="NumberOfBlades", default=None)
    Imbalances: Optional[RotorImbalances] = Field(alias="Imbalances", default=None)





StandardHub.update_forward_refs()
