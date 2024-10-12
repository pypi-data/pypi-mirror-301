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

from dnv_bladed_models.outputs import Outputs

from dnv_bladed_models.selected_component_output_group import SelectedComponentOutputGroup



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class TimeDomainOutputs(Outputs):
    r"""
    The definition outputs to write for this simulation.
    
    Not supported yet.
    
    Attributes:
    ----------
    TimeStepForOutputs : float, Not supported yet
        The output time step for the simulation.

    LengthOfOutputBuffer : float, Not supported yet
        The length of time to buffer the output logs.

    OutputSummaryInformation : bool, default=True, Not supported yet
        If true, the summary information output group will be created.

    OutputExternalControllers : bool, default=True, Not supported yet
        If true, the controller output group will be created.

    OutputBuoyancyInformation : bool, default=False, Not supported yet
        If true, the buoyancy output group will be created.

    OutputFiniteElementMatrices : bool, default=False, Not supported yet
        If true, the finite element output group will be created, providing far more detail about the finite element matrices.

    OutputSignalProperties : bool, default=False, Not supported yet
        If true, the signal properties output group will be created.  This records the properties provided to the controller, with and without noise and other distortions.

    OutputWakePropagation : bool, default=False, Not supported yet
        If true, the eddy viscosity propagation of the wake is output as a 2D table of relative velocity against radial position and distance traveled to a \".wake\" file in the output folder.

    OutputSoftwarePerformance : bool, default=False, Not supported yet
        If true, the software performance output group will be created.

    OutputStateInformation : bool, default=False, Not supported yet
        If true, the integrator state output group will be created.  This can be used to help understand how efficiently the integrator is coping with the simulation.

    OutputExternalControllerExchangeObject : bool, default=False, Not supported yet
        If true, this will output all of the values contained in the external controller interface before and after each external controller call.  This is intended to assist debugging external controllers.

    OutputExternalControllerLegacySwapArray : bool, default=False, Not supported yet
        If true, the contents of the swap array passed to a legacy controller will be logged.  This is used only when trying to debug legacy controllers, and will not produce useful results if there is more than one legacy controller being run.

    SelectedComponentOutputGroups : List[SelectedComponentOutputGroup], default=list(), Not supported yet
        A list of references to the OutputGroup of specific components to output.  This allows the outputs of individual components to be switched off, or chosen from an available list of output regimes.  If a component is not mentioned, it will produce outputs according to its default output group, if there is one available.

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('TimeDomainSimulation/TimeDomainOutputs/TimeDomainOutputs.json')
    
    TimeStepForOutputs: Optional[float] = Field(alias="TimeStepForOutputs", default=None) # Not supported yet
    LengthOfOutputBuffer: Optional[float] = Field(alias="LengthOfOutputBuffer", default=None) # Not supported yet
    OutputSummaryInformation: Optional[bool] = Field(alias="OutputSummaryInformation", default=True) # Not supported yet
    OutputExternalControllers: Optional[bool] = Field(alias="OutputExternalControllers", default=True) # Not supported yet
    OutputBuoyancyInformation: Optional[bool] = Field(alias="OutputBuoyancyInformation", default=False) # Not supported yet
    OutputFiniteElementMatrices: Optional[bool] = Field(alias="OutputFiniteElementMatrices", default=False) # Not supported yet
    OutputSignalProperties: Optional[bool] = Field(alias="OutputSignalProperties", default=False) # Not supported yet
    OutputWakePropagation: Optional[bool] = Field(alias="OutputWakePropagation", default=False) # Not supported yet
    OutputSoftwarePerformance: Optional[bool] = Field(alias="OutputSoftwarePerformance", default=False) # Not supported yet
    OutputStateInformation: Optional[bool] = Field(alias="OutputStateInformation", default=False) # Not supported yet
    OutputExternalControllerExchangeObject: Optional[bool] = Field(alias="OutputExternalControllerExchangeObject", default=False) # Not supported yet
    OutputExternalControllerLegacySwapArray: Optional[bool] = Field(alias="OutputExternalControllerLegacySwapArray", default=False) # Not supported yet
    SelectedComponentOutputGroups: Optional[List[SelectedComponentOutputGroup]] = Field(alias="SelectedComponentOutputGroups", default=list()) # Not supported yet

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
        TimeDomainOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainOutputs.from_file('/path/to/file')
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
        TimeDomainOutputs
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = TimeDomainOutputs.from_json('{ ... }')
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
        TimeDomainOutputs
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


TimeDomainOutputs.update_forward_refs()
