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

from dnv_bladed_models.aerofoil_library import AerofoilLibrary

from dnv_bladed_models.aileron_aerofoil_library import AileronAerofoilLibrary

from dnv_bladed_models.blade_additional_inertia import BladeAdditionalInertia

from dnv_bladed_models.blade_modelling import BladeModelling

from dnv_bladed_models.blade_output_group_library import BladeOutputGroupLibrary

from dnv_bladed_models.blade_section_definition import BladeSectionDefinition

from dnv_bladed_models.blade_sensors import BladeSensors

from dnv_bladed_models.component import Component

from dnv_bladed_models.interpolated_aerofoil_library import InterpolatedAerofoilLibrary

from dnv_bladed_models.mounting import Mounting



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Blade(Component, ComponentType='Blade'):
    r"""
    A blade component.
    
    Attributes:
    ----------
    ComponentType : str, default='Blade'
        Defines the specific type of Component model in use.  For a `Blade` object, this must always be set to a value of `Blade`.

    Modelling : BladeModelling, abstract

    AerofoilLibrary : AerofoilLibrary

    InterpolatedAerofoilLibrary : InterpolatedAerofoilLibrary

    AileronAerofoilLibrary : AileronAerofoilLibrary, Not supported yet

    Mounting : Mounting

    ToleranceForRepeatedSections : float, default=0.001
        The tolerance used to determine whether two blade sections are merely adjacent, or represent a step-change in properties at a discrete point.  If the plane point of the reference axes lie within this distance of each other, then it will be taken that the two blade section definitions represent the properties inboard and outboard of a single structural point.

    SectionDefinitions : List[BladeSectionDefinition], default=list()
        A list of section definitions which describle the aerodynamic and structural properties of the blade.

    AdditionalInertia : BladeAdditionalInertia

    OutputGroups : BladeOutputGroupLibrary, Not supported yet

    Sensors : BladeSensors, Not supported yet

    Notes:
    -----
    Modelling has the following concrete types:
        - FiniteElementBladeModelling
        - ModalBladeModelling
        - RigidBladeModelling
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/Blade.json')
    
    ComponentType: Optional[str] = Field(alias="ComponentType", default='Blade')
    Modelling: Optional[BladeModelling] = Field(alias="Modelling", default=None)
    AerofoilLibrary: Optional[AerofoilLibrary] = Field(alias="AerofoilLibrary", default=AerofoilLibrary())
    InterpolatedAerofoilLibrary: Optional[InterpolatedAerofoilLibrary] = Field(alias="InterpolatedAerofoilLibrary", default=InterpolatedAerofoilLibrary())
    AileronAerofoilLibrary: Optional[AileronAerofoilLibrary] = Field(alias="AileronAerofoilLibrary", default=AileronAerofoilLibrary()) # Not supported yet
    Mounting: Optional[Mounting] = Field(alias="Mounting", default=None)
    ToleranceForRepeatedSections: Optional[float] = Field(alias="ToleranceForRepeatedSections", default=0.001)
    SectionDefinitions: Optional[List[BladeSectionDefinition]] = Field(alias="SectionDefinitions", default=list())
    AdditionalInertia: Optional[BladeAdditionalInertia] = Field(alias="AdditionalInertia", default=None)
    OutputGroups: Optional[BladeOutputGroupLibrary] = Field(alias="OutputGroups", default=BladeOutputGroupLibrary()) # Not supported yet
    Sensors: Optional[BladeSensors] = Field(alias="Sensors", default=BladeSensors()) # Not supported yet

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
        Blade
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Blade.from_file('/path/to/file')
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
        Blade
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Blade.from_json('{ ... }')
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
        Blade
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


Blade.update_forward_refs()
