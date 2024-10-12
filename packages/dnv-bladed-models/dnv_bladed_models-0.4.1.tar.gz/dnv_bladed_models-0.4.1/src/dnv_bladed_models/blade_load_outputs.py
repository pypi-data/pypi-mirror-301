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

class BladeLoadOutputs(BladedModel):
    r"""
    Loads selected
    
    Not supported yet.
    
    Attributes:
    ----------
    FlapwiseBendingLoads : bool, default=False, Not supported yet
        Output blade bending moments for the flapwise direction (0=no, 1=yes).

    EdgewiseBendingLoads : bool, default=False, Not supported yet
        Output blade bending moments for the edgewise direction (0=no, 1=yes).

    FlapwiseShearLoads : bool, default=False, Not supported yet
        Output blade shear forces for the flapwise direction (0=no, 1=yes).

    EdgewiseShearLoads : bool, default=False, Not supported yet
        Output blade shear forces for the edgewise direction (0=no, 1=yes).

    OutOfPlaneBendingLoads : bool, default=False, Not supported yet
        Output blade bending moments for out of plane direction (0=no, 1=yes).

    InPlaneBendingLoads : bool, default=False, Not supported yet
        Output blade bending moments for in plane direction (0=no, 1=yes).

    OutOfPlaneShearLoads : bool, default=False, Not supported yet
        Output blade shear forces for out of plane direction (0=no, 1=yes).

    InPlaneShearLoads : bool, default=False, Not supported yet
        Output blade shear forces for in plane direction (0=no, 1=yes).

    RadialForces : bool, default=False, Not supported yet
        Output blade radial forces (0=no, 1=yes).

    LoadsInRootAxisSystem : bool, default=False, Not supported yet
        Output blade loads about the root axes system (0=no, 1=yes).

    LoadsInAeroAxisSystem : bool, default=False, Not supported yet
        Output blade loads about the aero axes system (0=no, 1=yes).

    LoadsInUserAxisSystem : bool, default=False, Not supported yet
        Output blade loads about the user defined axes system (0=no, 1=yes).

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/BladeOutputGroupLibrary/BladeOutputGroup/BladeLoadOutputs/BladeLoadOutputs.json')
    
    FlapwiseBendingLoads: Optional[bool] = Field(alias="FlapwiseBendingLoads", default=False) # Not supported yet
    EdgewiseBendingLoads: Optional[bool] = Field(alias="EdgewiseBendingLoads", default=False) # Not supported yet
    FlapwiseShearLoads: Optional[bool] = Field(alias="FlapwiseShearLoads", default=False) # Not supported yet
    EdgewiseShearLoads: Optional[bool] = Field(alias="EdgewiseShearLoads", default=False) # Not supported yet
    OutOfPlaneBendingLoads: Optional[bool] = Field(alias="OutOfPlaneBendingLoads", default=False) # Not supported yet
    InPlaneBendingLoads: Optional[bool] = Field(alias="InPlaneBendingLoads", default=False) # Not supported yet
    OutOfPlaneShearLoads: Optional[bool] = Field(alias="OutOfPlaneShearLoads", default=False) # Not supported yet
    InPlaneShearLoads: Optional[bool] = Field(alias="InPlaneShearLoads", default=False) # Not supported yet
    RadialForces: Optional[bool] = Field(alias="RadialForces", default=False) # Not supported yet
    LoadsInRootAxisSystem: Optional[bool] = Field(alias="LoadsInRootAxisSystem", default=False) # Not supported yet
    LoadsInAeroAxisSystem: Optional[bool] = Field(alias="LoadsInAeroAxisSystem", default=False) # Not supported yet
    LoadsInUserAxisSystem: Optional[bool] = Field(alias="LoadsInUserAxisSystem", default=False) # Not supported yet

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
        BladeLoadOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladeLoadOutputs.from_file('/path/to/file')
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
        BladeLoadOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = BladeLoadOutputs.from_json('{ ... }')
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
        BladeLoadOutputs
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


BladeLoadOutputs.update_forward_refs()
