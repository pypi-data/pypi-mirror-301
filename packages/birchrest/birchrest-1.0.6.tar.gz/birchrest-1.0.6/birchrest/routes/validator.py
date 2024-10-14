from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Type, get_args, get_origin
import re


def parse_data_class(data_class: Type[Any], data: Any) -> Any:
    """
    Parses and validates data against a dataclass, ensuring the data matches the
    field types, validation constraints (like min/max lengths, regex), and metadata
    such as default values. This function supports nested dataclasses and collections.

    The function checks if the provided data conforms to the field types and optional
    constraints specified in the dataclass. If the data is invalid, a `ValueError`
    is raised with a descriptive message.

    Supported validations include:
        - Type validation (e.g., int, str, float, etc.)
        - String constraints: min_length, max_length, regex pattern.
        - Numeric constraints: min_value, max_value.
        - List constraints: min_items, max_items, uniqueness of items.

    :param data_class: The dataclass type to validate against.
    :param data: The input data to be validated, typically a dictionary.
    :return: An instance of the dataclass with the validated data.
    :raises ValueError: If the data is missing required fields or if any validation fails.
    """

    if not is_dataclass(data_class):
        raise ValueError(f"{data_class} must be a dataclass")

    kwargs = {}
    for field in fields(data_class):
        field_name = field.name
        field_type = field.type
        field_metadata = field.metadata

        if field_name not in data:
            if field.default is not MISSING:
                kwargs[field_name] = field.default
            elif field.default_factory is not MISSING:
                kwargs[field_name] = field.default_factory()
            else:
                raise ValueError(f"Missing required field: {field_name}")
        else:
            field_value = data[field_name]

            if field_type is int:
                try:
                    field_value = int(field_value)
                except ValueError as e:
                    raise ValueError(f"Field '{field_name}' must be a valid integer.") from e

            if isinstance(field_value, str):
                min_length = field_metadata.get("min_length", None)
                max_length = field_metadata.get("max_length", None)
                regex = field_metadata.get("regex", None)

                if min_length is not None and len(field_value) < min_length:
                    raise ValueError(
                        f"Field '{field_name}' must have at least {min_length} characters."
                    )
                if max_length is not None and len(field_value) > max_length:
                    raise ValueError(
                        f"Field '{field_name}' must have at most {max_length} characters."
                    )
                if regex and not re.match(regex, field_value):
                    raise ValueError(f"Field '{field_name}' was malformed")

            if isinstance(field_value, (int, float)):
                min_value = field_metadata.get("min_value", None)
                max_value = field_metadata.get("max_value", None)

                if min_value is not None and field_value < min_value:
                    raise ValueError(
                        f"Field '{field_name}' must be at least {min_value}."
                    )
                if max_value is not None and field_value > max_value:
                    raise ValueError(
                        f"Field '{field_name}' must be at most {max_value}."
                    )

            if get_origin(field_type) is list:
                item_type = get_args(field_type)[0]

                min_items = field_metadata.get("min_items", None)
                max_items = field_metadata.get("max_items", None)
                unique = field_metadata.get("unique", False)

                if min_items is not None and len(field_value) < min_items:
                    raise ValueError(
                        f"Field '{field_name}' must have at least {min_items} items."
                    )
                if max_items is not None and len(field_value) > max_items:
                    raise ValueError(
                        f"Field '{field_name}' must have at most {max_items} items."
                    )
                if unique and len(field_value) != len(set(field_value)):
                    raise ValueError(f"Field '{field_name}' must contain unique items.")

                for item in field_value:
                    if not isinstance(item, item_type):
                        raise ValueError(
                            f"All items in field '{field_name}' must be of type {item_type}."
                        )

            if is_dataclass(field_type) and isinstance(field_value, dict):
                kwargs[field_name] = parse_data_class(field_type, field_value)
            else:
                origin_type = get_origin(field_type)
                if origin_type is not None:
                    if not isinstance(field_value, origin_type):
                        raise ValueError(
                            f"Incorrect type for field '{field_name}', expected {origin_type.__name__}"
                        )
                else:
                    if not isinstance(field_value, field_type):
                        raise ValueError(
                            f"Incorrect type for field '{field_name}', expected {field_type.__name__}"
                        )

                kwargs[field_name] = field_value

    return data_class(**kwargs)
