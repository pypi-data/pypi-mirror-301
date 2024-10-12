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



class DynamicStall_DynamicStallTypeEnum(str, Enum):
    COMPRESSIBLE_BEDDOES_LEISHMAN_MODEL = "CompressibleBeddoesLeishmanModel"
    IAG_MODEL = "IAGModel"
    INCOMPRESSIBLE_BEDDOES_LEISHMAN_MODEL = "IncompressibleBeddoesLeishmanModel"
    OYE_MODEL = "OyeModel"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class DynamicStall(BladedModel, ABC):
    r"""
    The common properties of all of the dynamic stall models.
    
    Attributes:
    ----------
    DynamicStallType : DynamicStall_DynamicStallTypeEnum
        Defines the specific type of model in use.

    UseDynamicPitchingMomentCoefficient : bool, default=True
        If true, the dynamic pitching moment coefficient will be used.  This option is enabled by default.  It is not recommended to disable this option for blades with a torsional degree of freedom because the so-called 'pitch- rate damping' term of the moment coefficient is typically important to keep the blade torsional mode stable.

    StartingRadius : float, default=0
        The fraction of the radius outboard of which the dynamic stall model will be used. A value of 0.0 means that dynamic stall is applied from the blade root.

    EndingRadius : float, default=0.95
        The fraction of the radius outboard of which the dynamic stall model will be switched off. A value of 1.0 means that dynamic stall is applied until the blade tip.

    SeparationTimeConstant : float, default=3
        A dimensionless time constant, given in terms of the time taken to travel half a chord. It defines the lag in the movement of the separation point due to unsteady pressure and boundary layer response.

    UseLinearFitGradientMethod : bool, default=True
        If true, the linear fit polar gradient is used to reconstruct the inviscid polar data. The fit is performed only within the linear polar regime that is searched automatically between the zero lift AoA to AoA = 7 deg. This approach is more suitable for polar data sets where the lift coefficient slope is not straight around 0 deg angle of attack. It is recommended to activate this option for more accurate computations. This option is turned on by default.

    Notes:
    -----
    This class is an abstraction, with the following concrete implementations:
        - CompressibleBeddoesLeishmanModel
        - IAGModel
        - IncompressibleBeddoesLeishmanModel
        - OyeModel
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/DynamicStall/common/DynamicStall.json')
    
    DynamicStallType: Optional[DynamicStall_DynamicStallTypeEnum] = Field(alias="DynamicStallType", default=None)
    UseDynamicPitchingMomentCoefficient: Optional[bool] = Field(alias="UseDynamicPitchingMomentCoefficient", default=True)
    StartingRadius: Optional[float] = Field(alias="StartingRadius", default=0)
    EndingRadius: Optional[float] = Field(alias="EndingRadius", default=0.95)
    SeparationTimeConstant: Optional[float] = Field(alias="SeparationTimeConstant", default=3)
    UseLinearFitGradientMethod: Optional[bool] = Field(alias="UseLinearFitGradientMethod", default=True)



    _subtypes_ = dict()

    def __init_subclass__(cls, DynamicStallType=None):
        cls._subtypes_[DynamicStallType or cls.__name__.lower()] = cls

    @classmethod
    def __get_validators__(cls):
        yield cls._discriminator_factory

    @classmethod
    def _discriminator_factory(cls, data: dict):
        if isinstance(data, dict):
            data_type = data.get("DynamicStallType")
            if data_type is None:
                raise ValueError("Missing 'DynamicStallType' in DynamicStall")
            sub = cls._subtypes_.get(data_type)
            if sub is None:
                raise TypeError(f"Unsupported sub-type: '{data_type}' for base-type 'DynamicStall'")
            return sub(**data)
        return data


DynamicStall.update_forward_refs()
