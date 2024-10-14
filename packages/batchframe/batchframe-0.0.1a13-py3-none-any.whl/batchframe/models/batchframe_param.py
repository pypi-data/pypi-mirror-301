from typing import Annotated, TypeVar, get_args, Optional, Any
from datetime import datetime
import inspect
from kink import di
import logging

_logger = logging.getLogger(__name__)

SUPPORTED_TYPES: set[type] = {str, int, float, datetime}

# Maybe check on https://github.com/python/mypy/issues/3331

T = TypeVar('T')

class BatchframeParamMarker:
    pass

BatchframeParam = Annotated[T, BatchframeParamMarker]


"""Inspects a classes' __init__ method and gives back a list of name-type
             tuples for any arguments type-hinted with BatchframeParam[type]

   _returns_ A list of tuples with (argument name, argument type, optional default value)
"""
def get_injectable_init_params(clazz: type) -> list[tuple[str, type, Optional[Any]]]:
    res: list[tuple[str, type, Optional[Any]]] = []

    for param_name, definition in inspect.signature(clazz.__init__).parameters.items(): #type: ignore [misc] # https://github.com/python/typing/discussions/1331
        generic_args = get_args(definition.annotation)
        if len(generic_args) == 2 and generic_args[1] == BatchframeParamMarker:
            res.append((param_name, generic_args[0], definition.default))

    return res

def get_all_di_services() -> set[type]:
    all_di_keys = di._services.keys()
    services: set[type] = set()
    for di_key in all_di_keys:
        if not isinstance(di_key, str):
            services.add(di_key)

    return services

# Typing bugs known in pyright and mypy: https://github.com/python/mypy/issues/17728
def cast_param_to_type(param_type: type[T], raw_param: str) -> T:
    if issubclass(param_type, (str, int, float)):
        return param_type(raw_param) # type: ignore [return-value]
    elif issubclass(param_type, datetime):
        return param_type.fromisoformat(raw_param) # type: ignore [return-value]
    else:
        raise ValueError('Unsupported type')


def init_all_params(name_value_args: dict[str, str]):
    all_services = get_all_di_services()
    all_params: dict[str, tuple[type, Optional[Any]]] = {}
    param_to_class_map: dict[str, type] = {}

    for service in all_services:
        found_params = get_injectable_init_params(service)

        for param_name, param_type, default_val in found_params:
            if param_name in param_to_class_map.keys():
                bound_class = param_to_class_map[param_name]
                if not (issubclass(bound_class, service) or issubclass(service, bound_class)):
                    raise ValueError(f"Batchframe parameter with name {param_name} in injectable {service} is defined in another non-parent/child class. "+
                                 "Please use unique parameter names!")
            elif param_type not in SUPPORTED_TYPES:
                raise ValueError(f"Type {param_type} of parameter {param_type} in injectable {service} is " +
                                 f"currently not supported for auto-injection. Please use any of {SUPPORTED_TYPES}!")
            else:
                all_params[param_name] = (param_type, default_val)
                param_to_class_map[param_name] = service
    
    for arg_name, arg_value in name_value_args.items():
        if arg_name in all_params.keys():
            param_type, default_val = all_params.pop(arg_name)
            casted_value: Any = cast_param_to_type(param_type, arg_value)
            di[arg_name] = casted_value
        else:
            _logger.warning(f"Parameter with name {arg_name} not found. Skipping this argument")

    # Clean out non-filled params that have default values
    all_params = {param_name:definition_tuple for (param_name, definition_tuple) in all_params.items() if definition_tuple[1] is inspect._empty}
    
    if len(all_params) > 0:
        raise ValueError(f"The following parameters have not been given values: {list(all_params.keys())}")