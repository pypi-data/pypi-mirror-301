from io import StringIO
from typing import Any, Type

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap


def describe(obj: Any) -> str:
    if isinstance(obj, FieldInfo):
        return obj.description or ""
    if hasattr(obj, "__doc__") and obj.__doc__:
        return obj.__doc__ or ""
    return ""


def describe_onto(model_doc: CommentedMap, Model: Type[BaseModel]):
    """Describe all fields of the commented map and possibly continue down the fields"""
    model_doc.yaml_set_start_comment(describe(Model))
    for field_name, field_info in Model.model_fields.items():
        field = model_doc[field_name]
        if isinstance(field, CommentedMap):
            describe_onto(field, field_info.annotation)
        else:
            model_doc.yaml_add_eol_comment(describe(field_info), key=field_name)


def yaml_with_comments(model_instance: BaseModel) -> str:
    # Serialize model
    yaml = YAML(typ="rt")
    model_dict = model_instance.model_dump()
    model_yaml_stream = StringIO()
    yaml.dump(model_dict, model_yaml_stream)
    model_yaml = model_yaml_stream.getvalue()

    model_doc: CommentedMap = yaml.load(model_yaml)
    assert isinstance(model_doc, CommentedMap), "Must be commented map for this to work"

    # Document model itself
    describe_onto(model_doc, type(model_instance))

    output = StringIO()
    yaml.dump(model_doc, output)
    return output.getvalue()
