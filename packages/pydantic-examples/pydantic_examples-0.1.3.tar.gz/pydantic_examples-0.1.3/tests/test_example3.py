from __future__ import annotations

from pydantic import BaseModel, Field

from pydantic_examples.yaml import yaml_with_comments


class LongDescriptionModel(BaseModel):
    """
    The root model has a very long description.

    It has multiple lines of all kinds of information, including
    all kinds of characters, like # ' " and /
    but also a hash mark
    # at the beginning of a line.
    """

    value: int = Field(
        default=1,
        description="""
                       Also, this field
                       has a very
                       long
                       description""",
    )


EXPECTED = """# The root model has a very long description.
#
# It has multiple lines of all kinds of information, including
# all kinds of characters, like # ' " and /
# but also a hash mark
# # at the beginning of a line.
value: 1  # Also, this field
# has a very
# long
# description
"""


def test_example3() -> None:
    rm = LongDescriptionModel()
    print("-------------")
    print(yaml_with_comments(rm))
    print("----------------")
    assert yaml_with_comments(rm) == EXPECTED, "Should produce expected value"
