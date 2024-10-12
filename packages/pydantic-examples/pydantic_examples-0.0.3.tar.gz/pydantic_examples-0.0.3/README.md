# pydantic-examples

Project to create example data from [Pydantic](https://docs.pydantic.dev/latest/) models.

From a model like:
```python
from pydantic import BaseModel, Field
from pydantic_examples import yaml_with_comments
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
