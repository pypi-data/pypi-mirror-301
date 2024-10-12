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

from dnv_bladed_models.additional_constrained_wave import AdditionalConstrainedWave

from dnv_bladed_models.wave_diffraction_approximation import WaveDiffractionApproximation

from dnv_bladed_models.waves import Waves



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class IrregularWaves(Waves, ABC):
    r"""
    The definition of irregular waves.
    
    Not supported yet.
    
    Attributes:
    ----------
    DirectionOfApproachClockwiseFromNorth : float, Not supported yet
        The bearing from which waves arrive at the turbine.

    RandomNumberSeed : int, Not supported yet
        A arbitrary integer used to generate a realisation of the irregular waves.  This ensures that the 'randomness' is consistent from simulation to simulation.

    WaveDiffractionApproximation : WaveDiffractionApproximation, abstract, Not supported yet

    AdditionalConstrainedWave : AdditionalConstrainedWave, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    WaveDiffractionApproximation has the following concrete types:
        - AutomaticMacCamyFuchs
        - AutomaticSimpleCutoffFrequency
        - MacCamyFuchs
        - SimpleCutoffFrequency
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Waves/common/IrregularWaves.json')
    
    DirectionOfApproachClockwiseFromNorth: Optional[float] = Field(alias="DirectionOfApproachClockwiseFromNorth", default=None) # Not supported yet
    RandomNumberSeed: Optional[int] = Field(alias="RandomNumberSeed", default=None) # Not supported yet
    WaveDiffractionApproximation: Optional[WaveDiffractionApproximation] = Field(alias="WaveDiffractionApproximation", default=None) # Not supported yet
    AdditionalConstrainedWave: Optional[AdditionalConstrainedWave] = Field(alias="AdditionalConstrainedWave", default=None) # Not supported yet





IrregularWaves.update_forward_refs()
