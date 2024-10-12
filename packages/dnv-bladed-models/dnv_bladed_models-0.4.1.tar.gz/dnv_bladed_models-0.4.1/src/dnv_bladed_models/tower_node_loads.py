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

class TowerNodeLoads(BladedModel):
    r"""
    The moments and forces to output for any node location where the loads are requested.
    
    Not supported yet.
    
    Attributes:
    ----------
    Mx : bool, default=False, Not supported yet
        If true, the moment about the X axis will be output.

    My : bool, default=False, Not supported yet
        If true, the moment about the Y axis will be output.

    Mz : bool, default=False, Not supported yet
        If true, the moment about the Z axis will be output.

    Mxy : bool, Not supported yet
        If true, the maximum moment about any axis that lies in the XY plane will be output.

    Fx : bool, default=False, Not supported yet
        If true, the force in the X direction will be output.

    Fy : bool, default=False, Not supported yet
        If true, the force in the Y direction will be output.

    Fz : bool, default=False, Not supported yet
        If true, the force in the Z direction will be output.

    Fxy : bool, Not supported yet
        If true, the maximum force along any axis that lies in the XY plane will be output.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Tower/TowerOutputGroupLibrary/TowerOutputGroup/TowerNodeLoads/TowerNodeLoads.json')
    
    Mx: Optional[bool] = Field(alias="Mx", default=False) # Not supported yet
    My: Optional[bool] = Field(alias="My", default=False) # Not supported yet
    Mz: Optional[bool] = Field(alias="Mz", default=False) # Not supported yet
    Mxy: Optional[bool] = Field(alias="Mxy", default=None) # Not supported yet
    Fx: Optional[bool] = Field(alias="Fx", default=False) # Not supported yet
    Fy: Optional[bool] = Field(alias="Fy", default=False) # Not supported yet
    Fz: Optional[bool] = Field(alias="Fz", default=False) # Not supported yet
    Fxy: Optional[bool] = Field(alias="Fxy", default=None) # Not supported yet

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
        TowerNodeLoads
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TowerNodeLoads.from_file('/path/to/file')
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
        TowerNodeLoads
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TowerNodeLoads.from_json('{ ... }')
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
        TowerNodeLoads
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


TowerNodeLoads.update_forward_refs()
