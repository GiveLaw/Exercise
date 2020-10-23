# importamos Flask y algunas funciones/métodos:
from flask import Flask, render_template, request, redirect, url_for


import sqlite3
conn = sqlite3.connect('database.db')
conn.execute(
	'''
		CREATE TABLE IF NOT EXISTS users(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT VARCHAR(50),
			email TEXT VARCHAR(30) UNIQUE,
			km NUMBER,
			suggest TEXT)
	''')
conn.close()


app = Flask(__name__)


@app.route('/')
def home():
	return render_template('index.html')



@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
	if request.method == 'POST':
		try:
			nombre = request.form["name"]
			correo = request.form["mail"]
			km_week = int(request.form["km"])
			if km_week < 0:
				km_week = 0
			elif km_week < 4:
				sug = 'Debes de Caminar más'
			else:
				sug = 'Felicidades'

			with sqlite3.connect('database.db') as db:
				cursor = db.cursor()
				cursor.execute('''INSERT INTO users
									VALUES (NULL, ?, ?, ?, ?)''',
									(nombre, correo, km_week, sug))
				db.commit()
			return redirect(url_for('home'))
		except BaseException as e:
			db.rollback()
			return render_template('result.html', error=e)
		finally:
			db.close()



@app.route('/users')
def users():
	db = sqlite3.connect('database.db')
	db.row_factory = sqlite3.Row
	cs = db.cursor()
	cs.execute("SELECT * FROM users")
	rows = cs.fetchall()
	cs.close()
	db.close()
	return render_template('users.html', rows=rows)



@app.route('/users/edit/<id><name><email><km>', methods=['POST', 'GET'])
def edit(id, name, email, km):
	if request.method == 'GET':

		try:
			nombre = request.form["name"]
			correo = request.form["mail"]
			km_week = request.form["km"]
			with sqlite3.connect('database.db') as db:
				cursor = db.cursor()
				cursor.execute('''UPDATE users SET
								name=?, email=?, km=?
								WHERE id=?''',
								(nombre, correo, km_week, id))
				db.commit()
			return render_template('edit.html', name=name, mail=email, km=km)
		except BaseException as e:
			db.rollback()
			return render_template('result.html', error=e)
		finally:
			db.close()



# @app.route('/users/edit/<id>')
# def edit(id):
# 	try:
# 		db = sqlite3.connect('database.db')
# 		cs = db.cursor()
# 		cs.execute('UPDATE ')
# 		db.commit()
# 		db.close()
# 		return redirect(url_for('users'))
# 	except BaseException as e:
# 		db.rollback()
# 		return render_template('result.html', error=e)



@app.route('/users/delete/<id>')
def delete(id):
	try:
		db = sqlite3.connect('database.db')
		cs = db.cursor()
		cs.execute('DELETE FROM users WHERE id=?', [id])
		db.commit()
		db.close()
		return redirect(url_for('users'))
	except BaseException as e:
		return render_template('result.html', error=e)
	



if __name__ == '__main__':
	app.run(debug=True)
