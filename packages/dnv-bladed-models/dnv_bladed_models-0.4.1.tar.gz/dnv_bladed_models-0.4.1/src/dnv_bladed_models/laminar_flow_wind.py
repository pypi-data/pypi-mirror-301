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

from dnv_bladed_models.time_domain_wind import TimeDomainWind

from dnv_bladed_models.wind_direction_shear_variation import WindDirectionShearVariation

from dnv_bladed_models.wind_horizontal_shear_variation import WindHorizontalShearVariation

from dnv_bladed_models.wind_mean_speed_variation import WindMeanSpeedVariation

from dnv_bladed_models.wind_vertical_shear_variation import WindVerticalShearVariation



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class LaminarFlowWind(TimeDomainWind, WindType='LaminarFlow'):
    r"""
    The definition of a wind field that varies throughout a time domain simulation, but does not have turbulence.
    
    Not supported yet.
    
    Attributes:
    ----------
    WindType : str, default='LaminarFlow', Not supported yet
        Defines the specific type of Wind model in use.  For a `LaminarFlow` object, this must always be set to a value of `LaminarFlow`.

    MeanSpeed : float, Not supported yet
        The (constant) mean wind speed for the duration of the simulation.

    MeanSpeedVariation : WindMeanSpeedVariation, abstract, Not supported yet

    VerticalShearVariation : WindVerticalShearVariation, abstract, Not supported yet

    HorizontalShearVariation : WindHorizontalShearVariation, abstract, Not supported yet

    DirectionShearVariation : WindDirectionShearVariation, abstract, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    MeanSpeedVariation has the following concrete types:
        - PresetWindMeanSpeedTransient
        - WindMeanSpeedTimeHistory
    
    VerticalShearVariation has the following concrete types:
        - PresetWindVerticalShearTransient
        - WindVerticalShearTimeHistory
    
    HorizontalShearVariation has the following concrete types:
        - PresetWindHorizontalShearTransient
        - WindHorizontalShearTimeHistory
    
    DirectionShearVariation has the following concrete types:
        - PresetWindDirectionShearTransient
        - WindDirectionShearTimeHistory
    
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/LaminarFlowWind.json')
    
    WindType: Optional[str] = Field(alias="WindType", default='LaminarFlow') # Not supported yet
    MeanSpeed: Optional[float] = Field(alias="MeanSpeed", default=None) # Not supported yet
    MeanSpeedVariation: Optional[WindMeanSpeedVariation] = Field(alias="MeanSpeedVariation", default=None) # Not supported yet
    VerticalShearVariation: Optional[WindVerticalShearVariation] = Field(alias="VerticalShearVariation", default=None) # Not supported yet
    HorizontalShearVariation: Optional[WindHorizontalShearVariation] = Field(alias="HorizontalShearVariation", default=None) # Not supported yet
    DirectionShearVariation: Optional[WindDirectionShearVariation] = Field(alias="DirectionShearVariation", default=None) # Not supported yet

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
        LaminarFlowWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LaminarFlowWind.from_file('/path/to/file')
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
        LaminarFlowWind
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LaminarFlowWind.from_json('{ ... }')
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
        LaminarFlowWind
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


LaminarFlowWind.update_forward_refs()
