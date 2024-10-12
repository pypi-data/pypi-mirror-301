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

from dnv_bladed_models.integrator import Integrator



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class RungeKuttaVariableStep(Integrator, IntegratorType='RungeKuttaVariableStep'):
    r"""
    Settings for the Runge Kutta Variable Step integrator.
    
    Not supported yet.
    
    Attributes:
    ----------
    IntegratorType : str, default='RungeKuttaVariableStep', Not supported yet
        Defines the specific type of Integrator model in use.  For a `RungeKuttaVariableStep` object, this must always be set to a value of `RungeKuttaVariableStep`.

    InitialStep : float, default=0, Not supported yet
        The recommended value is zero: the minimum time step will in fact be used.  A value larger than the minimum time step will speed up the initialisation of the simulation, but there is a risk of numerical problems if too large a value is used.

    Tolerance : float, default=0.005, Not supported yet
        The tolerance for the variable step integrator: This parameter defines the precision of the simulation. All states are integrated to an error within the integration tolerance multiplied by the state magnitude at that step. A higher value can increase simulation speed but lower precision.  Fixed step integrators: When the \"Maximum number of iterations\" > 1, the integrator relative tolerance is used to control how many iterations are carried out when integrating the first order and prescribed second order states. Iterations are carried out until the maximum number of iterations is reached, or until the change in all first order and prescribed state derivatives between successive iterations is less than the relative tolerance multiplied by the state derivative absolute value.

    MinimumTimeStep : float, default=1.0E-7, Not supported yet
        The minimum time step.  The simulation uses a 4/5th order Runge-Kutta variable time step method.  The time step will be reduced automatically if the specified tolerance is exceeded, until this minimum value is reached.

    MaximumTimeStep : float, default=1, Not supported yet
        The maximum time step.  This should normally be the same as the output time step, although a smaller value might be useful in some cases if the output time step is particularly long.  A very small value for the minimum time step is recommended, such as 10^-8 s, to ensure that the accuracy of simulation is not constrained by this.  In special cases, increasing the minimum time step may speed up the simulation with little loss of accuracy, but it is advisable to check that the results are not significantly altered by doing this.  This situation may arise for example with a dynamic mode which is inactive because it is heavily damped.  It may be better to remove the mode completely.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Settings/SolverSettings/Integrator/RungeKuttaVariableStep.json')
    
    IntegratorType: Optional[str] = Field(alias="IntegratorType", default='RungeKuttaVariableStep') # Not supported yet
    InitialStep: Optional[float] = Field(alias="InitialStep", default=0) # Not supported yet
    Tolerance: Optional[float] = Field(alias="Tolerance", default=0.005) # Not supported yet
    MinimumTimeStep: Optional[float] = Field(alias="MinimumTimeStep", default=1.0E-7) # Not supported yet
    MaximumTimeStep: Optional[float] = Field(alias="MaximumTimeStep", default=1) # Not supported yet

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
        RungeKuttaVariableStep
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = RungeKuttaVariableStep.from_file('/path/to/file')
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
        RungeKuttaVariableStep
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = RungeKuttaVariableStep.from_json('{ ... }')
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
        RungeKuttaVariableStep
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


RungeKuttaVariableStep.update_forward_refs()
