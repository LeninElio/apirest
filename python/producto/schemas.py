from marshmallow import Schema, fields


class ProductoSchema(Schema):
    id = fields.Integer(dump_only=True)
    nombre = fields.String(required=True)
    cantidad = fields.Integer(required=True)
    precio = fields.Float(required=True)
