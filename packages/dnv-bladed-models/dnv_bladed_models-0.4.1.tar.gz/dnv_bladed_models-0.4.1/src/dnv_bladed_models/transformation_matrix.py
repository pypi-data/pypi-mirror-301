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




from .models_impl import *
from .common_base_model import CommonBaseModel

class TransformationMatrix(BaseModel):
    r"""
    A 6x6 matrix to transform one set of coordinates into another.
    
    Attributes:
    ----------
    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('')
    
    __data__: List[List[float]] = PrivateAttr() 
    

    class Config:
        extra = Extra.forbid
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    def __iter__(self):
        return iter(self.__data__)

    def __getitem__(self, index):
        return self.__data__[index]

    def __len__(self):
        return len(self.__data__)

    def dict(self, **kwargs):
        return self.__data__

    @property
    def data(self):
        """Returns the matrix data"""
        return self.__data__

    def __init__(self, data: List[List[float]]=[]):
        self.validate(data)
        self.__data__ = data
        super().__init__()
        
    @classmethod
    def __get_validators__(cls):
        yield cls.cascadeValidate

    @classmethod
    def cascadeValidate(cls, v):
        vm = cls.parse_obj(v)
        return vm

    @classmethod
    def parse_obj(cls, obj: Any):
        obj = cls.validate(obj)
        return cls(obj)

    @classmethod
    def validate(cls, obj):
        if not isinstance(obj, list):
            try:
                obj = list(obj)
            except (TypeError, ValueError) as e:
                exc = TypeError(f'{cls.__name__} expected list not {obj.__class__.__name__}')
                raise ValidationError([ErrorWrapper(exc, loc=ROOT_KEY)], cls) from e
        for i, row in enumerate(obj):
            for j, item in enumerate(row):
                if not isinstance(item, float):
                    try:
                        obj[i][j] = float(item)
                    except (TypeError, ValueError) as e:
                        exc = TypeError(f'{cls.__name__} expected float not {item.__class__.__name__}')
                        raise ValidationError([ErrorWrapper(exc, loc=(ROOT_KEY, i, j))], cls)
        return obj



TransformationMatrix.update_forward_refs()
