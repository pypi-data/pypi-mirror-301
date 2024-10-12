from io import StringIO
from typing import Any

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


def describe_onto(model_doc: CommentedMap, model: BaseModel):
    """Describe all fields of the CommentedMap using the model for metadata"""
    model_description = describe(model)
    if model_description:
        model_doc.yaml_set_start_comment(model_description)
    for field_name, field_info in model.model_fields.items():
        if field_name in model_doc:
            field_description = describe(field_info)
            if field_description:
                model_doc.yaml_add_eol_comment(field_description, key=field_name)

            # Recurse into list/dict types
            if hasattr(model, field_name):
                model_field = getattr(model, field_name)
                if model_field:
                    if type(model_field) is dict:
                        key, value = next(iter(model_field.items()))
                        if isinstance(value, BaseModel):
                            describe_onto(model_doc[field_name][key], value)
                            pass
                    elif type(model_field) is list:
                        value = model_field[0]
                        if isinstance(value, BaseModel):
                            describe_onto(model_doc[field_name][0], value)


def yaml_with_comments(model_instance: BaseModel) -> str:
    """Take the given Pydantic model and render a YAML file with comments"""
    # Serialize model
    yaml = YAML(typ="rt")
    model_dict = model_instance.model_dump()
    model_yaml_stream = StringIO()
    yaml.dump(model_dict, model_yaml_stream)
    model_yaml = model_yaml_stream.getvalue()

    model_doc: CommentedMap = yaml.load(model_yaml)
    assert isinstance(model_doc, CommentedMap), "Must be commented map for this to work"

    # Document model itself
    describe_onto(model_doc, model_instance)

    output = StringIO()
    yaml.dump(model_doc, output)
    return output.getvalue()
