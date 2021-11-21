# App.py

from flask import Flask, render_template, request, redirect, url_for
from werkzeug.exceptions import abort
import sqlite3

###   FUNCIONES   ###
# Abrir conexión:
def get_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    return connection

# Selecionar POST:
def get_post(id):
    cn = get_connection()
    post = cn.execute('SELECT * FROM users WHERE id = ?', (id)).fetchone()
    cn.close()

    if post is None:
        abort(404)

    return post


# Trabajamos con los kilómetros:
def set_km(km):
    sug = 'Debes de Caminar más'
    if km < 0:
        km = 0
    elif km == 4:
        sug = 'Normal'
    elif km > 4:
        sug = 'Felicidades'

    return km, sug


# Init database:
cn = get_connection()
# Eliminamos la tabla:
cn.execute('DROP TABLE IF EXISTS users')
# Creamos la tabla:
cn.execute(
    '''
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT VARCHAR(50),
            mail TEXT VARCHAR(30),
            km NUMBER,
            suggest TEXT
        )
    ''')
# Añadimos datos iniciales:
km, sug = set_km(8)
cn.execute(' INSERT INTO users VALUES (NULL, ?, ?, ?, ?) ',
            ('Dario Antonio', 'dario@mail.com', km, sug))
km, sug = set_km(3)
cn.execute(' INSERT INTO users VALUES (NULL, ?, ?, ?, ?) ',
            ('Charlie Brown', 'Charlie@mail.org', km, sug))
km, sug = set_km(4)
cn.execute(' INSERT INTO users VALUES (NULL, ?, ?, ?, ?) ',
            ('Alex Markus', 'lex@mail.org', km, sug))
del(km, sug)
cn.commit()
cn.close()


#*****************************************************************************#

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


# usuarios:
@app.route('/users')
def users():
    connect = get_connection()
    cursor = connect.execute('SELECT * FROM users').fetchall()
    connect.close()
    return render_template('users.html', rows=cursor)


# Añadir un nuevo usuario:
@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        try:
            name = request.form["name"]
            email = request.form["mail"]
            km_week = int(request.form["km"])
            km, sug = set_km(km_week)

            connect = get_connection()
            connect.execute(' INSERT INTO users VALUES (NULL, ?, ?, ?, ?) ',
                                (name, email, km, sug) )
            connect.commit()
            connect.close()

            return redirect(url_for('home'))

        except BaseException as e:
            return render_template('result.html', error=e)


# Editar un usuario existente:
@app.route('/users/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    user = get_post(id)
    if request.method == 'POST':
        try:
            name = request.form["name"]
            email = request.form["mail"]
            km_week = int(request.form["km"])
            km, sug = set_km(km_week)

            connect = get_connection()
            connect.execute(' UPDATE users SET name=?, mail=?, km=?, suggest=? WHERE id=? ',
                            (name, email, km, sug, id) )
            connect.commit()
            connect.close()
        except BaseException as e:
            return render_template('result.html', error=e)
        return redirect(url_for('users'))
    return render_template('edit.html', post=user)


# Eliminamos un usuario:
@app.route('/users/delete/<id>')
def delete(id):
    try:
        connect = get_connection()
        connect.execute(' DELETE FROM users WHERE id=? ', [id] )
        connect.commit()
        connect.close()
    except BaseException as e:
        return render_template('result.html', error=e)
    return redirect(url_for('users'))



if __name__ == '__main__':
    app.run(debug=True)

#*****************************************************************************#