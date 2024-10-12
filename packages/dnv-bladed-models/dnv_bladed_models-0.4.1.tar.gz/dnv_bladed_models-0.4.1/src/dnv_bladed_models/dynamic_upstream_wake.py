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

from dnv_bladed_models.meandering_wake import MeanderingWake

from dnv_bladed_models.position_of_upwind_turbine import PositionOfUpwindTurbine

from dnv_bladed_models.wake_properties_of_upstream_turbine import WakePropertiesOfUpstreamTurbine



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class DynamicUpstreamWake(BladedModel):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    RadialStepSize : float, default=0.05, Not supported yet
        The resolution of the wake deficit profile in the radial direction.

    NumberOfRadialPoints : int, default=50, Not supported yet
        The total number of points in the radial wake deficit profile.

    StreamwiseStep : float, default=0.1, Not supported yet
        The integration step in streamwise direction for the propagation of the wake.

    MixingLength : float, default=1.323, Not supported yet
        The length scale of the part of ambient turbulence which affects the wake deficit evolution.

    ShearCalibrationConstant : float, default=0.008, Not supported yet
        The calibration factor for self-generated turbulence.  IEC edition 4 recommends a value of 0.008.

    AmbientCalibrationConstant : float, default=0.023, Not supported yet
        The calibration factor for influence of ambient turbulence.  IEC edition 4 recommends a value of 0.023.

    PositionOfUpwindTurbine : PositionOfUpwindTurbine, Not supported yet

    WakePropertiesOfUpstreamTurbine : WakePropertiesOfUpstreamTurbine, Not supported yet

    MeanderingWake : MeanderingWake, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/Wind/DynamicUpstreamWake/DynamicUpstreamWake.json')
    
    RadialStepSize: Optional[float] = Field(alias="RadialStepSize", default=0.05) # Not supported yet
    NumberOfRadialPoints: Optional[int] = Field(alias="NumberOfRadialPoints", default=50) # Not supported yet
    StreamwiseStep: Optional[float] = Field(alias="StreamwiseStep", default=0.1) # Not supported yet
    MixingLength: Optional[float] = Field(alias="MixingLength", default=1.323) # Not supported yet
    ShearCalibrationConstant: Optional[float] = Field(alias="ShearCalibrationConstant", default=0.008) # Not supported yet
    AmbientCalibrationConstant: Optional[float] = Field(alias="AmbientCalibrationConstant", default=0.023) # Not supported yet
    PositionOfUpwindTurbine: Optional[PositionOfUpwindTurbine] = Field(alias="PositionOfUpwindTurbine", default=None) # Not supported yet
    WakePropertiesOfUpstreamTurbine: Optional[WakePropertiesOfUpstreamTurbine] = Field(alias="WakePropertiesOfUpstreamTurbine", default=None) # Not supported yet
    MeanderingWake: Optional[MeanderingWake] = Field(alias="MeanderingWake", default=None) # Not supported yet

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
        DynamicUpstreamWake
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DynamicUpstreamWake.from_file('/path/to/file')
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
        DynamicUpstreamWake
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DynamicUpstreamWake.from_json('{ ... }')
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
        DynamicUpstreamWake
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


DynamicUpstreamWake.update_forward_refs()
