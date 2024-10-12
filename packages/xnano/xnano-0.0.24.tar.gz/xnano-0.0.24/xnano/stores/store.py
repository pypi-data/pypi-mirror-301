try:
    from chromadb import Client as ChromaClient
    from chromadb.config import Settings
    from chromadb.utils import embedding_functions
    from loguru import logger
    from typing import Any, Dict, Callable, List, Union, Optional, Literal, Type
    import uuid
    from pathlib import Path
    from openai import OpenAI


    from .. import completion, InstructorMode, BaseModel, Field, Completions, PredefinedModel
    from ..lib.chunk import chunker as chunk
    from ..lib.generate import generator as generate
    from ..lib.read import reader
except ImportError:

    import os
    from rich.console import Console
    console = Console()
    with console.status("[bold green]Loading data...[/bold green]"):
        print(
            "The [bold]`xnano(data)`[/bold] data extension is required to use this module. Install it?"
            "\n[bold]`pip install 'xnano[data]'`[/bold]"
        )
    if input("Install? (y/n)") == "y":
        os.system("pip install 'xnano[data]'")
        exit(1)
    else:
        print("Exiting...")
        exit(1)


from pydantic import BaseModel, create_model
from typing import Any, Dict, List, Optional, Type, Literal, TypeVar


T = TypeVar("T", bound=BaseModel)


class Document(BaseModel):
    """
    A document model that can be used to store and query documents.

    Attributes:
        content (Any): The content of the document.
        metadata (Dict[str, Any]): The metadata of the document.
        messages (Optional[List[Dict[str, Any]]]): The messages of the document.
    """

    content: Any
    metadata: Dict[str, Any]
    messages: Optional[List[Dict[str, Any]]] = []

    class Config:
        arbitrary_types_allowed = True

    def setup_messages(self):
        """
        Setup the messages for the document.
        """
        self.messages = [
            {
                "role": "system",
                "content": """
You are a world class document understanding assistant. You are able to
understand the content of a document and answer questions about it.
""",
            },
            {"role": "user", "content": "What is the document?"},
            {
                "role": "assistant",
                "content": f"""
Here's a full overview of the document! \n
Document Metadata: {self.metadata} \n\n
Document Content: {self.content}
""",
            },
        ]

    def generate(
        self,
        target: Type[T],
        instructions: Optional[str] = None,
        n: int = 1,
        process: Literal["batch", "sequential"] = "batch",
        client: Literal["litellm", "openai"] = "openai",
        model: Union[str, PredefinedModel] = "gpt-4o-mini",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 3,
        temperature: float = 0,
        mode: InstructorMode = "markdown_json_mode",
        verbose: bool = False,
    ) -> List[T]:
        """
        Generates a list of instances of the specified Pydantic model using the document's content as context.

        Example:
        ```python
        from zyx import Document

        doc = Document(content="Hello, world!", metadata={"file_name": "file.txt"}, messages=[])
        doc.generate(target=User, instructions="Tell me a joke.")
        ```

        Args:
            target (Type[T]): The Pydantic model to generate instances of.
            instructions (Optional[str]): The instructions for the generation.
            n (int): The number of instances to generate.
            process (Literal["batch", "sequential"]): The process to use for the generation.
            client (Literal["litellm", "openai"]): The client to use for the generation.
            model (str): The model to use for the generation.
            api_key (Optional[str]): The API key to use for the generation.
            base_url (Optional[str]): The base URL to use for the generation.
            organization (Optional[str]): The organization to use for the generation.
            max_tokens (Optional[int]): The maximum number of tokens to generate.
            max_retries (int): The maximum number of retries to use for the generation.
            temperature (float): The temperature to use for the generation.
            mode (InstructorMode): The mode to use for the generation.
            verbose (bool): Whether to print the messages to the console.

        Returns:
            List[T]: A list of instances of the specified Pydantic model.
        """
        if not self.messages:
            self.setup_messages()

        if n == 1:
            ResponseModel = target
        else:
            ResponseModel = create_model("ResponseModel", items=(List[target], ...))

        system_message = f"""
        You are a data generator with access to the following document:

        Document Metadata: {self.metadata}
        Document Content: {self.content}

        Your task is to generate {n} valid instance(s) of the following Pydantic model:

        {target.model_json_schema()}

        Use the document's content as context for generating these instances.
        Ensure that all generated instances comply with the model's schema and constraints.
        """
        user_message = (
            instructions
            if instructions
            else f"Generate {n} instance(s) of the given model using the document's content as context."
        )

        completion_client = Completions(
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            provider=client,
            verbose=verbose,
        )

        if process == "batch":
            response = completion_client.completion(
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_message},
                ],
                model=model,
                max_tokens=max_tokens,
                max_retries=max_retries,
                temperature=temperature,
                mode="markdown_json_mode"
                if model.startswith(("ollama/", "ollama_chat/"))
                else mode,
                response_model=ResponseModel,
            )
            return [response] if n == 1 else response.items
        else:  # Sequential generation
            results = []
            for i in range(n):
                instance = {}
                for field_name, field in target.model_fields.items():
                    field_system_message = f"""
                    You are a data generator with access to the following document:

                    Document Metadata: {self.metadata}
                    Document Content: {self.content}

                    Your task is to generate a valid value for the following field:

                    Field name: {field_name}
                    Field type: {field.annotation}
                    Field constraints: {field.json_schema_extra}

                    Use the document's content as context for generating this value.
                    Ensure that the generated value complies with the field's type and constraints.
                    """
                    field_user_message = f"Generate a value for the '{field_name}' field using the document's content as context."
                    if instance:
                        field_user_message += f"\nCurrent partial instance: {instance}"

                    if i > 0:
                        field_user_message += (
                            f"\n\nPrevious generations for this field:"
                        )
                        for j, prev_instance in enumerate(results[-min(3, i) :], 1):
                            field_user_message += (
                                f"\n{j}. {getattr(prev_instance, field_name)}"
                            )
                        field_user_message += "\n\nPlease generate a different value from these previous ones."

                    field_response = completion_client.completion(
                        messages=[
                            {"role": "system", "content": field_system_message},
                            {"role": "user", "content": field_user_message},
                        ],
                        model=model,
                        max_tokens=max_tokens,
                        max_retries=max_retries,
                        temperature=temperature,
                        mode="markdown_json_mode"
                        if model.startswith(("ollama/", "ollama_chat/"))
                        else mode,
                        response_model=create_model(
                            "FieldResponse", value=(field.annotation, ...)
                        ),
                    )
                    instance[field_name] = field_response.value

                results.append(target(**instance))

            return results

    def completion(
        self,
        prompt: str,
        model: Union[str, PredefinedModel] = "gpt-4o-mini",
        client: Literal["openai", "litellm"] = "openai",
        response_model: Optional[Type[BaseModel]] = None,
        mode: Optional[InstructorMode] = "tool_call",
        max_retries: Optional[int] = 3,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        organization: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        frequency_penalty: Optional[float] = None,
        presence_penalty: Optional[float] = None,
        stop: Optional[List[str]] = None,
        stream: Optional[bool] = False,
        verbose: Optional[bool] = False,
    ):
        """
        Generates a completion for the document.

        Example:
        ```python
        from zyx import Document

        doc = Document(content="Hello, world!", metadata={"file_name": "file.txt"}, messages=[])
        doc.completion(prompt="Tell me a joke.")
        ```

        Args:
            prompt (str): The prompt to use for the completion.
            model (str): The model to use for the completion.
            client (Literal["openai", "litellm"]): The client to use for the completion.
            response_model (Optional[Type[BaseModel]]): The response model to use for the completion.
            mode (Optional[InstructorMode]): The mode to use for the completion.
            max_retries (Optional[int]): The maximum number of retries to use for the completion.
            api_key (Optional[str]): The API key to use for the completion.
            base_url (Optional[str]): The base URL to use for the completion.
            organization (Optional[str]): The organization to use for the completion.
            run_tools (Optional[bool]): Whether to run the tools for the completion.
            tools (Optional[List[ToolType]]): The tools to use for the completion.
            parallel_tool_calls (Optional[bool]): Whether to run the tools in parallel.
            tool_choice (Optional[Literal["none", "auto", "required"]]): The tool choice to use for the completion.
            max_tokens (Optional[int]): The maximum number of tokens to generate.
            temperature (Optional[float]): The temperature to use for the completion.
            top_p (Optional[float]): The top p to use for the completion.
            frequency_penalty (Optional[float]): The frequency penalty to use for the completion.
            presence_penalty (Optional[float]): The presence penalty to use for the completion.
            stop (Optional[List[str]]): The stop to use for the completion.
            stream (Optional[bool]): Whether to stream the completion.
            verbose (Optional[bool]): Whether to print the messages to the console.

        """

        if not self.messages:
            self.setup_messages()

        self.messages.append({"role": "user", "content": prompt})

        response = completion(
            messages=self.messages,
            model=model,
            client=client,
            mode=mode,
            max_retries=max_retries,
            api_key=api_key,
            base_url=base_url,
            organization=organization,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stop=stop,
            stream=stream,
            verbose=verbose,
        )

        if response:
            self.messages.append(
                {"role": "assistant", "content": response.choices[0].message.content}
            )

        return response    


class ChromaNode(BaseModel):
    id: str
    text: str
    embedding: List[float]
    metadata: Optional[dict] = None


class SearchResponse(BaseModel):
    query: str
    results: List[ChromaNode] = Field(default_factory=list)


class SummaryResponse(BaseModel):
    summary: str


EmbeddingModel = Literal["text-embedding-3-small", "text-embedding-3-large",
                         "ollama/nomic-embed-text", "ollama/mxbai-embed-large",
                         "ollama/all-minilm"]


def embeddings(
    text : str,
    model : Union[str, EmbeddingModel] = "text-embedding-3-small",
    dimensions : int = 1536,
    api_key : Optional[str] = None,
    base_url : Optional[str] = None,
    organization : Optional[str] = None,
) -> List[float]:
    
    if model.startswith("ollama/"):
        model = model[7:]

        if not base_url:
            base_url = "http://localhost:11434/v1"
        if not api_key:
            api_key = "ollama"
    
    try:
    
        client = OpenAI(api_key=api_key, base_url=base_url, organization=organization)

        return client.embeddings.create(input=text, model=model, dimensions=dimensions).data[0].embedding
    
    except Exception as e:
        logger.error(f"Error generating embeddings: {e}")
        raise


class CustomEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, api_key: str, model: Union[str, EmbeddingModel] = "text-embedding-3-small", dimensions: int = 1536, base_url: Optional[str] = None, organization: Optional[str] = None):
        self.api_key = api_key
        self.model = model
        self.dimensions = dimensions
        self.base_url = base_url
        self.organization = organization

    def __call__(self, texts: List[str]) -> List[List[float]]:
        return [embeddings(text, model=self.model, dimensions=self.dimensions, api_key=self.api_key, base_url=self.base_url, organization=self.organization) for text in texts]

class Store:
    """
    Class for storing and retrieving data using Chroma.
    """

    def __init__(
        self,
        collection_name: str = "my_collection",
        model_class: Optional[Type[BaseModel]] = None,
        embedding_model: Union[str, EmbeddingModel] = "text-embedding-3-small",
        embedding_api_key: Optional[str] = None,
        embedding_dimensions: int = 1536,
        embedding_base_url: Optional[str] = None,
        embedding_organization: Optional[str] = None,
        location: Union[Literal[":memory:"], str] = ":memory:",
        persist_directory: str = "chroma_db",
        chunk_size: int = 512,
        model: Union[str, PredefinedModel] = "gpt-4o-mini",
    ):
        """
        Class for storing and retrieving data using Chroma.

        Args:
            collection_name (str): The name of the collection.
            model_class (Type[BaseModel], optional): Model class for storing data.
            embedding_api_key (str, optional): API key for embedding model.
            location (str): ":memory:" for in-memory database or a string path for persistent storage.
            persist_directory (str): Directory for persisting Chroma database (if not using in-memory storage).
            chunk_size (int): Size of chunks for text splitting.
            model (str): Model name for text summarization.
        """

        self.embedding_model = embedding_model
        self.collection_name = collection_name
        self.embedding_api_key = embedding_api_key
        self.embedding_dimensions = embedding_dimensions
        self.embedding_base_url = embedding_base_url
        self.embedding_organization = embedding_organization
        self.model_class = model_class
        self.location = location
        self.persist_directory = persist_directory
        self.chunk_size = chunk_size
        self.model = model

        self.client = self._initialize_client()
        self.collection = self._create_or_get_collection()

    def _initialize_client(self):
        """
        Initialize Chroma client. Use in-memory database if location is ":memory:",
        otherwise, use persistent storage at the specified directory.
        """
        if self.location == ":memory:":
            logger.info("Using in-memory Chroma storage.")
            return ChromaClient()  # In-memory by default
        else:
            logger.info(f"Using persistent Chroma storage at {self.persist_directory}.")
            settings = Settings(persist_directory=self.persist_directory)
            return ChromaClient(settings)

    def _create_or_get_collection(self):
        """Retrieve or create a Chroma collection with a custom embedding function."""
        self.embedding_function = CustomEmbeddingFunction(api_key=self.embedding_api_key, model=self.embedding_model, dimensions=self.embedding_dimensions, base_url=self.embedding_base_url, organization=self.embedding_organization)
        if self.collection_name in self.client.list_collections():
            logger.info(f"Collection '{self.collection_name}' already exists.")
            return self.client.get_collection(
                self.collection_name, embedding_function=self.embedding_function
            )
        else:
            logger.info(f"Creating collection '{self.collection_name}'.")
            return self.client.create_collection(
                name=self.collection_name, embedding_function=self.embedding_function
            )

    def _get_embedding(self, text: str) -> List[float]:
        """Generate embeddings for a given text using the custom embedding function.

        Args:
            text (str): The text to generate an embedding for.

        Returns:
            List[float]: The embedding for the text.
        """
        return self.embedding_function([text])[0]
        

    def add(
        self,
        data: Union[str, List[str], Document, List[Document]],
        chunk_size: int = 512,
        metadata: Optional[dict] = None,
    ):
        """Add documents or data to Chroma.

        Args:
            data (Union[str, List[str], Document, List[Document]]): The data to add to Chroma.
            metadata (Optional[dict]): The metadata to add to the data.
        """
        if isinstance(data, str):
            data = [data]
        elif isinstance(data, Document):
            data = [data]

        ids, embeddings, texts, metadatas = [], [], [], []

        for item in data:
            try:
                if isinstance(item, Document):
                    text = item.content
                    metadata = item.metadata
                else:
                    text = item

                # Chunk the content
                chunks = chunk(text, chunk_size=chunk_size, model=self.model)

                for chunk_text in chunks:
                    embedding_vector = self._get_embedding(chunk_text)
                    ids.append(str(uuid.uuid4()))
                    embeddings.append(embedding_vector)
                    texts.append(chunk_text)
                    chunk_metadata = metadata.copy() if metadata else {}
                    chunk_metadata["chunk"] = True
                    metadatas.append(chunk_metadata)
            except Exception as e:
                logger.error(f"Error processing item: {item}. Error: {e}")

        if embeddings:
            try:
                # Ensure metadatas is not empty
                metadatas = [m if m else {"default": "empty"} for m in metadatas]
                self.collection.add(
                    ids=ids, embeddings=embeddings, metadatas=metadatas, documents=texts
                )
                logger.info(
                    f"Successfully added {len(embeddings)} chunks to the collection."
                )
            except Exception as e:
                logger.error(f"Error adding points to collection: {e}")
        else:
            logger.warning("No valid embeddings to add to the collection.")

    def search(self, query: str, top_k: int = 5) -> SearchResponse:
        """Search in Chroma collection.

        Args:
            query (str): The query to search for.
            top_k (int): The number of results to return.

        Returns:
            SearchResponse: The search results.
        """
        try:
            query_embedding = self._get_embedding(query)
            search_results = self.collection.query(
                query_embeddings=[query_embedding], n_results=top_k
            )

            nodes = []
            for i in range(len(search_results["ids"][0])):  # Note the [0] here
                node = ChromaNode(
                    id=search_results["ids"][0][i],
                    text=search_results["documents"][0][i],
                    embedding=query_embedding,
                    metadata=search_results["metadatas"][0][i]
                    if search_results["metadatas"]
                    else {},
                )
                nodes.append(node)
            return SearchResponse(query=query, results=nodes)
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return SearchResponse(query=query)  # Return empty results on error

    def _summarize_results(self, results: List[ChromaNode]) -> str:
        """Summarize the search results.

        Args:
            results (List[ChromaNode]): The search results.

        Returns:
            str: The summary of the search results.
        """

        class SummaryModel(BaseModel):
            summary: str

        texts = [node.text for node in results]
        combined_text = "\n\n".join(texts)

        summary = generate(
            SummaryModel,
            instructions="Provide a concise summary of the following text, focusing on the most important information:",
            model=self.model,
            n=1,
        )

        return summary.summary

    def completion(
        self,
        messages: Union[str, List[dict]] = None,
        model: Optional[str] = None,
        top_k: Optional[int] = 5,
        tools: Optional[List[Union[Callable, dict, BaseModel]]] = None,
        run_tools: Optional[bool] = True,
        response_model: Optional[BaseModel] = None,
        mode: Optional[InstructorMode] = "tool_call",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        organization: Optional[str] = None,
        top_p: Optional[float] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: Optional[int] = 3,
        verbose: Optional[bool] = False,
    ):
        """Perform completion with context from Chroma.

        Args:
            messages (Union[str, List[dict]]): The messages to use for the completion.
            model (Optional[str]): The model to use for the completion.
            top_k (Optional[int]): The number of results to return from the search.
            tools (Optional[List[Union[Callable, dict, BaseModel]]]): The tools to use for the completion.
            run_tools (Optional[bool]): Whether to run the tools for the completion.
            response_model (Optional[BaseModel]): The response model to use for the completion.
            mode (Optional[InstructorMode]): The mode to use for the completion.
            base_url (Optional[str]): The base URL to use for the completion.
            api_key (Optional[str]): The API key to use for the completion.
            organization (Optional[str]): The organization to use for the completion.
            top_p (Optional[float]): The top p to use for the completion.
            temperature (Optional[float]): The temperature to use for the completion.
            max_tokens (Optional[int]): The maximum number of tokens to generate.
            max_retries (Optional[int]): The maximum number of retries to use for the completion.
            verbose (Optional[bool]): Whether to print the messages to the console.
        """
        logger.info(f"Initial messages: {messages}")

        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        elif isinstance(messages, list):
            messages = [
                {"role": "user", "content": m} if isinstance(m, str) else m
                for m in messages
            ]

        query = messages[-1].get("content", "") if messages else ""

        try:
            results = self.search(query, top_k=top_k)
            summarized_results = self._summarize_results(results.results)
        except Exception as e:
            logger.error(f"Error during search or summarization: {e}")
            summarized_results = ""

        if messages:
            if not any(message.get("role", "") == "system" for message in messages):
                system_message = {
                    "role": "system",
                    "content": f"Relevant information retrieved: \n {summarized_results}",
                }
                messages.insert(0, system_message)
            else:
                for message in messages:
                    if message.get("role", "") == "system":
                        message["content"] += (
                            f"\nAdditional context: {summarized_results}"
                        )

        try:
            result = completion(
                messages=messages,
                model=model or self.model,
                tools=tools,
                run_tools=run_tools,
                response_model=response_model,
                mode=mode,
                base_url=base_url,
                api_key=api_key,
                organization=organization,
                top_p=top_p,
                temperature=temperature,
                max_tokens=max_tokens,
                max_retries=max_retries,
            )

            if verbose:
                logger.info(f"Completion result: {result}")

            return result
        except Exception as e:
            logger.error(f"Error during completion: {e}")
            raise


    def add_docs(
            self,
            path : Union[str, Path],
            model : Union[str, EmbeddingModel] = "text-embedding-3-small",
            api_key : Optional[str] = None,
            base_url : Optional[str] = None,
            organization : Optional[str] = None,
    ):
        docs = reader(path, target="text")

        for doc in docs:
            self.add(doc.content)


if __name__ == "__main__":
    try:
        # Initialize the Store
        store = Store(
            collection_name="test_collection", embedding_api_key="your-api-key"
        )

        # Test adding single string
        store.add("This is a single string test.")
        print("Added single string.")

        # Test adding list of strings
        store.add(
            [
                "Multiple string test 1",
                "Multiple string test 2",
                "Multiple string test 3",
            ]
        )
        print("Added multiple strings.")

        # Test adding Document
        doc = Document(content="Document test content", metadata={"source": "test"})
        store.add(doc)
        print("Added Document.")

        # Test adding list of Documents
        docs = [
            Document(content="Document 1 content", metadata={"source": "test1"}),
            Document(content="Document 2 content", metadata={"source": "test2"}),
        ]
        store.add(docs)
        print("Added multiple Documents.")

        # Test search
        search_query = "test"
        results = store.search(search_query, top_k=3)
        print(f"\nSearch results for '{search_query}':")
        for result in results.results:
            print(f"ID: {result.id}, Text: {result.text}, Metadata: {result.metadata}")

        # Test search with more results than in collection
        large_k_results = store.search(search_query, top_k=100)
        print(f"\nSearch results with large top_k (100):")
        print(f"Number of results returned: {len(large_k_results.results)}")

        # Test completion
        completion_query = "What is the main topic of the documents?"
        completion_result = store.completion(completion_query)
        print(f"\nCompletion result for '{completion_query}':")
        print(completion_result)

        # Test completion with custom model and parameters
        custom_completion = store.completion(
            messages=[{"role": "user", "content": "Summarize the documents."}],
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=150,
        )
        print("\nCustom completion result:")
        print(custom_completion)

    except Exception as e:
        logger.error(f"Error in main execution: {e}")
