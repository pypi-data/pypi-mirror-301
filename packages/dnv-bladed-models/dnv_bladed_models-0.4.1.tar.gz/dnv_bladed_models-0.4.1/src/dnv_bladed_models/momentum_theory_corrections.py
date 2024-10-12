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

from dnv_bladed_models.dynamic_wake import DynamicWake

from dnv_bladed_models.glauert_skew_wake_model import GlauertSkewWakeModel



class MomentumTheoryCorrections_GlauertCorrectionMethodForHighInductionEnum(str, Enum):
    BLADED = "BLADED"
    NONE = "NONE"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class MomentumTheoryCorrections(BladedModel):
    r"""
    The Blade Element Momentum (BEM) theory model.
    
    Attributes:
    ----------
    GlauertCorrectionMethodForHighInduction : MomentumTheoryCorrections_GlauertCorrectionMethodForHighInductionEnum, default='BLADED'
        The Glauert correction method for when the rotor has high induction.

    GlauertSkewedWakeCorrectionModel : GlauertSkewWakeModel

    InductionFactorsTolerance : float, default=0.00010
        In the steady state (e.g. finding initial conditions) and/or when using equilibrium wake in the dynamic state, the axial and tangential factors are found by iteration. The precision to which these induction factors are found is determined by this tolerance.

    NoInflowBelowTipSpeedRatio : float, default=1
        The tip speed ratio below which the inflow calculations will be switched off. Default = 1

    FullInflowAboveTipSpeedRatio : float, default=2
        The tip speed ratio above which the inflow calculations will be switched on. Default = 2

    DynamicWake : DynamicWake, abstract

    IncludeStructuralVelocityInInductionCalculation : bool, default=True
        If true, the axial structural velocity will be included in the induction calculations. Enabled by default.

    Notes:
    -----
    DynamicWake has the following concrete types:
        - EquilibriumWakeModel
        - FreeFlowModel
        - FrozenWakeModel
        - OyeDynamicWake
        - PittAndPetersModel
    
    """
    _relative_schema_path: str = PrivateAttr('Settings/AerodynamicSettings/AerodynamicModel/MomentumTheoryCorrections/MomentumTheoryCorrections.json')
    
    GlauertCorrectionMethodForHighInduction: Optional[MomentumTheoryCorrections_GlauertCorrectionMethodForHighInductionEnum] = Field(alias="GlauertCorrectionMethodForHighInduction", default='BLADED')
    GlauertSkewedWakeCorrectionModel: Optional[GlauertSkewWakeModel] = Field(alias="GlauertSkewedWakeCorrectionModel", default=None)
    InductionFactorsTolerance: Optional[float] = Field(alias="InductionFactorsTolerance", default=0.00010)
    NoInflowBelowTipSpeedRatio: Optional[float] = Field(alias="NoInflowBelowTipSpeedRatio", default=1)
    FullInflowAboveTipSpeedRatio: Optional[float] = Field(alias="FullInflowAboveTipSpeedRatio", default=2)
    DynamicWake: Optional[DynamicWake] = Field(alias="DynamicWake", default=None)
    IncludeStructuralVelocityInInductionCalculation: Optional[bool] = Field(alias="IncludeStructuralVelocityInInductionCalculation", default=True)

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
        MomentumTheoryCorrections
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MomentumTheoryCorrections.from_file('/path/to/file')
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
        MomentumTheoryCorrections
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = MomentumTheoryCorrections.from_json('{ ... }')
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
        MomentumTheoryCorrections
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


MomentumTheoryCorrections.update_forward_refs()
