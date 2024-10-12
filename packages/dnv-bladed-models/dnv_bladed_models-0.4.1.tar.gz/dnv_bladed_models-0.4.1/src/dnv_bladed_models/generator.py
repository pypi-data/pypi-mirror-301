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

from dnv_bladed_models.component import Component

from dnv_bladed_models.electrical_losses import ElectricalLosses

from dnv_bladed_models.generator_output_group_library import GeneratorOutputGroupLibrary



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Generator(Component, ABC):
    r"""
    The common properties for all types of generator.
    
    Attributes:
    ----------
    GeneratorInertia : float
        The total rotational inertia of the generator, including that of the high-speed shaft after the clutch.

    Losses : ElectricalLosses, abstract

    OutputGroups : GeneratorOutputGroupLibrary, Not supported yet

    Notes:
    -----
    Losses has the following concrete types:
        - LinearElectricalLosses
        - NonLinearElectricalLosses
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Generator/common/Generator.json')
    
    GeneratorInertia: Optional[float] = Field(alias="GeneratorInertia", default=None)
    Losses: Optional[ElectricalLosses] = Field(alias="Losses", default=None)
    OutputGroups: Optional[GeneratorOutputGroupLibrary] = Field(alias="OutputGroups", default=GeneratorOutputGroupLibrary()) # Not supported yet





Generator.update_forward_refs()
