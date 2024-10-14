# patch.py

from typing import Optional, List, Union
from pydantic import create_model
from .. import completion, PredefinedModel, InstructorMode, BaseModel


def patch(
    instance: BaseModel,
    messages: Union[str, List[dict]],
    model: Union[str, PredefinedModel] = "gpt-4o-mini",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    organization: Optional[str] = None,
    max_tokens: Optional[int] = None,
    max_retries: int = 3,
    temperature: float = 0.7,
    mode: InstructorMode = "markdown_json_mode",
    progress_bar: Optional[bool] = True,
    verbose: bool = False,
) -> BaseModel:
    """
    Patches a BaseModel instance based on instructions or messages.

    Args:
        instance (BaseModel): The instance of the BaseModel to patch.
        messages (Union[str, List[dict]]): Instructions or messages for patching the model.
        model (Union[str, PredefinedModel]): The model to use for completions.
        api_key (Optional[str]): The API key to use.
        base_url (Optional[str]): The base URL to use.
        organization (Optional[str]): The organization to use.
        max_tokens (Optional[int]): The maximum number of tokens to use.
        max_retries (int): The maximum number of retries.
        temperature (float): The temperature to use for completions.
        mode (InstructorMode): The mode to use for completions.
        progress_bar (Optional[bool]): Whether to display a progress bar.
        verbose (bool): Whether to display verbose output.

    Returns:
        BaseModel: The patched instance.
    """
    # Step 1: Determine if changes are needed
    class YesNo(BaseModel):
        needs_change: bool

    change_prompt = f"Based on the following instructions or context, does the given {type(instance).__name__} instance need to be changed? Respond with True or False.\n\n"
    change_prompt += f"Instance: {instance.model_dump_json()}\n\n"
    change_prompt += f"Instructions/Context: {messages}\n"

    needs_change_response = completion(
        messages=change_prompt,
        model=model,
        api_key=api_key,
        base_url=base_url,
        organization=organization,
        response_model=YesNo,
        max_tokens=max_tokens,
        max_retries=max_retries,
        temperature=temperature,
        mode=mode,
        progress_bar=progress_bar,
        verbose=verbose,
    )

    if not needs_change_response.needs_change:
        if verbose:
            print("No changes needed for the instance.")
        return instance

    # Step 2: Select fields to update
    class FieldSelection(BaseModel):
        fields: List[str]

    select_prompt = f"Based on the following instructions or context, which fields of the {type(instance).__name__} instance need to be updated? Respond with a list of field names.\n\n"
    select_prompt += f"Instance: {instance.model_dump_json()}\n\n"
    select_prompt += f"Available fields: {', '.join(instance.model_fields.keys())}\n\n"
    select_prompt += f"Instructions/Context: {messages}\n"

    field_selection_response = completion(
        messages=select_prompt,
        model=model,
        api_key=api_key,
        base_url=base_url,
        organization=organization,
        response_model=FieldSelection,
        max_tokens=max_tokens,
        max_retries=max_retries,
        temperature=temperature,
        mode=mode,
        progress_bar=progress_bar,
        verbose=verbose,
    )

    fields_to_update = field_selection_response.fields

    # Step 3: Create update model and patch the instance
    update_fields = {
        field: (instance.model_fields[field].annotation, ...)
        for field in fields_to_update
    }
    UpdateModel = create_model(f"{type(instance).__name__}Update", **update_fields)

    patch_prompt = f"Update the following fields of the {type(instance).__name__} instance: {', '.join(fields_to_update)}\n\n"
    patch_prompt += f"Current instance: {instance.model_dump_json()}\n\n"
    patch_prompt += f"Instructions/Context: {messages}\n"

    update_response = completion(
        messages=patch_prompt,
        model=model,
        api_key=api_key,
        base_url=base_url,
        organization=organization,
        response_model=UpdateModel,
        max_tokens=max_tokens,
        max_retries=max_retries,
        temperature=temperature,
        mode=mode,
        progress_bar=progress_bar,
        verbose=verbose,
    )

    # Merge updates into the current data
    current_data = instance.model_dump()
    updated_data = {**current_data, **update_response.model_dump()}

    # Create and return the updated instance
    return type(instance)(**updated_data)

# Example usage
if __name__ == "__main__":
    class Person(BaseModel):
        name: str
        age: int
        occupation: str

    person = Person(name="John Doe", age=30, occupation="Engineer")

    instructions = "Update the person's age to 31 and change their occupation to 'Senior Engineer'."

    updated_person = patch(person, messages=instructions, verbose=True)
    print(f"Updated person: {updated_person}")