# coding: utf-8

from __future__ import annotations

from abc import ABC

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

from dnv_bladed_models.component import Component

from dnv_bladed_models.foundation_connectable_nodes import FoundationConnectableNodes



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class Foundation(Component, ABC):
    r"""
    FOUNDATION\&quot;
    
    Not supported yet.
    
    Attributes:
    ----------
    UseFiniteElementDeflectionsForFoundationLoads : bool, default=False, Not supported yet
        When this feature is enabled, support structure deflections calculated from the underlying finite element model are used to evaluate the foundation applied loads. The effect of these foundation loads is included when evaluating the turbine dynamic response.  This model is only active for time domain simulations. The foundation applied loads are calculated from the finite element deflections from the previous time step. This means that time step convergence studies may be required to ensure the accuracy of this model.  When this feature is enabled, the support structure node deflection outputs will be based on the finite element model rather than the modal deflections that are normally used. This ensures consistency between the foundation applied loads and the support structure node deflections.

    ConnectableNodes : FoundationConnectableNodes, Not supported yet

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/Foundation/common/Foundation.json')
    
    UseFiniteElementDeflectionsForFoundationLoads: Optional[bool] = Field(alias="UseFiniteElementDeflectionsForFoundationLoads", default=False) # Not supported yet
    ConnectableNodes: Optional[FoundationConnectableNodes] = Field(alias="ConnectableNodes", default=FoundationConnectableNodes()) # Not supported yet





Foundation.update_forward_refs()
