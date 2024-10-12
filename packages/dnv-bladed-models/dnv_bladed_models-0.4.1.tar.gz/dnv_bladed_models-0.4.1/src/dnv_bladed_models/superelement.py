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

from dnv_bladed_models.component import Component

from dnv_bladed_models.interface_load_file import InterfaceLoadFile

from dnv_bladed_models.superelement_connectable_nodes import SuperelementConnectableNodes

from dnv_bladed_models.transformation_matrix import TransformationMatrix



class Superelement_WaveLoadingUnitsInFileEnum(str, Enum):
    N = "N"
    K_N = "kN"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Superelement(Component, ComponentType='Superelement'):
    r"""
    A structural superelement, mathematically representing a structural component.
    
    Not supported yet.
    
    Attributes:
    ----------
    ComponentType : str, default='Superelement', Not supported yet
        Defines the specific type of Component model in use.  For a `Superelement` object, this must always be set to a value of `Superelement`.

    DefinitionFilepath : str, Not supported yet
        The filepath of URI to the superelement data.

    WaveLoadingFilepath : str, Not supported yet
        The filepath of URI to the accompanying wave data.

    WaveLoadingUnitsInFile : Superelement_WaveLoadingUnitsInFileEnum, default='kN', Not supported yet
        The units that were used when generating the wave load files.  The industry standard is to provide wave loads in kN and kNm.

    CoordinateTransformationMatrix : TransformationMatrix

    InterfaceLoadFile : InterfaceLoadFile, Not supported yet

    ConnectableNodes : SuperelementConnectableNodes, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Superelement/Superelement.json')
    
    ComponentType: Optional[str] = Field(alias="ComponentType", default='Superelement') # Not supported yet
    DefinitionFilepath: Optional[str] = Field(alias="DefinitionFilepath", default=None) # Not supported yet
    WaveLoadingFilepath: Optional[str] = Field(alias="WaveLoadingFilepath", default=None) # Not supported yet
    WaveLoadingUnitsInFile: Optional[Superelement_WaveLoadingUnitsInFileEnum] = Field(alias="WaveLoadingUnitsInFile", default='kN') # Not supported yet
    CoordinateTransformationMatrix: Optional[TransformationMatrix] = Field(alias="CoordinateTransformationMatrix", default=None)
    InterfaceLoadFile: Optional[InterfaceLoadFile] = Field(alias="InterfaceLoadFile", default=None) # Not supported yet
    ConnectableNodes: Optional[SuperelementConnectableNodes] = Field(alias="ConnectableNodes", default=SuperelementConnectableNodes()) # Not supported yet

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
        Superelement
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Superelement.from_file('/path/to/file')
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
        Superelement
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Superelement.from_json('{ ... }')
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
        Superelement
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


Superelement.update_forward_refs()
