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

from dnv_bladed_models.perturbation_settings import PerturbationSettings



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ModelLinearisationPerturbations(PerturbationSettings):
    r"""
    
    
    Not supported yet.
    
    Attributes:
    ----------
    WindSpeedPerturbation : float, Not supported yet
        The magnitude of perturbation of the wind speed around the equilibrium value.  It should be small so that the analysis stays in the linear region  Omit keyword in order to let Bladed calculate a default perturbation.

    PitchPerturbation : float, Not supported yet
        The magnitude of perturbation of the pitch angle around the equilibrium value.  It should be small so that the analysis stays in the linear region.  Omit keyword in order to let Bladed calculate a default perturbation.

    GeneratorTorquePerturbation : float, Not supported yet
        The magnitude of perturbation of the generator torque around the equilibrium value.  It should be small so that the analysis stays in the linear region.  Omit keyword in order to let Bladed calculate a default perturbation.

    WindShearPerturbation : float, default=0, Not supported yet
        The magnitude of both horizontal and vertical shear perturbations   The default is to have no perturbation on the wind shear.

    ApplyPitchPerturbationToEachBlade : bool, default=False, Not supported yet
        If true, the pitch angle will be perturbed in turn for each blade as well as collectively for all blades

    YawActuatorTorquePerturbation : float, Not supported yet
        Yaw actuator torque perturbation. The torque perturbation is evenly distributed across the actuator banks.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('SteadyCalculation/ModelLinearisationPerturbations/ModelLinearisationPerturbations.json')
    
    WindSpeedPerturbation: Optional[float] = Field(alias="WindSpeedPerturbation", default=None) # Not supported yet
    PitchPerturbation: Optional[float] = Field(alias="PitchPerturbation", default=None) # Not supported yet
    GeneratorTorquePerturbation: Optional[float] = Field(alias="GeneratorTorquePerturbation", default=None) # Not supported yet
    WindShearPerturbation: Optional[float] = Field(alias="WindShearPerturbation", default=0) # Not supported yet
    ApplyPitchPerturbationToEachBlade: Optional[bool] = Field(alias="ApplyPitchPerturbationToEachBlade", default=False) # Not supported yet
    YawActuatorTorquePerturbation: Optional[float] = Field(alias="YawActuatorTorquePerturbation", default=None) # Not supported yet

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
        ModelLinearisationPerturbations
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ModelLinearisationPerturbations.from_file('/path/to/file')
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
        ModelLinearisationPerturbations
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ModelLinearisationPerturbations.from_json('{ ... }')
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
        ModelLinearisationPerturbations
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


ModelLinearisationPerturbations.update_forward_refs()
