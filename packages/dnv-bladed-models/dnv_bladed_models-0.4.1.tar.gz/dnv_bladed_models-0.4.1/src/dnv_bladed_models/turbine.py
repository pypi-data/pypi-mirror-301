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

from dnv_bladed_models.assembly import Assembly

from dnv_bladed_models.bladed_control import BladedControl

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.electrical_grid import ElectricalGrid

from dnv_bladed_models.external_module import ExternalModule

from dnv_bladed_models.turbine_operational_parameters import TurbineOperationalParameters



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Turbine(BladedModel):
    r"""
    The definition of the turbine and its installation that is to be modelled.
    
    Attributes:
    ----------
    ElectricalGrid : ElectricalGrid, Not supported yet

    TurbineOperationalParameters : TurbineOperationalParameters

    Control : BladedControl, Not supported yet

    GlobalExternalModules : List[ExternalModule], default=list(), Not supported yet
        A list of any external modules that will be run with the time domain simulations.  It is expected that external modules defined here will interact with more than one area of the turbine, such as to apply additional aerodynamics loads to the entire structure.  Any external modules that represent a single component should be added to the Assembly tree.

    MeanSeaLevel : float, default=0
        The mean sea depth at the turbine location.  If omited, the Turbine will be considered an on-shore turbine and any sea states will be ignored.

    Assembly : Assembly

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Turbine/Turbine.json')
    
    ElectricalGrid: Optional[ElectricalGrid] = Field(alias="ElectricalGrid", default=None) # Not supported yet
    TurbineOperationalParameters: Optional[TurbineOperationalParameters] = Field(alias="TurbineOperationalParameters", default=None)
    Control: Optional[BladedControl] = Field(alias="Control", default=None) # Not supported yet
    GlobalExternalModules: Optional[List[ExternalModule]] = Field(alias="GlobalExternalModules", default=list()) # Not supported yet
    MeanSeaLevel: Optional[float] = Field(alias="MeanSeaLevel", default=0)
    Assembly: Optional[Assembly] = Field(alias="Assembly", default=Assembly())

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
        Turbine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Turbine.from_file('/path/to/file')
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
        Turbine
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Turbine.from_json('{ ... }')
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
        Turbine
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


Turbine.update_forward_refs()
