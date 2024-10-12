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
