from flask_login import LoginManager,login_user,logout_user,login_required,current_user
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

#Conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'efkrod'
app.config['MYSQL_PASSWORD'] = 'Admin1234.'
app.config['MYSQL_DB'] = 'control_visitas'
mysql = MySQL(app)

#Clave secreta para cifrado para el objeto session
app.secret_key = 'arquitectura'

#Ruta inicial para inicio de sesion 
#realiza una sentencia de Select para buscar el id y password de usuario
#e inicia sesion 
@app.route('/', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'id' in request.form and 'password' in request.form:
        id = request.form['id']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM cuenta WHERE id = %s AND password = %s', (id, password,))
        cuenta = cursor.fetchone()
        if cuenta:
            session['loggedin'] = True
            session['id'] = cuenta['id']
            session['nombre'] = cuenta['nombre']
            return render_template('index.html')
        else:
            msg = 'Id o contraseña incorrecta!'
    return render_template('login.html', msg=msg)

#Ruta que devuelve todos los datos almacenados en la tabla visitante
#RDevuelve la pagina index.html donde esta el formulario de creacion de usuario
@app.route('/index')
def index():
	cnx = mysql.connection.cursor()
	cnx.execute('SELECT * FROM visitante')
	data = cnx.fetchall()
	return render_template('index.html',visitantes = data)

#Ruta que realiza una insercion a la tabla visitante
#Devuelve la pagina index.html
@app.route('/crearVisitante', methods=['POST', 'GET'])
def crearVisitante():
	if request.method == 'POST':
		id=request.form['id']
		nombre=request.form['nombre']
		apellido=request.form['apellido']
		telefono=request.form['telefono']
		direccion=request.form['direccion']
		cnx = mysql.connection.cursor()
		cnx.execute("""INSERT INTO visitante 
						(id, nombre, apellido, telefono, direccion) 
					VALUES (%s, %s, %s, %s, %s)
					""",(id, nombre, apellido, telefono, direccion))
		mysql.connection.commit()
		flash('Visitante creado satisfactoriamente')
		return redirect(url_for('index'))

#Ruta que permite editar un registro de la tabla visitante
#Recibe el id de un visitante
#Devuelve la pagina editarV.html
@app.route('/editarVisitante/<string:id>')
def editarVisitante(id):
	cnx = mysql.connection.cursor()
	cnx.execute('SELECT * FROM visitante WHERE id =%s',[id])
	data = cnx.fetchall()
	return render_template('editarV.html', visitantes=data[0])

#Ruta que realiza un update en la tabla visitante
#recibe el id del visitante
@app.route('/actualizar/<string:id>', methods = ['POST'])
def actualizar(id):
	if request.method == 'POST':
		nombre=request.form['nombre']
		apellido=request.form['apellido']
		telefono=request.form['telefono']
		direccion=request.form['direccion']
		cnx = mysql.connection.cursor()
		cnx.execute("""
			UPDATE visitante
			SET nombre = %s,
				apellido = %s,
				telefono = %s,
				direccion= %s
			WHERE id = %s
			""",(nombre, apellido, telefono, direccion, id))
		mysql.connection.commit()
		return redirect(url_for('index'))

#Ruta que elimina un registro de la tabla visitante
#Recibe un id y delvuelve la pagina index
@app.route('/eliminarVisitante/<string:id>', methods = ['GET'])
def eliminarVisitante(id):
	cnx = mysql.connection.cursor()
	cnx.execute('DELETE FROM visitante WHERE id = {0}'.format(id))
	mysql.connection.commit()
	return redirect(url_for('index'))

#Ruta que genera un permiso para un visitante
#Recibe un id y devuelve la pagina permiso.html
@app.route('/permisoIngreso/<string:id>')
def permisoIngreso(id):
	cnx = mysql.connection.cursor()
	cnx.execute('SELECT nombre FROM visitante WHERE id =%s',[id])
	data = cnx.fetchall()
	return render_template('permiso.html', visitantes = data[0])

#Ruta que muestra una tabla con todos los registros de la tabla visitante
#Devuelve un archivo html 
@app.route('/listaVisitantes', methods=['GET'])
def listaVisitantes():
	cnx = mysql.connection.cursor()
	cnx.execute('SELECT * FROM visitante')
	data = cnx.fetchall()
	return render_template('listaU.html',visitantes = data)

if __name__ == '__main__':
    app.run(host='0.0.0.0')