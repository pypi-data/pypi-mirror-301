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



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class NominalHubWindSpeedVsRotorSpeedAndPitchAngle(BladedModel):
    r"""
    The look-up table for specifying the nominal free-field wind speed at the hub against the turbine&#39;s operating condition appropriate for that wind speed.  Wind speeds need to be in monotonic ascending order. Linear interpolation is used between points. The lowest value for the hub wind speed will be taken as the cut-in wind speed for the turbine, and the highest the cut-out wind speed.
    
    Attributes:
    ----------
    NominalHubWindSpeed : float
        The nominal free-field wind speed at the hub.

    RotorSpeed : float
        The rotor speed to apply for the specified hub wind speed in steady state/initial condition calculations. The generator torque will be calculated to achieve this rotor speed.  If the torque required is negative, a warning will be generated.

    PitchAngle : float
        The pitch angle to apply to all blades for the specified hub wind speed in steady state/initial condition calculations.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Turbine/TurbineOperationalParameters/NominalHubWindSpeedVsRotorSpeedAndPitchAngle/NominalHubWindSpeedVsRotorSpeedAndPitchAngle.json')
    
    NominalHubWindSpeed: Optional[float] = Field(alias="NominalHubWindSpeed", default=None)
    RotorSpeed: Optional[float] = Field(alias="RotorSpeed", default=None)
    PitchAngle: Optional[float] = Field(alias="PitchAngle", default=None)

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
        NominalHubWindSpeedVsRotorSpeedAndPitchAngle
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = NominalHubWindSpeedVsRotorSpeedAndPitchAngle.from_file('/path/to/file')
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
        NominalHubWindSpeedVsRotorSpeedAndPitchAngle
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = NominalHubWindSpeedVsRotorSpeedAndPitchAngle.from_json('{ ... }')
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
        NominalHubWindSpeedVsRotorSpeedAndPitchAngle
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


NominalHubWindSpeedVsRotorSpeedAndPitchAngle.update_forward_refs()
