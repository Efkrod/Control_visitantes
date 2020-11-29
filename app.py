from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'efkrod'
app.config['MYSQL_PASSWORD'] = 'Admin1234.'
app.config['MYSQL_DB'] = 'control_visitas'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def index():
	cnx = mysql.connection.cursor()
	cnx.execute('SELECT * FROM visitante')
	data = cnx.fetchall()
	return render_template('index.html',visitantes = data)


@app.route('/crearVisitante', methods=['POST'])
def crearVisitante():
	if request.method == 'POST':
		id=request.form['id']
		nombre=request.form['nombre']
		apellido=request.form['apellido']
		telefono=request.form['telefono']
		direccion=request.form['direccion']
		cnx = mysql.connection.cursor()
		cnx.execute('INSERT INTO visitante (id, nombre, apellido, telefono, direccion) VALUES (%s, %s, %s, %s, %s)',(id, nombre, apellido, telefono, direccion))
		mysql.connection.commit()
		flash('Visitante creado satisfactoriamente')
		return redirect(url_for('index'))


@app.route('/editarVisitante/<string:id>')
def editarVisitante(id):
	cnx = mysql.connection.cursor()
	cnx.execute('SELECT * FROM visitante WHERE id =%s',[id])
	data = cnx.fetchall()
	return render_template('editarV.html', visitantes=data[0])

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
		flash('Usuario actualizado exitomasente')
		return redirect(url_for('index'))


@app.route('/eliminarVisitante/<string:id>')
def eliminarVisitante(id):
	cnx = mysql.connection.cursor()
	cnx.execute('DELETE FROM visitante WHERE id = {0}'.format(id))
	mysql.connection.commit()
	flash('Visitante eliminado correctamente')
	return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()