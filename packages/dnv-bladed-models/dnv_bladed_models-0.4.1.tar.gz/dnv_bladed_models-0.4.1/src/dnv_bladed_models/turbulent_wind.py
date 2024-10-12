# coding: utf-8

from __future__ import annotations

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

from dnv_bladed_models.evolving_wind_turbulence import EvolvingWindTurbulence

from dnv_bladed_models.time_domain_wind import TimeDomainWind



class TurbulentWind_CentreTurbulenceFileOnEnum(str, Enum):
    CENTRED_ON_HUB = "CENTRED_ON_HUB"
    BEST_FIT = "BEST_FIT"
    USER_SPECIFIED = "USER_SPECIFIED"

class TurbulentWind_InterpolationMethodEnum(str, Enum):
    LINEAR = "LINEAR"
    CUBIC_IN_ROTOR_PLANE = "CUBIC_IN_ROTOR_PLANE"
    ALL_CUBIC = "ALL_CUBIC"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TurbulentWind(TimeDomainWind, WindType='TurbulentWind'):
    r"""
    The definition of a turbulent flow field, with the values for the turbulence defined in an external file.
    
    Not supported yet.
    
    Attributes:
    ----------
    WindType : str, default='TurbulentWind', Not supported yet
        Defines the specific type of Wind model in use.  For a `TurbulentWind` object, this must always be set to a value of `TurbulentWind`.

    MeanSpeed : float, Not supported yet
        The mean wind speed upon which the turbulence will be added.  This must correspond with the mean wind speed used to create the turbulence file.

    TurbulenceFilepath : str, Not supported yet
        The filepath or URI of the turbulence file.

    TurbulenceIntensity : float, Not supported yet
        The turbulence intensity in the longitudinal (global X) direction.  This is used to scale the turbulence provided in the file.

    TurbulenceIntensityLateral : float, Not supported yet
        The turbulence intensity in the lateral (global Y) direction.  This is typically in the order of 80% of the longitudinal turbulence intensity.

    TurbulenceIntensityVertical : float, Not supported yet
        The turbulence intensity in the vertical (global Z) direction.  This is typically in the order of 50% of the longitudinal turbulence intensity.

    CentreTurbulenceFileOn : TurbulentWind_CentreTurbulenceFileOnEnum, Not supported yet
        The method used to position the data in the turbulence file relative to the turbine.  If any part of the rotor exceeds this box, the simulation will terminate with an exception.

    InterpolationMethod : TurbulentWind_InterpolationMethodEnum, Not supported yet
        The method used to interpolate the wind speed in between the provided turbulence locations.

    RepeatTurbulenceFile : bool, Not supported yet
        If true, the turbulence file will be \"looped\".  If false, the turbulence will be 0 in all three components once the end of the file has been reached.  Using part of a turbulence file may invalidate its turbulence statistics, and no effort is made by Bladed to ensure coherence at the point when it transitions from the end of the wind file back to the beginning.

    EvolvingTurbulence : EvolvingWindTurbulence, Not supported yet

    TurbulenceFileStartTime : float, default=0, Not supported yet
        The time into turbulent wind file at start of simulation.  This can be used to synchronise the wind file with simulation.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/TurbulentWind.json')
    
    WindType: Optional[str] = Field(alias="WindType", default='TurbulentWind') # Not supported yet
    MeanSpeed: Optional[float] = Field(alias="MeanSpeed", default=None) # Not supported yet
    TurbulenceFilepath: Optional[str] = Field(alias="TurbulenceFilepath", default=None) # Not supported yet
    TurbulenceIntensity: Optional[float] = Field(alias="TurbulenceIntensity", default=None) # Not supported yet
    TurbulenceIntensityLateral: Optional[float] = Field(alias="TurbulenceIntensityLateral", default=None) # Not supported yet
    TurbulenceIntensityVertical: Optional[float] = Field(alias="TurbulenceIntensityVertical", default=None) # Not supported yet
    CentreTurbulenceFileOn: Optional[TurbulentWind_CentreTurbulenceFileOnEnum] = Field(alias="CentreTurbulenceFileOn", default=None) # Not supported yet
    InterpolationMethod: Optional[TurbulentWind_InterpolationMethodEnum] = Field(alias="InterpolationMethod", default=None) # Not supported yet
    RepeatTurbulenceFile: Optional[bool] = Field(alias="RepeatTurbulenceFile", default=None) # Not supported yet
    EvolvingTurbulence: Optional[EvolvingWindTurbulence] = Field(alias="EvolvingTurbulence", default=None) # Not supported yet
    TurbulenceFileStartTime: Optional[float] = Field(alias="TurbulenceFileStartTime", default=0) # Not supported yet

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass



    def to_json(self, indent: Optional[int] = 2, **json_kwargs: Any) -> str:
        r"""
        Generates a JSON string representation of the model.

        Parameters
        ----------
        indent : int
            The whitespace indentation to use for formatting, as per json.dumps().

        Examples
        --------
        >>> model.to_json()
        Renders the full JSON representation of the model object.
        """

        json_kwargs['by_alias'] = True
        json_kwargs['exclude_unset'] = False
        json_kwargs['exclude_none'] = True
        if self.Schema is None:
            self.Schema = SchemaHelper.construct_schema_url(self._relative_schema_path)
        
        return super().json(indent=indent, **json_kwargs)


    @classmethod
    def from_file(cls: Type['Model'], path: Union[str, Path]) -> 'Model':
        r"""
        Loads a model from a given file path.

        Parameters
        ----------
        path : string
            The file path to the model.

        Returns
        -------
        TurbulentWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TurbulentWind.from_file('/path/to/file')
        """
        
        return super().parse_file(path=path)


    @classmethod
    def from_json(cls: Type['Model'], b: StrBytes) -> 'Model':
        r"""
        Creates a model object from a JSON string.

        Parameters
        ----------
        b: StrBytes
            The JSON string describing the model.

        Returns
        -------
        TurbulentWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TurbulentWind.from_json('{ ... }')
        """

        return super().parse_raw(
            b=b,
            content_type='application/json')
        

    @classmethod
    def from_dict(cls: Type['Model'], obj: Any) -> 'Model':
        r"""
        Creates a model object from a dict.
        
        Parameters
        ----------
        obj : Any
            The dictionary object describing the model.

        Returns
        -------
        TurbulentWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.
        """
        
        return super().parse_obj(obj=obj)


    def to_file(self, path: Union[str, Path]):
        r"""
        Writes the model as a JSON document to a file with UTF8 encoding.

        Parameters
        ----------                
        path : string
            The file path to which the model will be written.

        Examples
        --------
        >>> model.to_file('/path/to/file')
        """

        with open(file=path, mode='w', encoding="utf8") as output_file:
            output_file.write(self.to_json())


TurbulentWind.update_forward_refs()
