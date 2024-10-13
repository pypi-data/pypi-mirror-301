from enum import Enum


class NodeType(Enum):
    CLASS_DECLARATION = "class_declaration"
    FIELD_DEFINITION = "field_definition"
    METHOD_DEFINITION = "method_definition"
    PROPERTY_IDENTIFIER = "property_identifier"
    FUNCTION_DECLARATION = "function_declaration"
    PRIVATE_PROPERTY_IDENTIFIER = "private_property_identifier"
    IDENTIFIER = "identifier"


class FieldNames(Enum):
    BODY = "body"
    NAME = "name"
    PROPERTY = "property"
    PARAMETERS = "parameters"
    FORMAL_PARAMETERS = "formal_parameters"
