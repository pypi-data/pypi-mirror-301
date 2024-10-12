from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union
from pydantic import BaseModel, root_validator
from .models_impl import *

class CommonBaseModel(BaseModel, ABC):

    @abstractmethod
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
        pass

    @abstractmethod
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
        pass

    @root_validator(pre=True)
    def _remove_underscore_fields(cls, values: Dict[str, Any]):
        remove_underscore_fields(values)
        return values