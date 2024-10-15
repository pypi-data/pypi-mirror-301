from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field

from pydantic_examples.yaml import yaml_with_comments

Uniq = AfterValidator(lambda v: list(sorted(set(v))))


class SecondLevel(BaseModel, extra="forbid"):
    """Second level here"""

    value: Annotated[int, Field(description="actual value")] = 0


class FirstLevel(BaseModel, extra="forbid"):
    """Nested documentation is also documentation"""

    fst: Annotated[SecondLevel, Field(description="fst level")] = SecondLevel()


class RootModel(BaseModel):
    """Root docstring"""

    root_fst: FirstLevel = FirstLevel()
    root_fst_list: list[FirstLevel] = [FirstLevel()]
    root_fst_dict: dict[str, FirstLevel] = {"a": FirstLevel()}


EXPECTED = """# Root docstring
root_fst:
# Nested documentation is also documentation
  fst:  # fst level
    value: 0  # actual value
root_fst_list:
# Nested documentation is also documentation
- fst:  # fst level
    value: 0  # actual value
root_fst_dict:
  a:
# Nested documentation is also documentation
    fst:  # fst level
      value: 0  # actual value
"""


def test_example2() -> None:
    rm = RootModel()
    assert yaml_with_comments(rm) == EXPECTED, "Should produce expected value"
