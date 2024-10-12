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



from .schema_helper import SchemaHelper 
from .models_impl import *
from .common_base_model import CommonBaseModel

class InterpolatedAerofoilLibrary(BladedModel):
    r"""
    A library of interpolated aerofoils, each of which has a 2D interpolation over thickness and Reynold&#39;s number.
    
    Attributes:
    ----------
    Notes:
    -----
    """
    _relative_schema_path: str = PrivateAttr('Components/Blade/InterpolatedAerofoilLibrary/InterpolatedAerofoilLibrary.json')
    

    class Config:
        extra = Extra.allow
        validate_assignment = True
        allow_population_by_field_name = True
        pass


    def items(self) -> list[tuple[str, List]]:
        """
        Returns a list of key-value pairs for all of the user-supplied entries currently in the model.
        """
        return [(k, self.__dict__[k]) for k in self.__dict__ if k not in self.__fields__]

    def keys(self) -> list[str]:
        """
        Returns a list of keys for all of the user-supplied entries currently in the model.
        """
        return [k for k in self.__dict__ if k not in self.__fields__]

    def values(self) -> list[List]:
        """
        Returns a list of model objects for all of the user-supplied entries currently in the model.
        """
        return [self.__dict__[k] for k in self.__dict__ if k not in self.__fields__]

    def __len__(self):
        return len([k for k in self.__dict__ if k not in self.__fields__])

    def __contains__(self, item):
        for k in self.__dict__:
            if k not in self.__fields__ and k == item:
                return True
        return False

    def __getitem__(self, key):
        if isinstance(key, int):
            keys = self.keys()
            if len(keys) == 0:
                raise KeyError(f"There are currently no entries in the model object.")
            if key < 0 or key >= len(keys):
                raise KeyError(f"Invalid index specified: {key} (0 >= i < {len(keys)})")
            key = keys[key]
        elif isinstance(key, str):
            if key in self.__fields__:
                raise KeyError(f"Item accessors can only be used for custom entries. '{key}' is a pre-defined model property.")
            if not key in self.__dict__:
                raise KeyError(f"There is no entry with key '{key}'.")
        return getattr(self, key)

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise KeyError(f"Custom entries can only be added with string keys")
        if key in self.__fields__:
            raise KeyError(f"Item accessors can only be used for custom entries. '{key}' is a pre-defined model property.")
        if not isinstance(value, List):
            raise TypeError(f"Entries must be of type 'List'; received '{type(value).__name__}'")
        setattr(self, key, value)

    def __delitem__(self, key):
        if isinstance(key, int):
            keys = self.keys()
            if len(keys) == 0:
                raise KeyError(f"There are currently no entries in the model object.")
            if key < 0 or key >= len(keys):
                raise KeyError(f"Invalid index specified: {key} (0 >= i < {len(keys)})")
            key = keys[key]
        elif isinstance(key, str):
            if key in self.__fields__:
                raise KeyError(f"Item accessors can only be used for custom entries. '{key}' is a pre-defined model property.")
            if not key in self.__dict__:
                raise KeyError(f"There is no entry with key '{key}'.")
        delattr(self, key)

    def __setattr__(self, name, value):
        if not name in self.__fields__ and not isinstance(value, List):
            raise TypeError(f"Entries must be of type 'List'; received '{type(value).__name__}'")
        super().__setattr__(name, value)

    class __CustomEntries__(BaseModel):
        entries: Dict[str, List] = Field(default={})

    @classmethod
    def __get_validators__(cls):
        yield cls._factory

    @classmethod
    def _factory(cls, data):
        if isinstance(data, InterpolatedAerofoilLibrary):
            return data
        if not isinstance(data, dict):
            raise TypeError('An object is required to define InterpolatedAerofoilLibrary models')
        return custom_entries_parser(cls, data, List, InterpolatedAerofoilLibrary.__CustomEntries__)

    @classmethod
    def parse_obj(cls: Type['Model'], obj: Any) -> 'Model':
        return custom_entries_parser(cls, obj, List, InterpolatedAerofoilLibrary.__CustomEntries__)


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
        InterpolatedAerofoilLibrary
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = InterpolatedAerofoilLibrary.from_file('/path/to/file')
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
        InterpolatedAerofoilLibrary
            The model object.

        Raises
        ------
        ValueError, ValidationError
            If the JSON document does not correctly describe the model according to the model schema.

        Examples
        --------
        >>> model = InterpolatedAerofoilLibrary.from_json('{ ... }')
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
        InterpolatedAerofoilLibrary
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


InterpolatedAerofoilLibrary.update_forward_refs()
InterpolatedAerofoilLibrary.__CustomEntries__.update_forward_refs() 
