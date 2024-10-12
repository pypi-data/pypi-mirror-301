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

from dnv_bladed_models.blade_section_offset_and_rotated_axes_system import BladeSectionOffsetAndRotatedAxesSystem



class BladeSectionOutputCoordinateSystem_YAxisFollowsEnum(str, Enum):
    COMPONENT_AXIS = "COMPONENT_AXIS"
    REFERENCE_AXIS = "REFERENCE_AXIS"
    AERODYNAMIC_AXIS = "AERODYNAMIC_AXIS"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class BladeSectionOutputCoordinateSystem(BladeSectionOffsetAndRotatedAxesSystem):
    r"""
    This axes system in which outputs will be produced.  This allows the output of loads in a different axis system to any of the physical properties.  If omitted, the reference axes will be used as the mass axes.
    
    Attributes:
    ----------
    YAxisFollows : BladeSectionOutputCoordinateSystem_YAxisFollowsEnum
        The orientation of the x and y axes.  A rotation about the reference z axis can be specified instead.

    ZAxisFollowsNeutralAxis : bool
        If true, the z axis is parallel to the line created by the origins of the neatural axes, and not the z axis of the reference plane.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeSectionDefinition/BladeSectionAxesAndCoordinateSystems/BladeSectionOutputCoordinateSystem/BladeSectionOutputCoordinateSystem.json')
    
    YAxisFollows: Optional[BladeSectionOutputCoordinateSystem_YAxisFollowsEnum] = Field(alias="YAxisFollows", default=None)
    ZAxisFollowsNeutralAxis: Optional[bool] = Field(alias="ZAxisFollowsNeutralAxis", default=None)

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
        BladeSectionOutputCoordinateSystem
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladeSectionOutputCoordinateSystem.from_file('/path/to/file')
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
        BladeSectionOutputCoordinateSystem
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladeSectionOutputCoordinateSystem.from_json('{ ... }')
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
        BladeSectionOutputCoordinateSystem
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


BladeSectionOutputCoordinateSystem.update_forward_refs()
