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

from dnv_bladed_models.steady_calculation import SteadyCalculation

from dnv_bladed_models.steady_calculation_with_component_outputs import SteadyCalculationWithComponentOutputs



class SteadyParkedLoadsCalculation_SweepParameterEnum(str, Enum):
    AZIMUTH_ANGLE = "AZIMUTH_ANGLE"
    YAW_ANGLE = "YAW_ANGLE"
    FLOW_INCLINATION = "FLOW_INCLINATION"
    PITCH_ANGLE = "PITCH_ANGLE"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class SteadyParkedLoadsCalculation(SteadyCalculation, SteadyCalculationType='SteadyParkedLoads'):
    r"""
    Defines a calculation which produces loads on the parked turbine in a steady wind.  Most realities such as tower shadow and wind shear are included, making the calculation almost equivalent to a time domain simulation in a steady wind.
    
    Not supported yet.
    
    Attributes:
    ----------
    SteadyCalculationType : str, default='SteadyParkedLoads', Not supported yet
        Defines the specific type of SteadyCalculation model in use.  For a `SteadyParkedLoads` object, this must always be set to a value of `SteadyParkedLoads`.

    WindSpeed : float, Not supported yet
        The wind speed at the hub height to be used for the calculation.

    AzimuthAngle : float, Not supported yet
        The fixed azimuth angle of the rotor (zero azimuth indicates blade 1 pointing upwards).

    YawAngle : float, Not supported yet
        The yaw angle to be used for the calculation.

    FlowInclination : float, Not supported yet
        The flow inclination to be used for the calculation.

    PitchAngle : float, Not supported yet
        The pitch angle of all of the blades to be used for the calculation.

    SweepParameter : SteadyParkedLoadsCalculation_SweepParameterEnum, Not supported yet
        The parameter to perform the sweep over.

    SweepEnd : float, Not supported yet
        The value for the end of the sweep.  The start value will be whatever it is in the parameters for the calculation.

    SweepInterval : float, Not supported yet
        The step size to take from the lowest to the highest value.

    Outputs : SteadyCalculationWithComponentOutputs

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/SteadyParkedLoadsCalculation.json')
    
    SteadyCalculationType: Optional[str] = Field(alias="SteadyCalculationType", default='SteadyParkedLoads') # Not supported yet
    WindSpeed: Optional[float] = Field(alias="WindSpeed", default=None) # Not supported yet
    AzimuthAngle: Optional[float] = Field(alias="AzimuthAngle", default=None) # Not supported yet
    YawAngle: Optional[float] = Field(alias="YawAngle", default=None) # Not supported yet
    FlowInclination: Optional[float] = Field(alias="FlowInclination", default=None) # Not supported yet
    PitchAngle: Optional[float] = Field(alias="PitchAngle", default=None) # Not supported yet
    SweepParameter: Optional[SteadyParkedLoadsCalculation_SweepParameterEnum] = Field(alias="SweepParameter", default=None) # Not supported yet
    SweepEnd: Optional[float] = Field(alias="SweepEnd", default=None) # Not supported yet
    SweepInterval: Optional[float] = Field(alias="SweepInterval", default=None) # Not supported yet
    Outputs: Optional[SteadyCalculationWithComponentOutputs] = Field(alias="Outputs", default=None)

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
        SteadyParkedLoadsCalculation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SteadyParkedLoadsCalculation.from_file('/path/to/file')
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
        SteadyParkedLoadsCalculation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = SteadyParkedLoadsCalculation.from_json('{ ... }')
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
        SteadyParkedLoadsCalculation
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


SteadyParkedLoadsCalculation.update_forward_refs()
