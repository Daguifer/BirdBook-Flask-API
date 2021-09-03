from flask import Flask, json, request, jsonify, Response
import pymysql
from pymysql.constants import CLIENT
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields


# ------------------------------------------------------------------------------

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/birdbook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


def getConexion():
    try:
        conexion = pymysql.connect(host='localhost',
                                   user='root',
                                   password='root',
                                   db='birdbook',
                                   client_flag=CLIENT.MULTI_STATEMENTS)

        # print('Conexión correcta')
        return conexion

    except (pymysql.err.OperationalError, pymysql.err.InternalError) as e:
        print('Error al conectar: ', e)

# **************************************************** MODELOS ****************************************************


class Usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45))
    email = db.Column(db.String(50))
    password = db.Column(db.String(45))

    def __init__(self, nombre, email, password):
        self.nombre = nombre
        self.email = email
        self.password = password


class Criadores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num_criador = db.Column(db.String(30))
    ubicacion = db.Column(db.String(100))
    telefono = db.Column(db.String(15))
    Usuarios_id = db.Column(db.Integer)

    def __init__(self, num_criador, ubicacion, telefono, Usuarios_id):
        self.num_criador = num_criador
        self.ubicacion = ubicacion
        self.telefono = telefono
        self.Usuarios_id = Usuarios_id


class Pajaros(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sexo = db.Column(db.String(1))
    fecha_nacimiento = db.Column(db.String(50))
    num_anilla = db.Column(db.String(10))
    procedencia = db.Column(db.String(45))
    raza = db.Column(db.Integer)
    Usuarios_id = db.Column(db.Integer)

    def __init__(self, sexo, fecha_nacimiento, num_anilla, procedencia, raza, Usuarios_id):
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.num_anilla = num_anilla
        self.procedencia = procedencia
        self.raza = raza
        self.Usuarios_id = Usuarios_id


class Razas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    variedad = db.Column(db.String(50))
    descripcion = db.Column(db.String(50))

    def __init__(self, variedad, descripcion):
        self.variedad = variedad
        self.descripcion = descripcion

# **************************************************** ESQUEMAS ****************************************************


class UsuariosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'password')


usuario_schema = UsuariosSchema()
usuarios_schema = UsuariosSchema(many=True)


class CriadoresSchema(ma.Schema):
    class Meta:
        fields = ('id', 'num_criador', 'ubicacion', 'telefono', 'Usuarios_id')


criador_schema = CriadoresSchema()
criadores_schema = CriadoresSchema(many=True)


class PajarosSchema(ma.Schema):
    class Meta:
        fields = ('id', 'sexo', 'fecha_nacimiento',
                  'num_anilla', 'procedencia', 'raza', 'Usuarios_id')


pajaro_schema = PajarosSchema()
pajaros_schema = PajarosSchema(many=True)


class RazasSchema(ma.Schema):
    class Meta:
        fields = ('id', 'variedad', 'descripcion')


raza_schema = RazasSchema()
razas_schema = RazasSchema(many=True)

# **************************************************** RUTAS ****************************************************

# ------------------------------------LOGIN------------------------------------


@app.route('/login', methods=['POST'])
def login():
    flag = "False"
    usuario = request.json['usuario']
    password = request.json['password']
    print(usuario)
    print(password)
    listado_usuarios = Usuarios.query.all()
    for row in listado_usuarios:
        if(row.nombre == usuario and row.password == password):
            flag = str(row.id)
            return flag
    return flag

# ------------------------------------USUARIOS------------------------------------


@app.route('/listarUsuarios', methods=['GET'])
def listarUsuarios():
    listado_usuarios = Usuarios.query.all()
    result = usuarios_schema.dump(listado_usuarios)
    return jsonify(result)


@app.route('/usuario/<int:id>')
def listarUsuarioPorID(id):
    usuario = Usuarios.query.get(id)
    result = usuario_schema.dump(usuario)
    return jsonify(result)


@app.route('/registroUsuario', methods=['POST'])
def registrarUsuario():
    usuario = request.json['usuario']
    password = request.json['password']
    email = request.json['email']
    resultado = "Error"
    conexion = getConexion()

    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuarios(nombre,email,password) VALUES (%s,%s,%s);"
            cursor.execute(consulta, (usuario, email, password))
            conexion.commit()
            resultado = "OK"
            return resultado
    finally:
        conexion.close()
        return resultado


# ------------------------------------CRIADORES------------------------------------

@app.route('/listarCriadores', methods=['GET'])
def listarCriadores():
    listado_criadores = Criadores.query.all()
    result = criadores_schema.dump(listado_criadores)
    return jsonify(result)


@app.route('/criador/<int:id>')
def listarCriadorPorID(id):
    criador = Criadores.query.get(id)
    result = criador_schema.dump(criador)
    return jsonify(result)


@app.route('/registroCriador', methods=['POST'])
def registrarCriador():
    usuario = request.json['usuario']
    password = request.json['password']
    email = request.json['email']
    ubicacion = request.json['ubicacion']
    telefono = request.json['telefono']
    numcriador = request.json['numcriador']

    print(usuario)
    print(password)
    print(email)
    print(ubicacion)
    print(telefono)
    print(numcriador)

    resultado = "Error"
    conexion = getConexion()

    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO usuarios(nombre,email,password) VALUES (%s,%s,%s);"
            cursor.execute(consulta, (usuario, email, password))

            conexion.commit()
    except:
        print("Error en el primer insert")

    try:
        conexion2 = getConexion()
        with conexion2.cursor() as cursor2:
            consulta1 = "SELECT max(id) FROM usuarios"
            cursor2.execute(consulta1)
            usuario_id = cursor2.fetchone()
            usuario_id = usuario_id[0]
            consulta2 = "INSERT INTO criadores(num_criador,ubicacion,telefono,Usuarios_id) VALUES (%s,%s,%s,%s)"
            cursor2.execute(
                consulta2, (numcriador, ubicacion, telefono, usuario_id))
            conexion2.commit()

        resultado = "OK"
        return resultado
    except Exception as e:
        print(e)

    conexion.close()
    conexion2.close()
    return resultado


# ------------------------------------PAJAROS------------------------------------


@app.route('/listarPajaros', methods=['GET'])
def listarPajaros():

    listado_pajaros = Pajaros.query.all()
    result = pajaros_schema.dump(listado_pajaros)
    # print(result)
    return jsonify(result)


@app.route('/pajaro/<int:id>')
def listarPajaroPorID(id):
    pajaro = Pajaros.query.get(id)
    result = pajaro_schema.dump(pajaro)
    return jsonify(result)

@app.route('/registroPajaro', methods=['POST'])
def registrarPajaro():
    sexo = request.json['sexo']
    raza = 56
    num_anilla = request.json['num_anilla']
    fecha_nac = request.json['fecha_nac']
    procedencia = request.json['procedencia']
    usuario_id = request.json['usuario_id']


    resultado = "Error"
    conexion = getConexion()

    try:
        with conexion.cursor() as cursor:
            consulta = "INSERT INTO pajaros(sexo,fecha_nacimiento,num_anilla, procedencia, raza, Usuarios_id) VALUES (%s,%s,%s,%s,%s,%s);"
            cursor.execute(consulta, (sexo, fecha_nac, num_anilla,procedencia,raza,usuario_id ))
            conexion.commit()
            resultado = "OK"
            return resultado
    finally:
        conexion.close()
        return resultado


@app.route('/borrarPajaro', methods=['POST'])
def borrarPajaro():
    id_pajaro = request.json['id_pajaro']
    print(id_pajaro)
    conexion = getConexion()
    try:
        with conexion.cursor() as cursor:
            consulta = "DELETE FROM pajaros WHERE id = %s;"
            cursor.execute(consulta, (id_pajaro))
            conexion.commit()
            resultado = "OK"
            return resultado
    except Exception as e:
            print (e)
    finally:
        conexion.close()
        return resultado

# ------------------------------------RAZAS------------------------------------


@app.route('/listarRazas', methods=['GET'])
def listarRazas():
    listado_razas = Razas.query.all()
    result = razas_schema.dump(listado_razas)
    return jsonify(result)


@app.route('/raza/<int:id>')
def listarRazaPorID(id):
    raza = Razas.query.get(id)
    result = raza_schema.dump(raza)
    return jsonify(result)


# **************************************************** RUN ****************************************************
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
