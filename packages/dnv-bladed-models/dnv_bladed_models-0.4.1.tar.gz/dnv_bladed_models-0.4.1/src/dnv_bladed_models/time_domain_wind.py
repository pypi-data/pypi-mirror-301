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

from dnv_bladed_models.dynamic_upstream_wake import DynamicUpstreamWake

from dnv_bladed_models.steady_wake_deficit import SteadyWakeDeficit

from dnv_bladed_models.vertical_shear import VerticalShear

from dnv_bladed_models.wind import Wind

from dnv_bladed_models.wind_direction_variation import WindDirectionVariation



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TimeDomainWind(Wind, ABC):
    r"""
    The definition of a wind field that varies throughout a time domain simulation.
    
    Not supported yet.
    
    Attributes:
    ----------
    ReferenceHeight : float, Not supported yet
        The reference height for the wind field, above which the free-field wind conditions take over.  If this is omitted, the hub height will be used, and if there is more than one the *highest* hub height.

    Inclination : float, default=0, Not supported yet
        The inclination of the flow relative to the horizontal plane.  Typically this is in the order of 8 degrees for an onshore turbine, and 0 degrees for an offshore turbine.

    UseGustPropagation : bool, Not supported yet
        If true, gust propagation will be applied (where the transient properties only \"arrive\" at the turbine as the flow does).  This is only relevant to transient flows.

    Direction : float, Not supported yet
        The (constant) direction of the wind relative to the global X axis.

    DirectionVariation : WindDirectionVariation, abstract, Not supported yet

    SteadyWakeDeficit : SteadyWakeDeficit, abstract, Not supported yet

    VerticalShear : VerticalShear, abstract, Not supported yet

    VerticalDirectionShear : float, Not supported yet
        The vertical direction shear, otherwise known as \"wind veer\".  This models the case where the direction of the wind field varies as the height increases.

    DynamicUpstreamWake : DynamicUpstreamWake, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    DirectionVariation has the following concrete types:
        - PresetWindDirectionTransient
        - WindDirectionTimeHistory
    
    SteadyWakeDeficit has the following concrete types:
        - Gaussian
        - UserDefinedWakeDeficit
    
    VerticalShear has the following concrete types:
        - ExponentialShearModel
        - LogarithmicShearModel
        - LookUpShearModel
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/common/TimeDomainWind.json')
    
    ReferenceHeight: Optional[float] = Field(alias="ReferenceHeight", default=None) # Not supported yet
    Inclination: Optional[float] = Field(alias="Inclination", default=0) # Not supported yet
    UseGustPropagation: Optional[bool] = Field(alias="UseGustPropagation", default=None) # Not supported yet
    Direction: Optional[float] = Field(alias="Direction", default=None) # Not supported yet
    DirectionVariation: Optional[WindDirectionVariation] = Field(alias="DirectionVariation", default=None) # Not supported yet
    SteadyWakeDeficit: Optional[SteadyWakeDeficit] = Field(alias="SteadyWakeDeficit", default=None) # Not supported yet
    VerticalShear: Optional[VerticalShear] = Field(alias="VerticalShear", default=None) # Not supported yet
    VerticalDirectionShear: Optional[float] = Field(alias="VerticalDirectionShear", default=None) # Not supported yet
    DynamicUpstreamWake: Optional[DynamicUpstreamWake] = Field(alias="DynamicUpstreamWake", default=None) # Not supported yet





TimeDomainWind.update_forward_refs()
