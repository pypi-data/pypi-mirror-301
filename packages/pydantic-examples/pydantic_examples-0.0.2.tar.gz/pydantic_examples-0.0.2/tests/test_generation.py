from typing import Annotated

from pydantic import BaseModel, Field

from pydantic_examples import yaml_with_comments


def test_should_include_docstring() -> None:
    class Example(BaseModel):
        """Example model"""

        value: Annotated[str, Field(description="Does not really matter")] = "foo"

    a = yaml_with_comments(Example())
    assert (
        a
        == """# Example model
value: foo  # Does not really matter
"""
    )

def test_should_work_with_nesting() -> None:
    class Nested(BaseModel):
        """Nested type"""
        value: Annotated[str, Field(description="Nested value")] = "also foo"
    
    class Example(BaseModel):
        """Example model"""

        normal: Annotated[str, Field(description="Does not really matter")] = "foo"
        nested_value: Nested = Nested()

    a = yaml_with_comments(Example())
    assert (
        a
        == """# Example model
normal: foo  # Does not really matter
nested_value:
# Nested type
  value: also foo  # Nested value
"""
    )