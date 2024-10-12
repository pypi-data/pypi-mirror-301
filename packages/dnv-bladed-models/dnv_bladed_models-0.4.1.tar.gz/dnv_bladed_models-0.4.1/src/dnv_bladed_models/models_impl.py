from typing import Dict
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.utils import ROOT_KEY

def remove_underscore_fields(values: Dict[str, any]):
    to_remove = set()
    for child_name, child in values.items():
        if child_name.startswith('_'):
            to_remove.add(child_name)
        elif isinstance(child, dict):
            remove_underscore_fields(child)
        elif isinstance(child, list):
            for item in child:
                if isinstance(child, dict):
                    remove_underscore_fields(item)
    for x in to_remove:
        del values[x]

def custom_entries_parser(cls, obj, valid_raw_type, entry_model):
    obj = cls._enforce_dict_if_root(obj)
    if not isinstance(obj, dict):
        try:
            obj = dict(obj)
        except (TypeError, ValueError) as e:
            exc = TypeError(f'{cls.__name__} expected dict not {obj.__class__.__name__}')
            raise ValidationError([ErrorWrapper(exc, loc=ROOT_KEY)], cls) from e
    ctor_data = {}
    entry_data = {}
    field_keys = set(val.alias or val.name for val in cls.__fields__.values())
    for key, val in obj.items():
        if not key in field_keys and not key.startswith('_') and isinstance(val, valid_raw_type):
            entry_data[key] = val
        else:
            ctor_data[key] = val

    instance = cls(**ctor_data)
    try:
        container = entry_model.parse_obj({ 'entries' : entry_data })
        for key, val in container.entries.items():
            setattr(instance, key, val)
    except ValidationError as e:
        raise ValidationError([ErrorWrapper(e, loc=cls.__name__)], cls)
           
    return instance

