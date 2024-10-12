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

from dnv_bladed_models.applied_load import AppliedLoad

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.environment import Environment

from dnv_bladed_models.event import Event

from dnv_bladed_models.external_module import ExternalModule

from dnv_bladed_models.externally_stepped_simulation import ExternallySteppedSimulation

from dnv_bladed_models.initial_condition import InitialCondition

from dnv_bladed_models.time_domain_outputs import TimeDomainOutputs



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TimeDomainSimulation(BladedModel):
    r"""
    The definition of a time domain analysis - mutually exclusive with &#39;SteadyCalculation&#39;
    
    Not supported yet.
    
    Attributes:
    ----------
    Duration : float, Not supported yet
        The duration of the simulation for which results will be output, excluding the LeadInTime. SI units are seconds.

    LeadInTime : float, default=7, Not supported yet
        The time that the simulation will run before any outputs are recorded.  This is to allow the simulation to \"settle\", allowing any non-equilibrium initial conditions to converge on their steady state values.  The lead-in time will be added to the duration, meaning that the duration will be the length of time the outputs are recorded for.  Any times specified within the simulation will be measured from the *end* of the lead-in period.

    Outputs : TimeDomainOutputs, Not supported yet

    AdditionalExternalModules : List[ExternalModule], default=list(), Not supported yet
        A list of external module that will be used for this simulation only.  This could be used to apply loading to the structure, or some other load case specific purpose.  If the external module is seeking to simulate an intrinsic property of the turbine, consider moving it into the GlobalExternalModules, or adding it to the Assembly tree.

    ExternallySteppedSimulation : ExternallySteppedSimulation, Not supported yet

    Environment : Environment, Not supported yet

    AppliedLoads : List[AppliedLoad], default=list(), Not supported yet
        A list of point loading definitions which apply a time history of forces to the structure.

    InitialConditions : List[InitialCondition], default=list(), Not supported yet
        A list of initial conditions to apply at the beginning of the simulation.

    Events : List[Event], default=list(), Not supported yet
        A list of events that occur during the simulation.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/TimeDomainSimulation.json')
    
    Duration: Optional[float] = Field(alias="Duration", default=None) # Not supported yet
    LeadInTime: Optional[float] = Field(alias="LeadInTime", default=7) # Not supported yet
    Outputs: Optional[TimeDomainOutputs] = Field(alias="Outputs", default=None) # Not supported yet
    AdditionalExternalModules: Optional[List[ExternalModule]] = Field(alias="AdditionalExternalModules", default=list()) # Not supported yet
    ExternallySteppedSimulation: Optional[ExternallySteppedSimulation] = Field(alias="ExternallySteppedSimulation", default=None) # Not supported yet
    Environment: Optional[Environment] = Field(alias="Environment", default=None) # Not supported yet
    AppliedLoads: Optional[List[AppliedLoad]] = Field(alias="AppliedLoads", default=list()) # Not supported yet
    InitialConditions: Optional[List[InitialCondition]] = Field(alias="InitialConditions", default=list()) # Not supported yet
    Events: Optional[List[Event]] = Field(alias="Events", default=list()) # Not supported yet

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
        TimeDomainSimulation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainSimulation.from_file('/path/to/file')
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
        TimeDomainSimulation
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainSimulation.from_json('{ ... }')
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
        TimeDomainSimulation
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


TimeDomainSimulation.update_forward_refs()
