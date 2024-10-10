from loguru import logger
from .. import Completions, InstructorMode, PredefinedModel
from pydantic import BaseModel, create_model
from typing import List, Literal, Optional, Type, Union
from rich.progress import Progress, SpinnerColumn, TextColumn


def generator(
    target: Type[BaseModel],
    instructions: Optional[str] = None,
    process: Literal["single", "batch"] = "single",
    n: int = 1,
    batch_size: int = 3,
    model: Union[str, PredefinedModel] = "gpt-4o-mini",
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    organization: Optional[str] = None,
    temperature: Optional[float] = None,
    max_retries: int = 3,
    mode: InstructorMode = "tool_call",
    client: Optional[Literal["openai", "litellm"]] = "openai",
    verbose: bool = False,
    progress_bar: Optional[bool] = True,
) -> Union[BaseModel, List[BaseModel]]:
    """
    Generates a single or batch of pydantic models based on the provided target schema.
    """

    if verbose:
        logger.info(f"Generating {n} {target.__name__} models.")
        logger.info(f"Using model: {model}")
        logger.info(f"Batch size: {batch_size}")
        logger.info(f"Process: {process}")

    system_message = f"""
    You are a data generator. Your task is to generate {n} valid instance(s) of the following Pydantic model:
    
    {target.model_json_schema()}
    
    Ensure that all generated instances comply with the model's schema and constraints.
    """

    user_message = (
        instructions
        if instructions
        else f"Generate {n} instance(s) of the given model."
    )

    completion_client = Completions(
        api_key=api_key,
        base_url=base_url,
        organization=organization,
        provider=client,
        verbose=verbose,
    )

    if progress_bar:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task_id = progress.add_task("Generating Model(s)...", total=n)

            if process == "single" or n == 1:
                response_model = (
                    target
                    if n == 1
                    else create_model("ResponseModel", items=(List[target], ...))
                )

                result = completion_client.completion(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    model=model,
                    response_model=response_model,
                    mode=mode,
                    max_retries=max_retries,
                    temperature=temperature,
                    progress_bar=progress_bar,
                )

                progress.update(task_id, completed=n)
                return result if n == 1 else result.items
            else:  # batch process
                results = []
                for i in range(0, n, batch_size):
                    batch_n = min(batch_size, n - i)
                    batch_message = f"Generate {batch_n} instances of the given model."
                    if results:
                        batch_message += f"\nPreviously generated instances: {results[-3:]}\nEnsure these new instances are different."

                    response_model = create_model("ResponseModel", items=(List[target], ...))

                    result = completion_client.completion(
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": batch_message},
                        ],
                        model=model,
                        response_model=response_model,
                        mode=mode,
                        max_retries=max_retries,
                        temperature=temperature,
                        progress_bar=progress_bar,
                    )

                    results.extend(result.items)
                    progress.update(task_id, advance=batch_n)

                return results
    else:
        if process == "single" or n == 1:
            response_model = (
                target
                if n == 1
                else create_model("ResponseModel", items=(List[target], ...))
            )

            result = completion_client.completion(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                model=model,
                response_model=response_model,
                mode=mode,
                max_retries=max_retries,
                temperature=temperature,
                progress_bar=progress_bar,
            )

            return result if n == 1 else result.items
        else:  # batch process
            results = []
            for i in range(0, n, batch_size):
                batch_n = min(batch_size, n - i)
                batch_message = f"Generate {batch_n} instances of the given model."
                if results:
                    batch_message += f"\nPreviously generated instances: {results[-3:]}\nEnsure these new instances are different."

                response_model = create_model("ResponseModel", items=(List[target], ...))

                result = completion_client.completion(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": batch_message},
                    ],
                    model=model,
                    response_model=response_model,
                    mode=mode,
                    max_retries=max_retries,
                    temperature=temperature,
                    progress_bar=progress_bar,
                )

                results.extend(result.items)

            return results


if __name__ == "__main__":

    class User(BaseModel):
        name: str
        age: int

    print(generator(User, n=5, process="batch", batch_size=2, verbose=True))
