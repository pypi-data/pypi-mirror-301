from pydantic import create_model, Field, BaseModel
import inspect
from typing import Any, Callable, Dict, Type, Union


def convert_to_openai_tool(
    function: Union[Dict[str, Any], Type[BaseModel], Callable],
) -> Dict[str, Any]:
    """Convert a raw function/class to an OpenAI tool."""
    from openai import pydantic_function_tool

    if isinstance(function, dict):
        # If it's already a dictionary, assume it's in the correct format
        return function
    elif isinstance(function, type) and issubclass(function, BaseModel):
        # If it's a Pydantic model, use pydantic_function_tool directly
        return pydantic_function_tool(function)
    elif callable(function):
        # If it's a callable, convert it to a Pydantic model first
        pydantic_model = create_pydantic_model_from_function(function)
        return pydantic_function_tool(pydantic_model)
    else:
        raise ValueError(f"Unsupported function type: {type(function)}")

def create_pydantic_model_from_function(function: Callable) -> Type[BaseModel]:
    """Create a Pydantic model from a Python function."""
    signature = inspect.signature(function)
    fields = {}
    for name, param in signature.parameters.items():
        annotation = param.annotation if param.annotation != inspect.Parameter.empty else Any
        default = ... if param.default == inspect.Parameter.empty else param.default
        fields[name] = (annotation, Field(default=default))
    
    # Use the original function name for the model
    model = create_model(function.__name__, **fields)
    model.__doc__ = function.__doc__ or ""
    
    # Store the original function as an attribute
    model._original_function = function
    
    return model