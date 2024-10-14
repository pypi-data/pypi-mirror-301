# XNANO

xnano is the lightweight implementation [zyx](https://zyx.hammad.fun) was meant to be. Documentation will be added soon.

## <code>install</code>

```bash
pip install xnano
```

or 

```bash
# for chromadb & litellm preinstalled
pip install 'xnano[all]'
```

## <code>basic usage</code>

```python
import xnano as x

# define a tool
def get_favorite_color() -> str:
    return "blue"


# automatic tool execution
x.completion(
    "what is my favorite color?",
    model = "gpt-4o-mini"          # all litellm models supported
    tools = [get_favorite_color]
)
```

### Easy LLM & Pydantic BaseModel Integration

```python
from xnano import BaseModel

class User(BaseModel):
    name: str
    age: int
    favorite_color: str

# This will generate 5 instances of the User class
User.generate(n=5)
```

**Generate Fields Sequentially (Chain-Of-Thought)**

```python
User.generate(
    model = "anthropic/claude-3.5",
    process = "sequential"            # defaults to 'batch'
)
```

**Optimized Schema Regeneration**

```python
user = User(
    name = "John Doe",
    age = 25,
    favorite_color = "blue"
)

user.patch(
    fields = ["name"],
    instructions = "The user's name has changed to John Smith"
)

# or user.regenerate() (not as strict)

# from xnano import patch can run the patch logic automatically from message threads.
```