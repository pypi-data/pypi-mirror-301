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

class LowSpeedShaft(BladedModel):
    r"""
    The low speed shaft bending definition.
    
    Attributes:
    ----------
    EffectiveShaftLength : float
        The length of the low speed shaft to be considered for the bending model, beginning at the outside face of the main bearing.

    HingePosition : float
        The fraction of the low speed shaft length (from the hub centre) where the hinge between the two massless rigid shafts are connected.

    TorsionalStiffness : float
        The shaft stiffness about the axis of rotation.

    TorsionalDamping : float
        The shaft damping about the axis of rotation.

    BendingStiffness : float
        The shaft's bending stiffness about any axis perpendicular to the axis of rotation.

    BendingDamping : float
        The shaft's bending damping about any axis perpendicular to the axis of rotation.

    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/DrivetrainAndNacelle/LowSpeedShaft/LowSpeedShaft.json')
    
    EffectiveShaftLength: Optional[float] = Field(alias="EffectiveShaftLength", default=None)
    HingePosition: Optional[float] = Field(alias="HingePosition", default=None)
    TorsionalStiffness: Optional[float] = Field(alias="TorsionalStiffness", default=None)
    TorsionalDamping: Optional[float] = Field(alias="TorsionalDamping", default=None)
    BendingStiffness: Optional[float] = Field(alias="BendingStiffness", default=None)
    BendingDamping: Optional[float] = Field(alias="BendingDamping", default=None)

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
        LowSpeedShaft
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LowSpeedShaft.from_file('/path/to/file')
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
        LowSpeedShaft
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = LowSpeedShaft.from_json('{ ... }')
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
        LowSpeedShaft
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


LowSpeedShaft.update_forward_refs()
