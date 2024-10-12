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

from dnv_bladed_models.shaft_input_power_vs_power_loss import ShaftInputPowerVsPowerLoss

from dnv_bladed_models.shaft_input_torque_vs_resisting_torque import ShaftInputTorqueVsResistingTorque

from dnv_bladed_models.shaft_speed_vs_shaft_input_power_vs_power_loss import ShaftSpeedVsShaftInputPowerVsPowerLoss

from dnv_bladed_models.shaft_speed_vs_shaft_input_torque_vs_resisting_torque import ShaftSpeedVsShaftInputTorqueVsResistingTorque



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class MechanicalLosses(BladedModel):
    r"""
    The common properties for the mechanical losses in the drivetrain.
    
    Attributes:
    ----------
    ShaftSpeedVsShaftInputTorqueVsResistingTorque : List[ShaftSpeedVsShaftInputTorqueVsResistingTorque], default=list()
        A series of look-up tables for the losses, each valid for the specified shaft speed.

    ShaftInputTorqueVsResistingTorque : List[ShaftInputTorqueVsResistingTorque], default=list()
        A look-up table for the losses, each valid for the specified input torque.

    ShaftSpeedVsShaftInputPowerVsPowerLoss : List[ShaftSpeedVsShaftInputPowerVsPowerLoss], default=list()
        A series of look-up tables for the losses, each valid for the specified shaft rotational speed.

    ShaftInputPowerVsPowerLoss : List[ShaftInputPowerVsPowerLoss], default=list()
        A series of look-up tables for the losses, each valid for the specified shaft rotational speed.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/DrivetrainAndNacelle/MechanicalLosses/MechanicalLosses.json')
    
    ShaftSpeedVsShaftInputTorqueVsResistingTorque: Optional[List[ShaftSpeedVsShaftInputTorqueVsResistingTorque]] = Field(alias="ShaftSpeedVsShaftInputTorqueVsResistingTorque", default=list())
    ShaftInputTorqueVsResistingTorque: Optional[List[ShaftInputTorqueVsResistingTorque]] = Field(alias="ShaftInputTorqueVsResistingTorque", default=list())
    ShaftSpeedVsShaftInputPowerVsPowerLoss: Optional[List[ShaftSpeedVsShaftInputPowerVsPowerLoss]] = Field(alias="ShaftSpeedVsShaftInputPowerVsPowerLoss", default=list())
    ShaftInputPowerVsPowerLoss: Optional[List[ShaftInputPowerVsPowerLoss]] = Field(alias="ShaftInputPowerVsPowerLoss", default=list())

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
        MechanicalLosses
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MechanicalLosses.from_file('/path/to/file')
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
        MechanicalLosses
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MechanicalLosses.from_json('{ ... }')
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
        MechanicalLosses
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


MechanicalLosses.update_forward_refs()
