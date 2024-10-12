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

from dnv_bladed_models.angle_vs_stiffness_torque import AngleVsStiffnessTorque

from dnv_bladed_models.damper import Damper

from dnv_bladed_models.pendulum_damper_mounting_position import PendulumDamperMountingPosition

from dnv_bladed_models.velocity_vs_damping_torque import VelocityVsDampingTorque



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class PendulumDamper(Damper, ComponentType='PendulumDamper'):
    r"""
    A \&quot;pendulum\&quot; or \&quot;tuned mass\&quot; damper, which uses a suspended mass to damp oscillations in a tower.
    
    Not supported yet.
    
    Attributes:
    ----------
    ComponentType : str, default='PendulumDamper', Not supported yet
        Defines the specific type of Component model in use.  For a `PendulumDamper` object, this must always be set to a value of `PendulumDamper`.

    Length : float, Not supported yet
        The length of the (rigid) pendulum arm.

    Mass : float, Not supported yet
        The mass suspended at the end of the pendulum arm.

    Inertia : float, Not supported yet
        Any added inertia for the pendulum.

    Stiffness : float, Not supported yet
        The constant stiffness term for the hinge of the pendulum.  This is in addition to the non-linear terms defined in the AngleVsStiffnessTorque parameter.

    Damping : float, Not supported yet
        The constant damping term for the hinge of the pendulum.  This is in addition to the non-linear terms defined in the VelocityVsDampingTorque parameter.

    InitialAngle : float, Not supported yet
        The initial angle of the pendulum at the beginning of the simulation.

    ConstantFriction : float, Not supported yet
        The constant friction torque applied to rotational hinge.  Any other friction contributions will be in addition to this.

    AngleVsStiffnessTorque : List[AngleVsStiffnessTorque], default=list(), Not supported yet
        A look-up table of additional stiffnesses that vary with the pendulum's position.

    VelocityVsDampingTorque : List[VelocityVsDampingTorque], default=list(), Not supported yet
        A look-up table of additional damping that vary with the pendulum's velocity.

    MountingPosition : PendulumDamperMountingPosition, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Damper/PendulumDamper.json')
    
    ComponentType: Optional[str] = Field(alias="ComponentType", default='PendulumDamper') # Not supported yet
    Length: Optional[float] = Field(alias="Length", default=None) # Not supported yet
    Mass: Optional[float] = Field(alias="Mass", default=None) # Not supported yet
    Inertia: Optional[float] = Field(alias="Inertia", default=None) # Not supported yet
    Stiffness: Optional[float] = Field(alias="Stiffness", default=None) # Not supported yet
    Damping: Optional[float] = Field(alias="Damping", default=None) # Not supported yet
    InitialAngle: Optional[float] = Field(alias="InitialAngle", default=None) # Not supported yet
    ConstantFriction: Optional[float] = Field(alias="ConstantFriction", default=None) # Not supported yet
    AngleVsStiffnessTorque: Optional[List[AngleVsStiffnessTorque]] = Field(alias="AngleVsStiffnessTorque", default=list()) # Not supported yet
    VelocityVsDampingTorque: Optional[List[VelocityVsDampingTorque]] = Field(alias="VelocityVsDampingTorque", default=list()) # Not supported yet
    MountingPosition: Optional[PendulumDamperMountingPosition] = Field(alias="MountingPosition", default=None) # Not supported yet

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
        PendulumDamper
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PendulumDamper.from_file('/path/to/file')
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
        PendulumDamper
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = PendulumDamper.from_json('{ ... }')
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
        PendulumDamper
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


PendulumDamper.update_forward_refs()
