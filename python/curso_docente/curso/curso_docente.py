from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from flask import request, jsonify

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/bdpythonapi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Profesor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    cursos = relationship("Curso", backref="profesor", lazy=True)


class Curso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    profesor_id = db.Column(db.Integer, ForeignKey('profesor.id'), nullable=False)


with app.app_context():
    db.create_all()


# Obtener todos los profesores
@app.route('/profesores', methods=['GET'])
def obtener_profesores():
    profesores = Profesor.query.all()
    resultados = []
    for profesor in profesores:
        resultados.append({
            'id': profesor.id,
            'nombre': profesor.nombre
        })
    return jsonify(resultados)


# Obtener un profesor por su id
@app.route('/profesor/<id>', methods=['GET'])
def obtener_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({'mensaje': 'Profesor no encontrado'})
    resultado = {
        'id': profesor.id,
        'nombre': profesor.nombre
    }
    return jsonify(resultado)


# Crear un nuevo profesor
@app.route('/profesor', methods=['POST'])
def crear_profesor():
    nombre = request.json['nombre']
    profesor = Profesor(nombre=nombre)
    db.session.add(profesor)
    db.session.commit()
    return jsonify({'mensaje': 'Profesor creado exitosamente'})


# Actualizar un profesor existente
@app.route('/profesor/<id>', methods=['PUT'])
def actualizar_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({'mensaje': 'Profesor no encontrado'})
    nombre = request.json['nombre']
    profesor.nombre = nombre
    db.session.commit()
    return jsonify({'mensaje': 'Profesor actualizado exitosamente'})


# Eliminar un profesor existente
@app.route('/profesor/<id>', methods=['DELETE'])
def eliminar_profesor(id):
    profesor = Profesor.query.get(id)
    if not profesor:
        return jsonify({'mensaje': 'Profesor no encontrado'})
    db.session.delete(profesor)
    db.session.commit()
    return jsonify({'mensaje': 'Profesor eliminado exitosamente'})


# Obtener todos los cursos
@app.route('/cursos', methods=['GET'])
def obtener_cursos():
    cursos = Curso.query.all()
    resultados = []
    for curso in cursos:
        resultados.append({
            'id': curso.id,
            'nombre': curso.nombre,
            'profesor': curso.profesor.nombre
        })
    return jsonify(resultados)


# Obtener un curso por su id
@app.route('/curso/<id>', methods=['GET'])
def obtener_curso(id):
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'mensaje': 'Curso no encontrado'})
    resultado = {
        'id': curso.id,
        'nombre': curso.nombre,
        'profesor': curso.profesor.nombre
    }
    return jsonify(resultado)


# Crear un nuevo curso
@app.route('/curso', methods=['POST'])
def crear_curso():
    nombre = request.json['nombre']
    profesor_id = request.json['profesor_id']
    profesor = Profesor.query.get(profesor_id)
    if not profesor:
        return jsonify({'mensaje': 'Profesor no encontrado'})
    curso = Curso(nombre=nombre, profesor=profesor)
    db.session.add(curso)
    db.session.commit()
    return jsonify({'mensaje': 'Curso creado exitosamente'})


# Actualizar un curso existente
@app.route('/curso/<id>', methods=['PUT'])
def actualizar_curso(id):
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'mensaje': 'Curso no encontrado'})

    nombre = request.json['nombre']
    profesor_id = request.json['profesor_id']
    profesor = Profesor.query.get(profesor_id)
    if not profesor:
        return jsonify({'mensaje': 'Profesor no encontrado'})
    curso.nombre = nombre
    curso.profesor = profesor
    db.session.commit()
    return jsonify({'mensaje': 'Curso actualizado exitosamente'})


@app.route('/curso/<id>', methods=['DELETE'])
def eliminar_curso(id):
    curso = Curso.query.get(id)
    if not curso:
        return jsonify({'mensaje': 'Curso no encontrado'})
    db.session.delete(curso)
    db.session.commit()
    return jsonify({'mensaje': 'Curso eliminado exitosamente'})


if __name__ == '__main__':
    app.run(debug=True)
