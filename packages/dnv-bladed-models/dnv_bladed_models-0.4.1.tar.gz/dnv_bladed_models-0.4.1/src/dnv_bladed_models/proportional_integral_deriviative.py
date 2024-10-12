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

from dnv_bladed_models.response_to_demand import ResponseToDemand



class ProportionalIntegralDeriviative_DifferentialGainActionEnum(str, Enum):
    ERROR = "Error"
    FEEDBACK = "Feedback"
    SETPOINT = "Setpoint"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ProportionalIntegralDeriviative(ResponseToDemand, ResponseToDemandType='ProportionalIntegralDeriviative'):
    r"""
    Defines an proportional, integral, deriviative (PID) response to the controller&#39;s demands.
    
    Attributes:
    ----------
    ResponseToDemandType : str, default='ProportionalIntegralDeriviative'
        Defines the specific type of ResponseToDemand model in use.  For a `ProportionalIntegralDeriviative` object, this must always be set to a value of `ProportionalIntegralDeriviative`.

    ProportionalGain : float, default=0
        The gain on the contemporaneous error.

    IntegralGain : float, default=0
        The gain on the integral from time zero till the present of the error signal.

    DifferentialGain : float, default=0
        The gain the filtered derivative of the error.  The derivative of the error is passed through a low-pass filter.

    DifferentialGainAction : ProportionalIntegralDeriviative_DifferentialGainActionEnum, default='Feedback'
        The proportional and integral terms are apllied on error.  Derivative term may also be applied on the feedback or setpoint signals.

    DifferentialGainTimeConstant : float, default=0
        The derivative term uses a low-pass filter on input.

    DesaturationTimeConstant : float, default=0
        The time constant for when the output exceeds the limits.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/PitchSystem/PitchController/PitchSystemDemand/ResponseToDemand/ProportionalIntegralDeriviative.json')
    
    ResponseToDemandType: Optional[str] = Field(alias="ResponseToDemandType", default='ProportionalIntegralDeriviative')
    ProportionalGain: Optional[float] = Field(alias="ProportionalGain", default=0)
    IntegralGain: Optional[float] = Field(alias="IntegralGain", default=0)
    DifferentialGain: Optional[float] = Field(alias="DifferentialGain", default=0)
    DifferentialGainAction: Optional[ProportionalIntegralDeriviative_DifferentialGainActionEnum] = Field(alias="DifferentialGainAction", default='Feedback')
    DifferentialGainTimeConstant: Optional[float] = Field(alias="DifferentialGainTimeConstant", default=0)
    DesaturationTimeConstant: Optional[float] = Field(alias="DesaturationTimeConstant", default=0)

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
        ProportionalIntegralDeriviative
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ProportionalIntegralDeriviative.from_file('/path/to/file')
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
        ProportionalIntegralDeriviative
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ProportionalIntegralDeriviative.from_json('{ ... }')
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
        ProportionalIntegralDeriviative
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


ProportionalIntegralDeriviative.update_forward_refs()
