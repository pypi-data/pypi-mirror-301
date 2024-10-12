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

from dnv_bladed_models.lidar_beam import LidarBeam

from dnv_bladed_models.lidar_focal_distance_control import LidarFocalDistanceControl

from dnv_bladed_models.lidar_scanning_pattern import LidarScanningPattern

from dnv_bladed_models.look_up_table_element import LookUpTableElement



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Lidar(Component, ComponentType='Lidar'):
    r"""
    A Lidar sensor mounted on the scructure.
    
    Not supported yet.
    
    Attributes:
    ----------
    ComponentType : str, default='Lidar', Not supported yet
        Defines the specific type of Component model in use.  For a `Lidar` object, this must always be set to a value of `Lidar`.

    LensArea : float, Not supported yet
        The area of the lens.

    LaserWavelength : float, Not supported yet
        The wavelength of the laser.

    WeightingFunction : List[LookUpTableElement], default=list(), Not supported yet
        The relationship between the distance from the focal point and the weighting to put on the sample.  Every Lidar sampling point has a finite width, where velocities are collected to either side of the nominal focal distance.  This relationship is used to put more weight on those samples closest to the nominal focal point.

    LidarBeams : List[LidarBeam], default=list(), Not supported yet
        The definition of the lidar beams.

    ScanningPattern : LidarScanningPattern, abstract, Not supported yet

    FocalDistanceControl : LidarFocalDistanceControl, abstract, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    ScanningPattern has the following concrete types:
        - CircularLidarScan
        - LidarControllerScan
        - RosetteLidarScan
    
    FocalDistanceControl has the following concrete types:
        - ControllerLidarSettings
        - MultipleLidarFocalDistances
        - SingleLidarFocalDistance
    
    """
    _relative_schema_path: str = PrivateAttr('Components/Lidar/Lidar.json')
    
    ComponentType: Optional[str] = Field(alias="ComponentType", default='Lidar') # Not supported yet
    LensArea: Optional[float] = Field(alias="LensArea", default=None) # Not supported yet
    LaserWavelength: Optional[float] = Field(alias="LaserWavelength", default=None) # Not supported yet
    WeightingFunction: Optional[List[LookUpTableElement]] = Field(alias="WeightingFunction", default=list()) # Not supported yet
    LidarBeams: Optional[List[LidarBeam]] = Field(alias="LidarBeams", default=list()) # Not supported yet
    ScanningPattern: Optional[LidarScanningPattern] = Field(alias="ScanningPattern", default=None) # Not supported yet
    FocalDistanceControl: Optional[LidarFocalDistanceControl] = Field(alias="FocalDistanceControl", default=None) # Not supported yet

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
        Lidar
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Lidar.from_file('/path/to/file')
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
        Lidar
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = Lidar.from_json('{ ... }')
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
        Lidar
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


Lidar.update_forward_refs()
