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

from dnv_bladed_models.bladed_model import BladedModel

from dnv_bladed_models.vector3_d import Vector3D



class ConnectableNode_ComponentTypesAllowedEnum(str, Enum):
    COMPONENTS = "COMPONENTS"

from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class ConnectableNode(BladedModel, ABC):
    r"""
    An object declaring a distal node for a component.
    
    Not supported yet.
    
    Attributes:
    ----------
    ComponentTypesAllowed : ConnectableNode_ComponentTypesAllowedEnum, Not supported yet
        Optional: A list of the components that could be attached to the node.  If not specified, this will be governed by the component's connectivity.

    RelativeOrientation : List[float], default=list(), Not supported yet
        The relative orientation of the attached component to the current component (e.g. the axle to the nacelle, or the blade assembly to the hub).  Required if encrypted and not the same as the parent (e.g. for a nacelle's axle node)

    OffsetIfEncrypted : Vector3D

    Notes:
    -----This model is not supported yet by the Bladed calculation engine.
    """
    _relative_schema_path: str = PrivateAttr('Components/common/ConnectableNode.json')
    
    ComponentTypesAllowed: Optional[ConnectableNode_ComponentTypesAllowedEnum] = Field(alias="ComponentTypesAllowed", default=None) # Not supported yet
    RelativeOrientation: Optional[List[float]] = Field(alias="RelativeOrientation", default=list()) # Not supported yet
    OffsetIfEncrypted: Optional[Vector3D] = Field(alias="OffsetIfEncrypted", default=None)





ConnectableNode.update_forward_refs()
