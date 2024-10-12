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

from dnv_bladed_models.fixed_step_integrator import FixedStepIntegrator



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ImplicitNewmarkBetaFixedStep(FixedStepIntegrator, IntegratorType='ImplicitNewmarkBetaFixedStep'):
    r"""
    Settings for the Implicit Newmark Beta Fixed Step integrator.
    
    Not supported yet.
    
    Attributes:
    ----------
    IntegratorType : str, default='ImplicitNewmarkBetaFixedStep', Not supported yet
        Defines the specific type of Integrator model in use.  For a `ImplicitNewmarkBetaFixedStep` object, this must always be set to a value of `ImplicitNewmarkBetaFixedStep`.

    MaximumNumberOfIterations : int, default=1, Not supported yet
        The maximum number of iterations for prescribed freedoms and first order states (e.g. dynamic stall & wake).  A value of 1 may sometimes inprecisely integrate first order states

    Beta : float, default=0.25, Not supported yet
        The β parameter for the Newmark-β integration method.  The recommended value of 0.25 (with a γ value of 0.50) results in the constant average acceleration method that is unconditionally stable for linear systems.  A value of 0.26 (with a γ value of 0.52) results in a method that is close to the constant average acceleration method but includes a small amount of numerical damping to reduce unwanted vibrations of high-frequency modes. Note that the numerical damping increases with the step size.

    Gamma : float, default=0.5, Not supported yet
        The γ parameter for the Newmark-β integration method.  The recommended value depends on the β parameter and given by the formula γ = 2.sqrt(β) - 0.5.  Values higher than 0.5 introduce positive numerical damping, whereas lower values introduce negative numerical damping.

    ToleranceMultiplier : float, default=1, Not supported yet
        The tolerance used for defining the convergence criteria of the Newton-Raphson equilibrium iterations for 1st and 2nd order states.  Reduced values of this parameter result in more iterations and more accurate solutions, whereas increased values result in less iterations and less accurate solutions, which eventually may cause stability problems.  The allowable range of values for this parameter is 0.001 to 1000.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/Integrator/ImplicitNewmarkBetaFixedStep.json')
    
    IntegratorType: Optional[str] = Field(alias="IntegratorType", default='ImplicitNewmarkBetaFixedStep') # Not supported yet
    MaximumNumberOfIterations: Optional[int] = Field(alias="MaximumNumberOfIterations", default=1) # Not supported yet
    Beta: Optional[float] = Field(alias="Beta", default=0.25) # Not supported yet
    Gamma: Optional[float] = Field(alias="Gamma", default=0.5) # Not supported yet
    ToleranceMultiplier: Optional[float] = Field(alias="ToleranceMultiplier", default=1) # Not supported yet

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
        ImplicitNewmarkBetaFixedStep
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ImplicitNewmarkBetaFixedStep.from_file('/path/to/file')
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
        ImplicitNewmarkBetaFixedStep
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = ImplicitNewmarkBetaFixedStep.from_json('{ ... }')
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
        ImplicitNewmarkBetaFixedStep
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


ImplicitNewmarkBetaFixedStep.update_forward_refs()
