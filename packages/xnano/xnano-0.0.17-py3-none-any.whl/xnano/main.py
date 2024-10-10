# xnano.main
# primary module for xnano
# entrypoint for completions

__all__ = [
    "Completions",
    "completion",
    "InstructorMode",

    "BaseModel",
    "Field"
]

# xnano/main.py
# hammad saeed .. twentytwentyfour

# base module for llm client
# litellm extension included in xnano[ext] or xnano[all]

# internal
from .utils.convert_to_openai_tool import convert_to_openai_tool

# ext
import enum
import time
from instructor import Mode
from openai.types.chat import ChatCompletion
from loguru import logger
from pydantic import create_model, Field, BaseModel as PydanticBaseModel
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Generator,
    Optional,
    overload,
    Type,
    TypeVar,
    Union
)
import json
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, TextColumn


# rich setup
import builtins
from rich import print as rich_print
builtins.print = rich_print


# BaseModel Subclass Client
T = TypeVar("T", bound="BaseModel")


# instructor config
InstructorMode = Literal[
    "function_call", "parallel_tool_call", "tool_call", "mistral_tools",
    "json_mode", "json_o1", "markdown_json_mode", "json_schema_mode",
    "anthropic_tools", "anthropic_json", "cohere_tools", "vertexai_tools",
    "vertexai_json", "gemini_json", "gemini_tools", "json_object", "tools_strict",
]


# Instructor Helper
def get_mode(mode: InstructorMode) -> Mode:
    return Mode(mode)


# predefined models
PredefinedModel = Literal[
    "o1-preview", "o1-mini",
    "gpt-4o-mini", "gpt-4o", "gpt-4", "gpt-4-turbo", "gpt-4-turbo-preview",
    "gpt-4-vision-preview",
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k",
    "claude-3.5", "claude-3", "claude-2",
    "claude-3-haiku-20240307", "claude-3-opus-20240229", "claude-3-sonnet-20240229",
    "ollama/llama3.2", "ollama/llama3.2:3b", "ollama/llama3.2:1b",
    "ollama/llama3.1", "ollama/llama3.1:8b", "ollama/llama3.1:70b",
    "ollama/llama3", "ollama/llama3:8b", "ollama/llama3:70b",
    "ollama/mistral-nemo",
    "ollama/llava",
    "ollama/mistral", "ollama/mistral:7b", "ollama/mistral:7b:instruct",
    "ollama/mixtral", "ollama/mixtral:8x7b", "ollama/mixtral:8x7b:instruct",
    "ollama/gemma2", "ollama/gemma2:9b", "ollama/gemma2:27b",
    "ollama/phi3.5",
    "ollama/qwen2.5", "ollama/qwen2.5:0.5b", "ollama/qwen2.5:1.5b", "ollama/qwen2.5:3b",
    "ollama/qwen2.5:7b", "ollama/qwen2.5:14b", "ollama/qwen2.5:32b", "ollama/qwen2.5:72b",
]


# constants & models
LiteLLM = Type["LiteLLM"]


# base client class
class Client(PydanticBaseModel):
    base: Optional[Any] = None
    patch: Optional[Any] = None


# client config
class Config(PydanticBaseModel):
    """
    Configuration for the Completions client.
    """
    api_key : Optional[str] = None
    base_url : Optional[str] = None
    organization : Optional[str] = None
    project : Optional[str] = None
    provider : Literal["openai", "litellm"] = "openai"
    verbose : bool = False


class CompletionArguments(PydanticBaseModel):
    """
    Base completion arguments for requests
    """
    # base
    messages : Union[List[Dict[str, str]], List[Dict[str, Any]]]
    model : Union[str, PredefinedModel] = "gpt-4o-mini"
    max_tokens : Optional[int] = None
    temperature : Optional[float] = None
    top_p : Optional[float] = None
    frequency_penalty : Optional[float] = None
    presence_penalty : Optional[float] = None
    stop : Optional[List[str]] = None
    stream : Optional[bool] = None
    kwargs : Optional[Dict[str, Any]] = None


class ToolArguments(PydanticBaseModel):
    """
    Arguments for the tool
    """
    tools : Optional[List[Dict[str, Any]]] = None
    tool_choice : Optional[str] = None
    parallel_tool_calls : Optional[bool] = None


class InstructorArguments(PydanticBaseModel):
    """
    Optional arguments for instructor completion
    """
    max_retries : Optional[int] = None
    response_model : Optional[Type[PydanticBaseModel]] = None


def build_args(
        args : CompletionArguments,
        instructor : Optional[InstructorArguments] = None,
        tool : Optional[ToolArguments] = None
) -> Dict[str, Any]:

    full_args = args.model_dump(
        exclude={
            "kwargs" if not args.kwargs else None
        }
    )

    # Add instructor arguments if provided
    if instructor:
        full_args['response_model'] = instructor.response_model

    # Add tool arguments if provided
    if tool:
        full_args['tools'] = tool.tools
        if tool.tool_choice is not None:
            full_args['tool_choice'] = tool.tool_choice
        if tool.parallel_tool_calls is not None:
            full_args['parallel_tool_calls'] = tool.parallel_tool_calls

    return full_args


class Arguments(PydanticBaseModel):
    """
    Arguments for the client
    """
    args : CompletionArguments
    instructor : Optional[InstructorArguments] = None
    tool : Optional[ToolArguments] = None


Response = Union[str, PydanticBaseModel, Generator, ChatCompletion]

# Completion Client
class Completions:
    """Base class for all LLM completions in the xnano library."""

    @staticmethod
    def format_messages(
        messages: Union[str, list[dict]] = None,
        verbose: Optional[bool] = False,
        type: Optional[Literal["user", "system", "assistant"]] = "user",
    ) -> list[dict]:
        """Formats the messages into a list of dictionaries."""
        if isinstance(messages, str):
            if verbose:
                print("Converting string to message format.")
            return [{"role": type, "content": messages}]
        elif isinstance(messages, list) and all(isinstance(m, dict) for m in messages):
            if verbose:
                print("Messages are in the correct format.")
            return messages
        raise ValueError("Invalid message format")

    @staticmethod
    def format_to_openai_tools(tools: List[Union[Dict[str, Any], Type[PydanticBaseModel], Callable]]) -> List[Dict[str, Any]]:
        """Converts the tools to a list of OpenAI-compatible tool dictionaries."""
        formatted_tools = []
        for tool in tools:
            logger.info(f"Processing tool: {tool}, type: {type(tool)}")
            try:
                openai_tool = convert_to_openai_tool(tool)
                formatted_tools.append(openai_tool)
            except Exception as e:
                logger.error(f"Error converting tool to OpenAI format: {e}")
        return formatted_tools

    @staticmethod
    def convert_to_image_message(
        message : Union[str, dict],
        image : str
    ):
        import base64
        from pathlib import Path

        # Run Image Preformatting
        # If image is a local file, convert to base64
        if Path(image).is_file():
            with open(image, "rb") as image_file:
                # Open Image in a binary read mode
                # Convert to base64
                image = base64.b64encode(image_file.read()).decode("utf-8")

        # If image is a URL, keep as is
        # Run Check if image is URL
        elif image.startswith("http") or image.startswith("https"):
            image = image

        # Run Check if image is base64
        elif image.startswith("data:image"):
            image = image

        # Run check if Message is in dict format
        if isinstance(message, dict):
            message = message['content']

        return {
            "role" : "user",
            "content" : [
            {
                "type" : "text",
                "text" : message,
            },
            {
                "type" : "image_url",
                "image_url" : {
                    "url" : image
                }
            }
            ]
        }

    @staticmethod
    def does_system_prompt_exist(messages: list[dict]) -> bool:
        """Checks if a system prompt exists in the messages."""
        return any(message.get("role") == "system" for message in messages)

    @staticmethod
    def swap_system_prompt(
        system_prompt: dict = None, messages: Union[str, list[dict[str, str]]] = None
    ):
        """Swaps the system prompt with the system_prompt."""
        messages = Completions.format_messages(messages)
        for message in messages:
            if message.get("role") == "system":
                messages.insert(0, system_prompt)
                messages.remove(message)
                break
        else:
            messages.insert(0, system_prompt)

        while len([message for message in messages if message.get("role") == "system"]) > 1:
            messages.pop()

        return messages

    @staticmethod
    def repair_messages(messages: list[dict], verbose: Optional[bool] = False) -> list[dict]:
        """Repairs the messages by performing quick logic steps."""
        if any(isinstance(message, list) for message in messages):
            messages = [item for sublist in messages for item in sublist]
            if verbose:
                print("Detected nested lists and flattened the list.")

        for i in range(len(messages) - 1):
            if isinstance(messages[i], dict):
                if messages[i].get("role") == "assistant" and (not isinstance(messages[i + 1], dict) or messages[i + 1].get("role") != "user"):
                    messages[i + 1] = {"role": "user", "content": ""}
                    if verbose:
                        print("Detected a mixmatch in message order, repaired order.")
                elif messages[i].get("role") == "user" and (not isinstance(messages[i + 1], dict) or messages[i + 1].get("role") != "assistant"):
                    messages[i + 1] = {"role": "assistant", "content": ""}
                    if verbose:
                        print("Detected a mixmatch in message order, repaired order.")

        return messages

    @staticmethod
    def add_messages(
        inputs: Union[str, list[dict], dict] = None,
        messages: list[dict] = None,
        type: Optional[Literal["user", "system", "assistant"]] = "user",
        verbose: Optional[bool] = False,
    ) -> list[dict]:
        """Adds a message to the thread."""
        if isinstance(inputs, str):
            formatted_message = Completions.format_messages(messages=inputs, verbose=verbose, type=type)
            messages.extend(formatted_message)
        elif isinstance(inputs, dict):
            messages.append(inputs)
        elif isinstance(inputs, list):
            for item in inputs:
                if isinstance(item, dict):
                    messages.append(item)
                elif verbose:
                    print(f"Skipping invalid message format: {item}")

        return Completions.repair_messages(messages, verbose)

    @staticmethod
    def recommend_client_by_model(
        model: str, base_url: Optional[str] = None, api_key: Optional[str] = None
    ) -> tuple[Literal["openai", "litellm"], Optional[str], Optional[str], Optional[str]]:
        """Recommends the client to use for the given model. Used in one-shot completions."""
        if model.startswith("ollama/"):
            model = model[7:]
            if not base_url:
                base_url = "http://localhost:11434/v1"
            if not api_key:
                api_key = "ollama"
            return "openai", model, base_url, api_key

        if base_url is not None:
            return "openai", model, base_url, api_key

        if model.startswith(("gpt-", "o1", "openai/")):
            if model.startswith("openai/"):
                model = model[7:]
            return "openai", model, base_url, api_key

        else:
            return "litellm", model, base_url, api_key

    def __init__(
            self,
            api_key : Optional[str] = None,
            base_url : Optional[str] = None,
            organization : Optional[str] = None,
            project : Optional[str] = None,
            provider : Literal["openai", "litellm"] = "openai",
            verbose : bool = False
    ):
        """
        Initialize the Completions client.

        Args:
            api_key (str): Your OpenAI API key.
            base_url (str): The base URL for the OpenAI API.
            organization (str): Your OpenAI organization.
            project (str): Your OpenAI project.
            provider (str): The provider to use for completions.
            verbose (bool): Whether to print verbose output.
            progress_bar (bool): Whether to print a progress bar. Default is True.
        """

        self.tools = []

        self.config = Config(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            project=project,
            provider=provider,
            verbose=verbose
        )

        try:
            self.client = Client(
                base = self.__init_openai_client__() if self.config.provider == "openai" else self.__init_litellm_client__(),
            )

            self.client.patch = self.__patch_openai_client__() if self.config.provider == "openai" else self.__patch_litellm_client__()
        except Exception as e:
            logger.error(f"Failed to initialize {self.config.provider} client: {e}")
            raise e

        if self.config.verbose:
            logger.info(f"Completions Client Config: {self.config}")
            logger.success("\nInitialized.")


    def __init_openai_client__(self):
        from openai import OpenAI
        
        return OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            organization=self.config.organization,
        )


    def __patch_openai_client__(self):
        from instructor import from_openai

        return from_openai(self.client.base, mode=Mode.TOOLS)


    def __init_litellm_client__(self):
        try:
            from litellm import LiteLLM

            return LiteLLM(
                api_key=self.config.api_key,
                base_url=self.config.base_url,
                organization=self.config.organization,
            )
        except ImportError:
            raise ImportError("LiteLLM not included in the base xnano package. Please install xnano[ext] or xnano[all] to use litellm.")


    def __patch_litellm_client__(self):
        from instructor import patch

        return patch(self.client.base, mode=Mode.TOOLS)


    def chat_completion(
            self,
            args: Arguments,
            progress_bar: Optional[bool] = True
    ):
        completion_args = build_args(args.args, args.instructor, args.tool)

        # Ensure tools are correctly formatted
        if 'tools' in completion_args:
            completion_args['tools'] = self.format_to_openai_tools(completion_args['tools'])

        if args.instructor:
            if args.instructor.response_model and args.args.stream:
                return self.client.patch.chat.completions.create_partial(**completion_args)
            else:
                return self.client.patch.chat.completions.create(**completion_args)
        else:
            return self.client.base.chat.completions.create(**completion_args)


    def execute_tool_call(
        self,
        tools: List[Union[Dict[str, Any], Type[PydanticBaseModel], Callable]],
        args: Arguments,
        response: Any,
    ) -> Union[Any, Arguments, None]:
        """Executes the tool calls."""
        if not response.choices[0].message.tool_calls:
            return None

        args.args.messages.append(response.choices[0].message.model_dump())
        tools_executed = False

        for tool_call in response.choices[0].message.tool_calls:
            tool = next((t for t in tools if (
                isinstance(t, dict) and t["function"]["name"] == tool_call.function.name) or
                (callable(t) and t.__name__ == tool_call.function.name) or
                (isinstance(t, type) and issubclass(t, PydanticBaseModel) and t.__name__ == tool_call.function.name)), None)

            if tool:
                if isinstance(tool, dict):
                    # Handle dictionary-based tool
                    execute_function = lambda **kwargs: "Batman"  # Replace with actual logic
                else:
                    execute_function = tool if callable(tool) else getattr(tool, 'execute', None)

                if execute_function:
                    if self.config.verbose:
                        logger.info(f"Executing tool {tool_call.function.name} with arguments {tool_call.function.arguments}")
                    try:
                        # Parse the arguments
                        call_args = json.loads(tool_call.function.arguments)

                        # Execute the function
                        tool_response = execute_function(**call_args)

                        tool_call_result_message = {"role": "tool", "content": str(tool_response), "tool_call_id": tool_call.id}
                        args.args.messages.append(tool_call_result_message)
                        tools_executed = True
                    except Exception as e:
                        logger.error(f"Error executing tool {tool_call.function.name}: {e}")
                        raise e
                else:
                    logger.warning(f"Tool {tool_call.function.name} was found but has no execute method.")
            else:
                logger.warning(f"Tool {tool_call.function.name} was called but not found.")

        if tools_executed:
            return args

        logger.warning("Tools were called, but none were executed.")
        return response


    def completion(
            self,
            messages: Union[str, List[Dict[str, str]]],
            model: Union[str, PredefinedModel] = "gpt-4o-mini",
            image: Optional[str] = None,
            response_model: Optional[PydanticBaseModel] = None,
            mode: InstructorMode = "tool_call",
            max_retries: Optional[int] = None,
            run_tools: Optional[bool] = True,
            tools: Optional[List[Union[Dict[str, Any], Type[PydanticBaseModel], Callable]]] = None,
            tool_choice: Optional[str] = None,
            parallel_tool_calls: Optional[bool] = None,
            max_tokens: Optional[int] = None,
            temperature: Optional[float] = None,
            top_p: Optional[float] = None,
            frequency_penalty: Optional[float] = None,
            presence_penalty: Optional[float] = None,
            stop: Optional[List[str]] = None,
            progress_bar: Optional[bool] = True,
            stream: Optional[bool] = None,
            **kwargs
    ):
        """Generate an LLM Completion with tools, streaming or Pydantic structured outputs.
        
        Example:
    `        ```python
            response = completion(
                messages = [{"role": "user", "content": "Hello, how are you?"}],
                model = "gpt-4o-mini",
                response_model = User,
                mode = "markdown_json_mode",
                max_retries = 3,
            ```

        Args:
            messages (Union[str, List[Dict[str, str]]]): The messages to generate a completion for.
            model (Union[str, PredefinedModel]): The model to use for the completion.
            image (Optional[str]): The image to use for the completion.
            response_model (Optional[PydanticBaseModel]): The Pydantic model to use for the completion.
            mode (InstructorMode): The mode to use for the completion.
            max_retries (Optional[int]): The maximum number of retries to use for the completion.
            run_tools (Optional[bool]): Whether to run tools for the completion.
            tools (Optional[List[Union[Dict[str, Any], Type[PydanticBaseModel], Callable]]]): The tools to use for the completion.
            tool_choice (Optional[str]): The tool choice to use for the completion.
            parallel_tool_calls (Optional[bool]): Whether to run tool calls in parallel.
            max_tokens (Optional[int]): The maximum number of tokens to use for the completion.
            temperature (Optional[float]): The temperature to use for the completion.
            top_p (Optional[float]): The top p to use for the completion.
            frequency_penalty (Optional[float]): The frequency penalty to use for the completion.
            presence_penalty (Optional[float]): The presence penalty to use for the completion.
            stop (Optional[List[str]]): The stop to use for the completion.
            progress_bar (Optional[bool]): Whether to print a progress bar.
            stream (Optional[bool]): Whether to stream the completion.
            **kwargs: Additional keyword arguments.

        Returns:
            Response[Union[str, PydanticBaseModel, Generator, ChatCompletion]]: The completion.
        """
        messages = self.format_messages(messages)

        if image:
            latest_message = messages[-1]
            latest_message = self.convert_to_image_message(latest_message, image)
            messages = messages[:-1]
            messages.append(latest_message)

        recommended_provider, recommended_model, recommended_base_url, recommended_api_key = self.recommend_client_by_model(model, self.config.base_url, self.config.api_key)

        if recommended_provider != self.config.provider or recommended_base_url != self.config.base_url or recommended_api_key != self.config.api_key:
            self.__init__(api_key=recommended_api_key or self.config.api_key,
                          base_url=recommended_base_url or self.config.base_url,
                          organization=self.config.organization,
                          provider=recommended_provider,
                          verbose=self.config.verbose)

        if model != recommended_model:
            model = recommended_model

        if tools:
            self.tools = tools  # Store the original tools
            formatted_tools = self.format_to_openai_tools(tools)
            if not formatted_tools:
                logger.warning("No valid tools were formatted. Proceeding without tools.")
        else:
            formatted_tools = None

        # Prepare arguments
        args = Arguments(
            args=CompletionArguments(
                messages=messages,
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                stream=stream,
                kwargs=kwargs
            ),
            instructor=InstructorArguments(
                response_model=response_model,
                max_retries=max_retries
            ) if response_model else None,
            tool=ToolArguments(
                tools=formatted_tools,
                tool_choice=tool_choice,
                parallel_tool_calls=parallel_tool_calls
            ) if formatted_tools else None
        )

        # If both tools and response model are present
        if response_model and formatted_tools:
            # Run tools first without response model
            args.instructor = None
            args.args.stream = False
            base_response = self.chat_completion(args)
            args = self.execute_tool_call(formatted_tools, args, base_response)

            # Re-run with response model using the updated message thread
            if isinstance(args, Arguments):
                args.instructor = InstructorArguments(
                    response_model=response_model,
                    max_retries=max_retries
                )
                args.args.stream = stream
                return self.chat_completion(args)

            return base_response

        # If only response model is present
        if response_model:
            if model.startswith("o1-"):
                logger.warning("OpenAI O1- model detected. Using JSON_O1 Instructor Mode.")
                self.client.patch.mode = Mode.JSON_O1
            else:
                self.client.patch.mode = get_mode(mode)

            if self.config.verbose:
                logger.info(f"Instructor Mode: {self.client.patch.mode}")

        # If no response model, run tools if available
        if not response_model:
            if not run_tools or not formatted_tools:
                return self.chat_completion(args)

            args.args.stream = False
            base_response = self.chat_completion(args)
            args = self.execute_tool_call(formatted_tools, args, base_response)

            if isinstance(args, Arguments):
                args.args.stream = stream
                if self.config.verbose:
                    logger.info("Re-running completion with tools executed...")
                return self.chat_completion(args)

            return base_response

        return self.chat_completion(args, progress_bar=progress_bar)


def completion(
        messages : Union[str, List[Dict[str, str]]],
        model : Union[str, PredefinedModel] = "gpt-4o-mini",
        api_key : Optional[str] = None,
        base_url : Optional[str] = None,
        organization : Optional[str] = None,
        response_model : Optional[PydanticBaseModel] = None,
        mode : InstructorMode = "tool_call",
        max_retries : Optional[int] = None,
        image : Optional[str] = None,
        run_tools : Optional[bool] = True,
        tools : Optional[List[Union[Dict[str, Any], Type[PydanticBaseModel], Callable]]] = None,
        parallel_tool_calls : Optional[bool] = None,
        tool_choice : Optional[str] = None,
        max_tokens : Optional[int] = None,
        temperature : Optional[float] = None,
        top_p : Optional[float] = None,
        frequency_penalty : Optional[float] = None,
        presence_penalty : Optional[float] = None,
        stop : Optional[List[str]] = None,
        stream : Optional[bool] = None,
        provider : Optional[Literal["openai", "litellm"]] = "openai",
        progress_bar : Optional[bool] = True,
        verbose : Optional[bool] = False,
        **kwargs
) -> Any:
    """Runs an LLM completion, with tools, streaming or Pydantic structured outputs.
    
    Example:
        ```python
        response = completion(
            messages = [{"role": "user", "content": "Hello, how are you?"}],
            model = "gpt-4o-mini",
            response_model = User,
            mode = "markdown_json_mode",
            max_retries = 3,
            stream = True,
        )
        for chunk in response:
            print(chunk)
        ```

    Args:
        messages (Union[str, List[Dict[str, str]]]): The messages to generate a completion for.
        model (Union[str, PredefinedModel]): The model to use for the completion.
        api_key (Optional[str]): The API key to use for the completion.
        base_url (Optional[str]): The base URL to use for the completion.
        organization (Optional[str]): The organization to use for the completion.
        response_model (Optional[PydanticBaseModel]): The Pydantic model to use for the completion.
        mode (InstructorMode): The mode to use for the completion.
        max_retries (Optional[int]): The maximum number of retries to use for the completion.
        image (Optional[str]): The image to use for the completion.
        run_tools (Optional[bool]): Whether to run tools for the completion.
        tools (Optional[List[Union[Dict[str, Any], Type[PydanticBaseModel], Callable]]]): The tools to use for the completion.
        parallel_tool_calls (Optional[bool]): Whether to run tool calls in parallel.
        tool_choice (Optional[str]): The tool choice to use for the completion.
        max_tokens (Optional[int]): The maximum number of tokens to use for the completion.
        temperature (Optional[float]): The temperature to use for the completion.
        top_p (Optional[float]): The top p to use for the completion.
        frequency_penalty (Optional[float]): The frequency penalty to use for the completion.
        presence_penalty (Optional[float]): The presence penalty to use for the completion.
        stop (Optional[List[str]]): The stop to use for the completion.
        stream (Optional[bool]): Whether to stream the completion.
        provider (Optional[Literal["openai", "litellm"]]): The provider to use for the completion.
        progress_bar (Optional[bool]): Whether to print a progress bar.
        verbose (Optional[bool]): Whether to print verbose output.
        **kwargs: Additional keyword arguments.

    Returns:
        Response[Union[str, PydanticBaseModel, Generator, ChatCompletion]]: The completion.
    """

    client = Completions(
        api_key=api_key,
        base_url=base_url,
        organization=organization,
        provider=provider,
        verbose=verbose
    )

    if stream:
        progress_bar = False

    if progress_bar:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True
        ) as progress:
            task_id = progress.add_task("Generating Completion...", total=None)

            response = client.completion(
                messages=messages,
                model=model,
                image=image,
                response_model=response_model,
                mode=mode,
                max_retries=max_retries,
                run_tools=run_tools,
                tools=tools,
                parallel_tool_calls=parallel_tool_calls,
                tool_choice=tool_choice,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                progress_bar=progress_bar,
                stream=stream,
                **kwargs
            )

            progress.update(task_id, completed=1)

            return response

    else:
        return client.completion(
                messages=messages,
                model=model,
                image=image,
                response_model=response_model,
                mode=mode,
                max_retries=max_retries,
                run_tools=run_tools,
                tools=tools,
                parallel_tool_calls=parallel_tool_calls,
                tool_choice=tool_choice,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                frequency_penalty=frequency_penalty,
                presence_penalty=presence_penalty,
                stop=stop,
                progress_bar=progress_bar,
                stream=stream,
                **kwargs
            )
    

# Pydantic BaseModel Subclass Client
class BaseModel(PydanticBaseModel):

    @overload
    @classmethod
    def generate(
        cls: Type[T],
        instructions: Optional[str] = None,
        n: int = 1,
        process: Literal["batch", "sequential"] = "batch",
        client: Optional[Literal["litellm", "openai"]] = None,
        model : Union[str, PredefinedModel] = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        temperature: float = 0,
        mode: InstructorMode = "markdown_json_mode",
        verbose: bool = False,
        progress_bar: Optional[bool] = True,
    ) -> Union[T, List[T]]: ...

    @overload
    def generate(
        self: T,
        instructions: Optional[str] = None,
        n: int = 1,
        process: Literal["batch", "sequential"] = "batch",
        client: Optional[Literal["litellm", "openai"]] = None,
        model : Union[str, PredefinedModel] = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        temperature: float = 0,
        mode: InstructorMode = "markdown_json_mode",
        verbose: bool = False,
        progress_bar: Optional[bool] = True,
    ) -> Union[T, List[T]]: ...

    @classmethod
    def generate(
        cls_or_self: Union[Type[T], T],
        instructions: Optional[str] = None,
        n: int = 1,
        process: Literal["batch", "sequential"] = "batch",
        client: Optional[Literal["litellm", "openai"]] = "openai",
        model : Union[str, PredefinedModel] = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        temperature: float = 0,
        mode: InstructorMode = "markdown_json_mode",
        verbose: bool = False,
        progress_bar: Optional[bool] = True,
    ) -> Union[T, List[T]]:
        """Generates instance(s) of the given Pydantic model.
        
        Example:
            ```python
            class PersonModel(PydanticBaseModel):
                secret_identity: str
                name: str
                age: int

            PersonModel.generate(n=2)
            ```

        Args:
            cls_or_self (Union[Type[T], T]): The class or instance of the Pydantic model.
            instructions (Optional[str]): The instructions to use for the generation.
            n (int): The number of instances to generate.
            model (str): The model to use for the generation.
            api_key (Optional[str]): The API key to use for the generation.
            base_url (Optional[str]): The base URL to use for the generation.
            organization (Optional[str]): The organization to use for the generation.
            max_tokens (Optional[int]): The maximum number of tokens to use for the generation.
            max_retries (int): The maximum number of retries to use for the generation.
            temperature (float): The temperature to use for the generation.
            mode (InstructorMode): The mode to use for the generation.
            progress_bar (Optional[bool]): Whether to print a progress bar.
            verbose (bool): Whether to print verbose output.

        Returns:
            Union[T, List[T]]: The generated instance(s).
        """
        cls = cls_or_self if isinstance(cls_or_self, type) else type(cls_or_self)

        ResponseModel = cls if n == 1 else create_model("ResponseModel", items=(List[cls], ...))

        system_message = (
            f"You are a data generator. Your task is to generate {n} valid instance(s) of the following Pydantic model:\n\n"
            f"{cls.model_json_schema()}\n\n"
            f"Ensure that all generated instances comply with the model's schema and constraints."
        )

        if isinstance(cls_or_self, BaseModel):
            system_message += f"\n\nUse the following instance as a reference or starting point:\n{cls_or_self.model_dump_json()}"

        system_message += "\nALWAYS COMPLY WITH USER INSTRUCTIONS FOR CONTENT TOPICS & GUIDELINES."

        user_message = instructions or f"Generate {n} instance(s) of the given model."

        if verbose:
            logger.info(f"Template: {system_message}")
            logger.info(f"Instructions: {user_message}")

        completion_client = Completions(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            provider=client,
            verbose=verbose,
        )

        if process == "batch":

            if progress_bar:

                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task_id = progress.add_task("Generating Model(s)...", total=None)
                    
                    response = completion_client.completion(
                        messages=[
                            {"role": "system", "content": system_message},
                            {"role": "user", "content": user_message},
                        ],
                        model=model,
                        max_tokens=max_tokens,
                        max_retries=max_retries,
                        temperature=temperature,
                        mode="markdown_json_mode" if model.startswith(("ollama/", "ollama_chat/")) else mode,
                        response_model=ResponseModel,
                    )

                    progress.update(task_id, completed=1)

            else:
                response = completion_client.completion(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    model=model,
                    max_tokens=max_tokens,
                    max_retries=max_retries,
                    temperature=temperature,
                    mode="markdown_json_mode" if model.startswith(("ollama/", "ollama_chat/")) else mode,
                )

            return response if n == 1 else response.items
        else:  # Sequential generation
            results = []

            if progress_bar:
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    transient=True
                ) as progress:
                    task_id = progress.add_task("Generating Model(s)...", total=None)

                    for i in range(n):
                        instance: Dict[str, Any] = {}
                        for field_name, field in cls.model_fields.items():
                            field_system_message = (
                                f"You are a data generator. Your task is to generate a valid value for the following field:\n\n"
                                f"Field name: {field_name}\n"
                                f"Field type: {field.annotation}\n"
                                f"Field constraints: {field.json_schema_extra}\n\n"
                                f"Ensure that the generated value complies with the field's type and constraints.\n\n"
                                f"ALWAYS COMPLY WITH USER INSTRUCTIONS FOR CONTENT TOPICS & GUIDELINES."
                            )
                            field_user_message = f"Generate a value for the '{field_name}' field."

                            if instance:
                                field_user_message += f"\nCurrent partial instance: {instance}"

                            if i > 0:
                                field_user_message += "\n\nPrevious generations for this field:"
                                for j, prev_instance in enumerate(results[-min(3, i):], 1):
                                    field_user_message += f"\n{j}. {getattr(prev_instance, field_name)}"
                                field_user_message += "\n\nPlease generate a different value from these previous ones."

                            field_user_message += f"\n\nUSER INSTRUCTIONS DEFINED BELOW FOR CONTENT & GUIDELINES\n\n<instructions>\n{instructions or 'No additional instructions provided.'}\n</instructions>"

                            field_response = completion_client.completion(
                                messages=[
                                    {"role": "system", "content": field_system_message},
                                    {"role": "user", "content": field_user_message},
                                ],
                                model=model,
                                max_tokens=max_tokens,
                                max_retries=max_retries,
                                temperature=temperature,
                                mode="markdown_json_mode" if model.startswith(("ollama/", "ollama_chat/")) else mode,
                                response_model=create_model("FieldResponse", value=(field.annotation, ...)),
                            )
                            instance[field_name] = field_response.value

                        results.append(cls(**instance))

                        progress.update(task_id, completed=i + 1)
            else:

                for i in range(n):
                    instance: Dict[str, Any] = {}
                    for field_name, field in cls.model_fields.items():
                        field_system_message = (
                            f"You are a data generator. Your task is to generate a valid value for the following field:\n\n"
                            f"Field name: {field_name}\n"
                            f"Field type: {field.annotation}\n"
                            f"Field constraints: {field.json_schema_extra}\n\n"
                            f"Ensure that the generated value complies with the field's type and constraints.\n\n"
                            f"ALWAYS COMPLY WITH USER INSTRUCTIONS FOR CONTENT TOPICS & GUIDELINES."
                        )
                        field_user_message = f"Generate a value for the '{field_name}' field."

                        if instance:
                            field_user_message += f"\nCurrent partial instance: {instance}"

                        if i > 0:
                            field_user_message += "\n\nPrevious generations for this field:"
                            for j, prev_instance in enumerate(results[-min(3, i):], 1):
                                field_user_message += f"\n{j}. {getattr(prev_instance, field_name)}"
                            field_user_message += "\n\nPlease generate a different value from these previous ones."

                        field_user_message += f"\n\nUSER INSTRUCTIONS DEFINED BELOW FOR CONTENT & GUIDELINES\n\n<instructions>\n{instructions or 'No additional instructions provided.'}\n</instructions>"

                        field_response = completion_client.completion(
                            messages=[
                                {"role": "system", "content": field_system_message},
                                {"role": "user", "content": field_user_message},
                            ],
                            model=model,
                            max_tokens=max_tokens,
                            max_retries=max_retries,
                            temperature=temperature,
                            mode="markdown_json_mode" if model.startswith(("ollama/", "ollama_chat/")) else mode,
                            response_model=create_model("FieldResponse", value=(field.annotation, ...)),
                        )
                        instance[field_name] = field_response.value

                    results.append(cls(**instance))

            return results[0] if n == 1 else results
        

    @classmethod
    def select(
        cls: Type[T],
        field_name: str,
        instructions: Optional[str] = None,
        n: int = 1,
        model : Union[str, PredefinedModel] = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        temperature: float = 0.7,
        mode: InstructorMode = "markdown_json_mode",
        progress_bar: Optional[bool] = True,
        verbose: bool = False,
    ) -> Union[enum.Enum, List[enum.Enum]]:
        """Selects values for an Enum field.
        
        Example:
            ```python
            class PersonModel(PydanticBaseModel):
                secret_identity: str
                name: str
                age: int

            PersonModel.select(field_name="secret_identity", instructions="Select a secret identity for the person.")
            ```
        
        Args:
            cls (Type[T]): The class of the Pydantic model.
            field_name (str): The name of the Enum field to select values for.
            instructions (Optional[str]): The instructions to use for the selection.
            n (int): The number of values to select.
            model (str): The model to use for the selection.
            api_key (Optional[str]): The API key to use for the selection.
            base_url (Optional[str]): The base URL to use for the selection.
            organization (Optional[str]): The organization to use for the selection.
            max_tokens (Optional[int]): The maximum number of tokens to use for the selection.
            max_retries (int): The maximum number of retries to use for the selection.
            temperature (float): The temperature to use for the selection.
            mode (InstructorMode): The mode to use for the selection.
            progress_bar (Optional[bool]): Whether to print a progress bar.
            verbose (bool): Whether to print verbose output.

        Returns:
            Union[enum.Enum, List[enum.Enum]]: The selected values.
        """
        if field_name not in cls.model_fields or not issubclass(cls.model_fields[field_name].annotation, enum.Enum):
            raise ValueError(f"'{field_name}' is not an Enum field in this model.")

        enum_class = cls.model_fields[field_name].annotation
        enum_values = [e.value for e in enum_class]

        completion_client = Completions(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            provider="openai",
            verbose=verbose,
        )

        if progress_bar:
            start_time = time()

            with Progress(
                SpinnerColumn(),
                *Progress.get_default_columns(),
                TimeElapsedColumn(),
                transient=True
            ) as progress:

                system_message = (
                    f"You are an AI assistant helping to select values for an Enum field.\n\n"
                    f"Field name: {field_name}\n"
                    f"Possible values: {enum_values}\n\n"
                    f"Your task is to select {n} appropriate value(s) from the given options and explain your reasoning."
                )

                user_message = (
                    f"Please select {n} value(s) for the '{field_name}' field.\n\n"
                    f"Instructions: {instructions or 'No additional instructions provided.'}"
                )

                ResponseModel = create_model(
                    "ResponseModel",
                    selections=(List[str], ...),
                    explanations=(List[str], ...)
                )

                response = completion_client.completion(
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": user_message},
                    ],
                    model=model,
                    max_tokens=max_tokens,
                    max_retries=max_retries,
                    temperature=temperature,
                    mode=mode,
                    response_model=ResponseModel,
                )

                results = [enum_class(selection) for selection in response.selections]

                if verbose:
                    for selection, explanation in zip(results, response.explanations):
                        logger.info(f"Selected: {selection}")
                        logger.info(f"Explanation: {explanation}")

                elapsed_time = time() - start_time
                progress.update(
                    SpinnerColumn(),
                    *Progress.get_default_columns(),
                    TimeElapsedColumn(),
                    transient=True
                )

        else:

            response = completion_client.completion(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                model=model,
                max_tokens=max_tokens,
                max_retries=max_retries,
                temperature=temperature,
                mode=mode,
                response_model=ResponseModel,
            )

            results = [enum_class(selection) for selection in response.selections]

            if verbose:
                for selection, explanation in zip(results, response.explanations):
                    logger.info(f"Selected: {selection}")
                    logger.info(f"Explanation: {explanation}")
            

        return results[0] if n == 1 else results


if __name__ == "__main__":
    class PersonModel(PydanticBaseModel):
        secret_identity: str
        name: str
        age: int

    def get_secret_identity():
        """
        Get the secret identity of a person.
        """
        return "Batman"

    print(completion("Who is SpiderMan", verbose=True, response_model=PersonModel))

    print(completion(messages="What is my secret identity?", tools=[get_secret_identity]))

    print(completion(messages="What is my secret identity?", tools=[get_secret_identity], response_model=PersonModel))
