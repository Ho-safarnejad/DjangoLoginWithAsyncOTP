otp_schema = {
    'id': {'type': 'integer', "required": True},
    'phone': {'type': 'string', "required": True},
    'code': {'type': 'integer', "required": True},
    'expiration': {'type': 'string', "required": True},
    'used': {'type': 'boolean', "required": True},
}
