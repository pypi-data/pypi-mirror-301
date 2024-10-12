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

from dnv_bladed_models.current_direction_shear_variation import CurrentDirectionShearVariation

from dnv_bladed_models.time_vs_current_direction_shear import TimeVsCurrentDirectionShear



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class CurrentDirectionShearTimeHistory(CurrentDirectionShearVariation, DirectionShearVariationType='TimeHistory'):
    r"""
    A time history of the vertical direction shear (veer).  This is a linear relationship between the height and the local direction, with the direction being its nominal value at the reference height.
    
    Not supported yet.
    
    Attributes:
    ----------
    DirectionShearVariationType : str, default='TimeHistory', Not supported yet
        Defines the specific type of DirectionShearVariation model in use.  For a `TimeHistory` object, this must always be set to a value of `TimeHistory`.

    TimeVsDirectionShear : List[TimeVsCurrentDirectionShear], default=list(), Not supported yet
        A list of points specifying the wind veer at the corresponding time.  The wind veer will be interpolated between these points; the wind veer before the first point will be constant at the first point's value; and the wind veer after the last point will remain constant at the last point's value

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/Environment/SeaState/Current/CurrentDirectionShearVariation/CurrentDirectionShearTimeHistory.json')
    
    DirectionShearVariationType: Optional[str] = Field(alias="DirectionShearVariationType", default='TimeHistory') # Not supported yet
    TimeVsDirectionShear: Optional[List[TimeVsCurrentDirectionShear]] = Field(alias="TimeVsDirectionShear", default=list()) # Not supported yet

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
        CurrentDirectionShearTimeHistory
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = CurrentDirectionShearTimeHistory.from_file('/path/to/file')
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
        CurrentDirectionShearTimeHistory
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = CurrentDirectionShearTimeHistory.from_json('{ ... }')
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
        CurrentDirectionShearTimeHistory
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


CurrentDirectionShearTimeHistory.update_forward_refs()
