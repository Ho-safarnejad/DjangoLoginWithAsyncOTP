def generate_list_schema_validator(object_schema):
    return {
        'count': {'type': 'integer', 'required': True},
        'next': {'type': 'string', "required": True, 'nullable': True},
        'previous': {'type': 'string', "required": True, 'nullable': True},
        'results': {'type': 'list', 'schema': {'type': 'dict', 'schema': object_schema}}
    }
