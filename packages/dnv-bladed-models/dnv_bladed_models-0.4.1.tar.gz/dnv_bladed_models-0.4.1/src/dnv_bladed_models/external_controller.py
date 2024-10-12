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



class ExternalController_CallingConventionEnum(str, Enum):
    CDECL = "__cdecl"
    STDCALL = "__stdcall"

class ExternalController_TimeStepMultiplierEnum(str, Enum):
    EVERY = "Every"
    SECOND = "Second"
    THIRD = "Third"
    FOURTH = "Fourth"
    FIFTH = "Fifth"
    SIXTH = "Sixth"
    SEVENTH = "Seventh"
    EIGTH = "Eigth"
    NINTH = "Ninth"
    TENTH = "Tenth"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ExternalController(BladedModel):
    r"""
    A definition of a single controller for the turbine.
    
    Not supported yet.
    
    Attributes:
    ----------
    Filepath : str, Not supported yet
        The location of the external controller dll.

    CallingConvention : ExternalController_CallingConventionEnum, default='__cdecl', Not supported yet
        The calling convention to be used when calling the external controller.  The default for all C-family languages is '__cdecl'.  The default for FORTRAN is '__stdcall' unless the [C] qualifier is specfied immediately after the function name.  Specifying the wrong calling convention can lead to unexplained system exceptions when attempting to call the external controller.

    FunctionName : str, default='ExternalController', Not supported yet
        The name of the function in the dll to run.  This must satisfy the standard external controller typedef, found in the ExternalControllerApi.h.

    PassParametersByFile : bool, default=False, Not supported yet
        If true, a file will be written containing the parameters in the above box.  The location of this file can be obtained in the external controller using the function GetInfileFilepath.  The name of this file will be \"DISCON.IN\" if there is only one controller, or of the pattern \"DISCONn.IN\", where 'n' is the number of the controller.  If not checked (the default), this string will be directly available using the function GetUserParameters.

    ForceLegacy : bool, default=False, Not supported yet
        If true, only the old-style 'DISCON' function will be looked for in the controller, and raise an error if it cannot be found.  This is only used for testing legacy controllers where both CONTROLLER and DISCON functions are both defined, but the DISCON function is required.

    TimeStepMultiplier : ExternalController_TimeStepMultiplierEnum, default='Every', Not supported yet
        Whether the controller should be called on every discrete timestep, set above.

    Parameters : Dict[str, Any], Not supported yet
        JSON data that will be passed to the constructor of the external module.

    UseFloatingPointProtection : bool, default=True, Not supported yet
        If true, this will apply floating point protection when calling the external controllers.  When the protection is on, any floating point errors are trapped and reported.  When this is switched off, the behaviour will default to that of the computer's floating point machine, but this can often be to not report the error, and to use a semi-random (but often very large) number instead of the correct result.  This can lead to unrepeatable results and numeric errors.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Turbine/BladedControl/ExternalController/ExternalController.json')
    
    Filepath: Optional[str] = Field(alias="Filepath", default=None) # Not supported yet
    CallingConvention: Optional[ExternalController_CallingConventionEnum] = Field(alias="CallingConvention", default='__cdecl') # Not supported yet
    FunctionName: Optional[str] = Field(alias="FunctionName", default='ExternalController') # Not supported yet
    PassParametersByFile: Optional[bool] = Field(alias="PassParametersByFile", default=False) # Not supported yet
    ForceLegacy: Optional[bool] = Field(alias="ForceLegacy", default=False) # Not supported yet
    TimeStepMultiplier: Optional[ExternalController_TimeStepMultiplierEnum] = Field(alias="TimeStepMultiplier", default='Every') # Not supported yet
    Parameters: Optional[Dict[str, Any]] = Field(alias="Parameters", default=None) # Not supported yet
    UseFloatingPointProtection: Optional[bool] = Field(alias="UseFloatingPointProtection", default=True) # Not supported yet

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
        ExternalController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ExternalController.from_file('/path/to/file')
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
        ExternalController
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ExternalController.from_json('{ ... }')
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
        ExternalController
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


ExternalController.update_forward_refs()
