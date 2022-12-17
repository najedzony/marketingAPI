from src.constants.type_conversion import TYPE_CONVERSION_MAP
from src.exceptions.api_exceptions import (
    MissingMandatoryValueException,
    BadParameterType,
    BadParameterValue,
    BadParameter,
)


class Validator:
    def __init__(self):
        pass

    def validate_types(self, schema, request):
        for name, type, is_mandatory in schema:
            if name not in request and is_mandatory:
                raise MissingMandatoryValueException(
                    f"Missing mandatory parameter {name}."
                )
            value = request.get(name)
            if value:
                try:
                    converted = TYPE_CONVERSION_MAP[type](value)
                except Exception:
                    raise BadParameterType(
                        f"Bad type of parameter {name}. Expected {type}."
                    )

    def validate_values(self, fields_with_values, request):
        print(fields_with_values)
        for name, values in fields_with_values:
            request_value = request.get(name)
            if request_value and request_value not in values:
                raise BadParameterValue(
                    f"Bad parameter {name} value. Expected one of {values}, got {request_value}."
                )

    def validate_unique(self, unique_fields, request, table):
        for field in unique_fields:
            value = request.get(field)
            if value:
                kwargs = {field: value}
                exists = table.query.filter_by(**kwargs).first()
                if exists:
                    raise BadParameterValue(
                        f"{field} with value {value} already exists."
                    )

    def validate_names(self, parameters, request):
        for field in request:
            if field not in parameters:
                raise BadParameter(f"There's no such parameter as {field}")
