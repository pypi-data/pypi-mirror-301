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

from dnv_bladed_models.full_load_operation import FullLoadOperation

from dnv_bladed_models.nominal_hub_wind_speed_vs_minimum_steady_state_pitch_angle import NominalHubWindSpeedVsMinimumSteadyStatePitchAngle

from dnv_bladed_models.partial_load_operation import PartialLoadOperation



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class VariableSpeedPitchRegulatedControlModel(BladedModel):
    r"""
    The operational parameters that Bladed uses to determine the steady state conditions of the turbine. Although some of the values will be made available to the external controller through the API, they will not be used by Bladed during the remainder of a time domain simulation.
    
    Attributes:
    ----------
    MinimumSteadyStatePitchAngle : float
        This value represents the minimum allowable blade pitch angle used for determining pitch angle during steady state/initial condition calculation. It is combined with the MaximumSteadyStatePitchAngle to define the allowable pitch range. Additionally, the external controller API can access this value.

    MaximumSteadyStatePitchAngle : float
        This value represents the minimum allowable blade pitch angle used for determining pitch angle during steady state/initial condition calculation. It is combined with the MinimumSteadyStatePitchAngle to define the allowable pitch range. Please note that the steady-state algorithm does not support overspeed steady state conditions in cases where rotor speeds exceed the specified value for FullLoadOperation::GeneratorSpeed. Additionally, this value is accessible via the external controller API.

    MinimumExternalControllerPitchRate : float
        A value that will be exposed through the external controller API. The user may choose to use or ignore it. Bladed is not using this value internally.

    MaximumExternalControllerPitchRate : float
        A value that will be exposed through the external controller API. The user may choose to use or ignore it. Bladed is not using this value internally.

    NominalHubWindSpeedVsMinimumSteadyStatePitchAngle : List[NominalHubWindSpeedVsMinimumSteadyStatePitchAngle], default=list()
        The look-up table for specifying hub wind speed against the respective minimum pitch angle for pitch scheduling. Wind speeds need to be in monotonic ascending order. Linear interpolation is used between points. If the hub wind speed exceeds the specified value the nearest will be used and a warning message will be written.

    PartialLoadOperation : PartialLoadOperation

    FullLoadOperation : FullLoadOperation

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Turbine/TurbineOperationalParameters/VariableSpeedPitchRegulatedControlModel/VariableSpeedPitchRegulatedControlModel.json')
    
    MinimumSteadyStatePitchAngle: Optional[float] = Field(alias="MinimumSteadyStatePitchAngle", default=None)
    MaximumSteadyStatePitchAngle: Optional[float] = Field(alias="MaximumSteadyStatePitchAngle", default=None)
    MinimumExternalControllerPitchRate: Optional[float] = Field(alias="MinimumExternalControllerPitchRate", default=None)
    MaximumExternalControllerPitchRate: Optional[float] = Field(alias="MaximumExternalControllerPitchRate", default=None)
    NominalHubWindSpeedVsMinimumSteadyStatePitchAngle: Optional[List[NominalHubWindSpeedVsMinimumSteadyStatePitchAngle]] = Field(alias="NominalHubWindSpeedVsMinimumSteadyStatePitchAngle", default=list())
    PartialLoadOperation: Optional[PartialLoadOperation] = Field(alias="PartialLoadOperation", default=None)
    FullLoadOperation: Optional[FullLoadOperation] = Field(alias="FullLoadOperation", default=None)

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
        VariableSpeedPitchRegulatedControlModel
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = VariableSpeedPitchRegulatedControlModel.from_file('/path/to/file')
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
        VariableSpeedPitchRegulatedControlModel
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = VariableSpeedPitchRegulatedControlModel.from_json('{ ... }')
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
        VariableSpeedPitchRegulatedControlModel
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


VariableSpeedPitchRegulatedControlModel.update_forward_refs()
