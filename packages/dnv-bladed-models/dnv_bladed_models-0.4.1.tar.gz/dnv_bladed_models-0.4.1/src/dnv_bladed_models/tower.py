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

from dnv_bladed_models.added_inertia import AddedInertia

from dnv_bladed_models.structure import Structure

from dnv_bladed_models.tower_aerodynamic_properties import TowerAerodynamicProperties

from dnv_bladed_models.tower_can import TowerCan

from dnv_bladed_models.tower_connectable_nodes import TowerConnectableNodes

from dnv_bladed_models.tower_hydrodynamic_properties import TowerHydrodynamicProperties

from dnv_bladed_models.tower_materials_library import TowerMaterialsLibrary

from dnv_bladed_models.tower_output_group_library import TowerOutputGroupLibrary

from dnv_bladed_models.tower_sensors import TowerSensors



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Tower(Structure, ComponentType='Tower'):
    r"""
    An axisymmetric tower, made from a series of tower \&quot;cans\&quot;.
    
    Attributes:
    ----------
    ComponentType : str, default='Tower'
        Defines the specific type of Component model in use.  For a `Tower` object, this must always be set to a value of `Tower`.

    MaterialsLibrary : TowerMaterialsLibrary

    Cans : List[TowerCan], default=list()
        A list of cans, each one sitting on the top of the previous one.  These cans can be constant-section or tapered.

    AerodynamicProperties : TowerAerodynamicProperties

    HydrodynamicProperties : TowerHydrodynamicProperties, Not supported yet

    PointInertias : List[AddedInertia], default=list()
        A list of additional inertias to add to the tower.

    OutputGroups : TowerOutputGroupLibrary, Not supported yet

    ConnectableNodes : TowerConnectableNodes, Not supported yet

    Sensors : TowerSensors, Not supported yet

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/Tower/Tower.json')
    
    ComponentType: Optional[str] = Field(alias="ComponentType", default='Tower')
    MaterialsLibrary: Optional[TowerMaterialsLibrary] = Field(alias="MaterialsLibrary", default=TowerMaterialsLibrary())
    Cans: Optional[List[TowerCan]] = Field(alias="Cans", default=list())
    AerodynamicProperties: Optional[TowerAerodynamicProperties] = Field(alias="AerodynamicProperties", default=None)
    HydrodynamicProperties: Optional[TowerHydrodynamicProperties] = Field(alias="HydrodynamicProperties", default=None) # Not supported yet
    PointInertias: Optional[List[AddedInertia]] = Field(alias="PointInertias", default=list())
    OutputGroups: Optional[TowerOutputGroupLibrary] = Field(alias="OutputGroups", default=TowerOutputGroupLibrary()) # Not supported yet
    ConnectableNodes: Optional[TowerConnectableNodes] = Field(alias="ConnectableNodes", default=TowerConnectableNodes()) # Not supported yet
    Sensors: Optional[TowerSensors] = Field(alias="Sensors", default=TowerSensors()) # Not supported yet

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
        Tower
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Tower.from_file('/path/to/file')
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
        Tower
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Tower.from_json('{ ... }')
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
        Tower
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


Tower.update_forward_refs()
