from flask import jsonify
from models import Producto
from schemas import ProductoSchema

producto_schema = ProductoSchema()


def create_producto(request):
    print('ESTES ES EL REQUEST', request.json.keys())

    if request.headers.get('content-type') != 'application/json':
        return jsonify({'error': 'Solicitud debe estar en formato JSON.'}), 400

    required_keys = ['nombre', 'cantidad', 'precio']
    if not all(key in request.json for key in required_keys):
        return jsonify({'error': 'Solicitud debe contener nombre, cantidad y precio.'}), 400

    nombre = request.json['nombre']
    cantidad = request.json['cantidad']
    precio = request.json['precio']

    producto = Producto(nombre, cantidad, precio)
    producto.save()

    return jsonify(producto_schema.dump(producto))


def get_productos():
    productos = Producto.query.all()
    return jsonify(producto_schema.dump(productos, many=True))


def get_producto(id):
    producto = Producto.query.get(id)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado.'})
    else:
        return jsonify(producto_schema.dump(producto))


def update_producto(request, id):
    producto = Producto.query.get(id)

    nombre = request.json['nombre']
    cantidad = request.json['cantidad']
    precio = request.json['precio']

    producto.nombre = nombre
    producto.cantidad = cantidad
    producto.precio = precio
    producto.update()

    return jsonify(producto_schema.dump(producto))


def delete_producto(id):
    producto = Producto.query.get(id)
    print('este es productoo', producto)
    if producto is None:
        return jsonify({'message': 'Producto no encontrado.'})
    else:
        producto.delete()
        return jsonify({'message': 'Producto eliminado'})
