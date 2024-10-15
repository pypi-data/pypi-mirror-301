# pydantic-examples

Project to create examples of serialized [Pydantic](https://docs.pydantic.dev/latest/) models with comments.

Intended to easily generate example config files if you load and validate the configuration using Pydantic.

From a model like:
```python
from pydantic import BaseModel, Field
from pydantic_examples.yaml import yaml_with_comments
from typing import Annotated

class Example(BaseModel):
        """Example model"""

        value: Annotated[str, Field(description="Does not really matter")] = "foo"
```

You can generate
```yaml
# Example model
value: foo  # Does not really matter
```

Status
======
This project was created with a single use-case in mind (yaml from Pydantic) but is open to PRs and collaboration on Github.

Feel free to file issues, raise PRs and join in if you want.
