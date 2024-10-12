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

from dnv_bladed_models.bladed_model import BladedModel



class EvolvingWindTurbulence_MethodEnum(str, Enum):
    KRISTENSEN = "KRISTENSEN"
    EXPONENTIAL = "EXPONENTIAL"

class EvolvingWindTurbulence_ApplyToEnum(str, Enum):
    OFF = "OFF"
    LIDAR_ONLY = "LIDAR_ONLY"
    ALL_WIND_CALCULATIONS = "ALL_WIND_CALCULATIONS"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class EvolvingWindTurbulence(BladedModel):
    r"""
    The settings for evolving turbulence.  In the case of a normal turbulent wind field, the turbulence is \&quot;frozen\&quot; and approaches the turbine at a constant block.  Although this doesn&#39;t match physical reality, it is a particular problem for Lidar - as it gives them a \&quot;perfect\&quot; insight into the oncoming wind field.  In order to represent the nature of real turbulence, a second turbulence file is superimposed on the windfield so that it \&quot;evolves\&quot; as it moves forward.  This is computationally expensive, and is usually applied only to the Lidar readings - although it can be applied to all the wind values in a simulation.
    
    Not supported yet.
    
    Attributes:
    ----------
    SecondTurbulenceFilepath : str, Not supported yet
        The filepath or URI of the second turbulence file.  The turbulence in this file will be used to simulate an evolving turbulence field.

    Method : EvolvingWindTurbulence_MethodEnum, Not supported yet
        The method used to combine the turbulence in the two turbulence files.

    ExponentialFactor : float, Not supported yet
        The exponential factor for use in the exponential model.

    ApplyTo : EvolvingWindTurbulence_ApplyToEnum, Not supported yet
        Evolving turbulence is usually only applied to Lidar readings, but it can be applied to all wind values.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/EvolvingWindTurbulence/EvolvingWindTurbulence.json')
    
    SecondTurbulenceFilepath: Optional[str] = Field(alias="SecondTurbulenceFilepath", default=None) # Not supported yet
    Method: Optional[EvolvingWindTurbulence_MethodEnum] = Field(alias="Method", default=None) # Not supported yet
    ExponentialFactor: Optional[float] = Field(alias="ExponentialFactor", default=None) # Not supported yet
    ApplyTo: Optional[EvolvingWindTurbulence_ApplyToEnum] = Field(alias="ApplyTo", default=None) # Not supported yet

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
        EvolvingWindTurbulence
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = EvolvingWindTurbulence.from_file('/path/to/file')
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
        EvolvingWindTurbulence
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = EvolvingWindTurbulence.from_json('{ ... }')
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
        EvolvingWindTurbulence
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


EvolvingWindTurbulence.update_forward_refs()
