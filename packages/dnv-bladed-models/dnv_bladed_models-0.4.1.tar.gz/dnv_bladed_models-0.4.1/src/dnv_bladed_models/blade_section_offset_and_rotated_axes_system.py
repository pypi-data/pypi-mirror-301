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

from dnv_bladed_models.blade_section_offset_axes_system import BladeSectionOffsetAxesSystem



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladeSectionOffsetAndRotatedAxesSystem(BladeSectionOffsetAxesSystem, ABC):
    r"""
    The common properties of axes systems that are offset from the reference axes.
    
    Attributes:
    ----------
    RotationAboutReferenceZ : float, default=0
        The rotation of the axis system's x and y axes around the reference z axis (the section plane normal).

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeSectionDefinition/BladeSectionAxesAndCoordinateSystems/common/BladeSectionOffsetAndRotatedAxesSystem.json')
    
    RotationAboutReferenceZ: Optional[float] = Field(alias="RotationAboutReferenceZ", default=0)





BladeSectionOffsetAndRotatedAxesSystem.update_forward_refs()
