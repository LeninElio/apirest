from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
# app.secret_key = "hello"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


# creacion de la tabla categoria
class Categoria(db.Model):
    cat_id = db.Column(db.Integer, primary_key=True)
    cat_nom = db.Column(db.String(100))
    cat_desc = db.Column(db.String(100))

    def __init__(self, cat_nom, cat_desc):
        self.cat_nom = cat_nom
        self.cat_desc = cat_desc


with app.app_context():
    db.create_all()


# marshmellow sirve para definir esquemas
# esquema categoria
class CategoriaSchema(ma.Schema):
    class Meta:
        fields = ('cat_id', 'cat_nom', 'cat_desc')


# una sola respuesta
categoria_schema = CategoriaSchema()


# muchas respuestas
categorias_schema = CategoriaSchema(many=True)


# GET
@app.route('/categoria', methods=['GET'])
def get_categorias():
    all_categorias = Categoria.query.all()
    result = categorias_schema.dump(all_categorias)
    return jsonify(result)


# GET por id
@app.route('/categoria/<id>', methods=['GET'])
def get_categoria(id):
    una_categoria = Categoria.query.get(id)
    return categoria_schema.jsonify(una_categoria)


# POST
@app.route('/categoria', methods=['POST'])
def insert_categoria():
    cat_nom = request.json['cat_nom']
    cat_desc = request.json['cat_desc']
    nuevo_registro = Categoria(cat_nom, cat_desc)
    db.session.add(nuevo_registro)
    db.session.commit()
    return categoria_schema.jsonify(nuevo_registro)


# PUT
@app.route('/categoria/<id>', methods=['PUT'])
def update_categoria(id):
    actualizar_categoria = Categoria.query.get(id)
    cat_nom = request.json['cat_nom']
    cat_desc = request.json['cat_desc']

    actualizar_categoria.cat_nom = cat_nom
    actualizar_categoria.cat_desc = cat_desc

    db.session.commit()
    return categoria_schema.jsonify(actualizar_categoria)


# DELETE
@app.route('/categoria/<id>', methods=['DELETE'])
def delete_categoria(id):
    eliminar_categoria = Categoria.query.get(id)
    db.session.delete(eliminar_categoria)
    db.session.commit()

    return categoria_schema.jsonify(eliminar_categoria)


# mensaje de bienvenida
@app.route('/', methods=['GET'])
def index():
    return jsonify({'mensaje': 'Bienvenido al ejemplo de APIREST con Python'})


if __name__ == "__main__":
    app.run(debug=True)
