from typing import Annotated

from pydantic import BaseModel, Field

from pydantic_examples import yaml_with_comments


class Nested(BaseModel):
    """Nested documentation is also documentation"""

    value: Annotated[int, Field(description="nested_interger value")] = 0


class Banana(BaseModel):
    """Documentation on the base model"""

    field_a: Annotated[str, Field(description="field_a description")] = ""
    field_b: int = 0
    field_c: float = 1.0
    field_d: bool = True
    field_e: Annotated[list[str], Field(description="list field")] = []
    field_f: dict = {}
    field_g: Annotated[dict[str, Nested], Field(description="nested field")] = {
        "a": Nested()
    }
    field_h: Annotated[list[Nested], Field(description="list of nested")] = [
        Nested(),
        Nested(),
    ]


EXPECTED = """# Documentation on the base model
field_a: ''  # field_a description
field_b: 0
field_c: 1.0
field_d: true
field_e: [] # list field
field_f: {}
field_g: # nested field
  a:
# Nested documentation is also documentation
    value: 0  # nested_interger value
field_h: # list of nested
# Nested documentation is also documentation
- value: 0  # nested_interger value
- value: 0
"""


def test_example1() -> None:
    bended = Banana()
    assert yaml_with_comments(bended) == EXPECTED, "Should produce expected value"
