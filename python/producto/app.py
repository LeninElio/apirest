from flask import Flask, request
from config import Config
from database import db
import controllers as cn

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


@app.route('/productos', methods=['POST'])
def create():
    return cn.create_producto(request)


@app.route('/productos', methods=['GET'])
def read_all():
    return cn.get_productos()


@app.route('/productos/<id>', methods=['GET'])
def read_one(id):
    return cn.get_producto(id)


@app.route('/productos/<id>', methods=['PUT'])
def update(id):
    return cn.update_producto(request, id)


@app.route('/productos/<id>', methods=['DELETE'])
def delete(id):
    return cn.delete_producto(id)


if __name__ == '__main__':
    app.run(debug=True)
