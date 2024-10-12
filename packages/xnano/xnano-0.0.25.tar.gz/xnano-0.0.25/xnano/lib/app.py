from rich.console import Console
from .. import PredefinedModel, Completions
from typing import Union, Optional
import typer


def chat_app(
        model: str = typer.Option("gpt-4o-mini", help="Model to use for chat"),
        api_key: Optional[str] = typer.Option(None, help="API key for authentication"),
        base_url: Optional[str] = typer.Option(None, help="Base URL for API requests"),
        organization: Optional[str] = typer.Option(None, help="Organization for API requests"),
        temperature: float = typer.Option(0.7, help="Temperature for response generation"),
        system_prompt: Optional[str] = typer.Option(None, help="System prompt to set context"),
        max_tokens: int = typer.Option(4096, help="Maximum number of tokens in the response"),
) -> None:
    
    console = Console()
    client = Completions(
        api_key=api_key,
        base_url=base_url,
        organization=organization,
    )

    messages = []

    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    while True:

        console.print(f"[dim]Model: {model}[/dim]\n")
        console.print(f"[dim]Temperature: {temperature}[/dim]\n")
        console.print(f"[dim]Max tokens: {max_tokens}[/dim]\n")

        user_input = console.input("[bold green]> [/bold green]")

        if user_input in ["exit", "quit", "q"]:
            break

        messages.append({"role": "user", "content": user_input})

        response = client.completion(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
            progress_bar=False
        )

        for chunk in response:
            console.print(chunk.choices[0].delta.content or "", end="", style="bold green")

        console.print()

        messages.append({"role": "assistant", "content": chunk.choices[0].delta.content or ""})


if __name__ == "__main__":
    typer.run(chat_app)