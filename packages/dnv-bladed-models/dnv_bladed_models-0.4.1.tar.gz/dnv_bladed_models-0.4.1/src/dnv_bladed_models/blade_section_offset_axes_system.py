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

class BladeSectionOffsetAxesSystem(BladedModel, ABC):
    r"""
    The common properties of axes systems that are offset from the reference axes.
    
    Attributes:
    ----------
    OffsetInReferenceX : float, default=0
        The offset of the axis system origin from the reference axes in x.

    OffsetInReferenceY : float, default=0
        The offset of the axis system origin from the reference axes in y.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeSectionDefinition/BladeSectionAxesAndCoordinateSystems/common/BladeSectionOffsetAxesSystem.json')
    
    OffsetInReferenceX: Optional[float] = Field(alias="OffsetInReferenceX", default=0)
    OffsetInReferenceY: Optional[float] = Field(alias="OffsetInReferenceY", default=0)





BladeSectionOffsetAxesSystem.update_forward_refs()
