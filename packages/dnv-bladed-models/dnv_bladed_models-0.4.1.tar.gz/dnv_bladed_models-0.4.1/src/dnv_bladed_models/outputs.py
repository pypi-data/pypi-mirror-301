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



class Outputs_FileFormatEnum(str, Enum):
    BINARY = "BINARY"
    ASCII = "ASCII"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Outputs(BladedModel, ABC):
    r"""
    Definition outputs to write for this analysis.
    
    Attributes:
    ----------
    OutputDirectory : str
        The output directory for results files.

    FileStem : str, default=''
        A name for the analysis that will be used as the name of all the output files.  If omitted, the run type will be used, such as 'powprod'.

    FileFormat : Outputs_FileFormatEnum, default='BINARY'
        The output format, whether it is ASCII or binary.

    OutputDongleActivity : bool, default=False
        If true, the dongle activity will be logged.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('common/Outputs.json')
    
    OutputDirectory: Optional[str] = Field(alias="OutputDirectory", default=None)
    FileStem: Optional[str] = Field(alias="FileStem", default='')
    FileFormat: Optional[Outputs_FileFormatEnum] = Field(alias="FileFormat", default='BINARY')
    OutputDongleActivity: Optional[bool] = Field(alias="OutputDongleActivity", default=False)





Outputs.update_forward_refs()
