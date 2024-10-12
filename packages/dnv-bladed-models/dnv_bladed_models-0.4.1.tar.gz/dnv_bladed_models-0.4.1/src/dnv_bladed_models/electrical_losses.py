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



class ElectricalLosses_ElectricalLossesTypeEnum(str, Enum):
    LINEAR_ELECTRICAL_LOSSES = "LinearElectricalLosses"
    NON_LINEAR_ELECTRICAL_LOSSES = "NonLinearElectricalLosses"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ElectricalLosses(BladedModel, ABC):
    r"""
    The electrical losses in the generator.
    
    Attributes:
    ----------
    ElectricalLossesType : ElectricalLosses_ElectricalLossesTypeEnum
        Defines the specific type of model in use.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - LinearElectricalLosses
        - NonLinearElectricalLosses
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Generator/ElectricalLosses/common/ElectricalLosses.json')
    
    ElectricalLossesType: Optional[ElectricalLosses_ElectricalLossesTypeEnum] = Field(alias="ElectricalLossesType", default=None)



    _subtypes_ = dict()

    def __init_subclass__(cls, ElectricalLossesType=None):
        cls._subtypes_[ElectricalLossesType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("ElectricalLossesType")
            if data_type is None:
                raise ValueError("Missing 'ElectricalLossesType' in ElectricalLosses")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'ElectricalLosses'")
            return sub(**data)
        return data


ElectricalLosses.update_forward_refs()
