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

from dnv_bladed_models.brake import Brake

from dnv_bladed_models.component import Component

from dnv_bladed_models.drivetrain_and_nacelle_mass_properties import DrivetrainAndNacelleMassProperties

from dnv_bladed_models.drivetrain_connectable_nodes import DrivetrainConnectableNodes

from dnv_bladed_models.drivetrain_output_group_library import DrivetrainOutputGroupLibrary

from dnv_bladed_models.high_speed_shaft_flexibility import HighSpeedShaftFlexibility

from dnv_bladed_models.low_speed_shaft import LowSpeedShaft

from dnv_bladed_models.mechanical_losses import MechanicalLosses

from dnv_bladed_models.nacelle_cover import NacelleCover

from dnv_bladed_models.nacelle_sensors import NacelleSensors

from dnv_bladed_models.pallet_mounting_flexibility import PalletMountingFlexibility

from dnv_bladed_models.position_of_hub_centre import PositionOfHubCentre

from dnv_bladed_models.slipping_clutch import SlippingClutch



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class DrivetrainAndNacelle(Component, ComponentType='DrivetrainAndNacelle'):
    r"""
    A drivetrain component.  This includes the gearbox; all shafts and brakes right up to the hub centre; the mainframe of the nacelle; all fairings and ancilliary items on the nacelle.  It excludes the generator.
    
    Attributes:
    ----------
    ComponentType : str, default='DrivetrainAndNacelle'
        Defines the specific type of Component model in use.  For a `DrivetrainAndNacelle` object, this must always be set to a value of `DrivetrainAndNacelle`.

    PositionOfHubCentre : PositionOfHubCentre

    NacelleCover : NacelleCover

    MassProperties : DrivetrainAndNacelleMassProperties

    Sensors : NacelleSensors, Not supported yet

    ShaftBrakes : List[Brake], default=list()
        Definitions for the brakes on the various shafts of the drivetrain.

    GearboxRatio : float
        The ratio of the high speed shaft (connected to the generator) to the low speed shaft (connected to the hub). Negative values cause the low-speed shaft and high-speed shaft to rotate in opposite directions.

    GearboxInertia : float
        The total rotational inertia of the gearbox, referred to the high speed side.

    SlippingClutch : SlippingClutch

    HighSpeedShaftTorsion : HighSpeedShaftFlexibility

    MountingFlexibility : PalletMountingFlexibility

    LowSpeedShaft : LowSpeedShaft

    Losses : MechanicalLosses

    OutputGroups : DrivetrainOutputGroupLibrary, Not supported yet

    ConnectableNodes : DrivetrainConnectableNodes, Not supported yet

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/DrivetrainAndNacelle/DrivetrainAndNacelle.json')
    
    ComponentType: Optional[str] = Field(alias="ComponentType", default='DrivetrainAndNacelle')
    PositionOfHubCentre: Optional[PositionOfHubCentre] = Field(alias="PositionOfHubCentre", default=None)
    NacelleCover: Optional[NacelleCover] = Field(alias="NacelleCover", default=None)
    MassProperties: Optional[DrivetrainAndNacelleMassProperties] = Field(alias="MassProperties", default=None)
    Sensors: Optional[NacelleSensors] = Field(alias="Sensors", default=NacelleSensors()) # Not supported yet
    ShaftBrakes: Optional[List[Brake]] = Field(alias="ShaftBrakes", default=list())
    GearboxRatio: Optional[float] = Field(alias="GearboxRatio", default=None)
    GearboxInertia: Optional[float] = Field(alias="GearboxInertia", default=None)
    SlippingClutch: Optional[SlippingClutch] = Field(alias="SlippingClutch", default=None)
    HighSpeedShaftTorsion: Optional[HighSpeedShaftFlexibility] = Field(alias="HighSpeedShaftTorsion", default=None)
    MountingFlexibility: Optional[PalletMountingFlexibility] = Field(alias="MountingFlexibility", default=None)
    LowSpeedShaft: Optional[LowSpeedShaft] = Field(alias="LowSpeedShaft", default=None)
    Losses: Optional[MechanicalLosses] = Field(alias="Losses", default=None)
    OutputGroups: Optional[DrivetrainOutputGroupLibrary] = Field(alias="OutputGroups", default=DrivetrainOutputGroupLibrary()) # Not supported yet
    ConnectableNodes: Optional[DrivetrainConnectableNodes] = Field(alias="ConnectableNodes", default=DrivetrainConnectableNodes()) # Not supported yet

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
        DrivetrainAndNacelle
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DrivetrainAndNacelle.from_file('/path/to/file')
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
        DrivetrainAndNacelle
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = DrivetrainAndNacelle.from_json('{ ... }')
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
        DrivetrainAndNacelle
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


DrivetrainAndNacelle.update_forward_refs()
