from flask import Flask, render_template, url_for, redirect,request,session,g,flash
from werkzeug.security import check_password_hash, generate_password_hash
import mysql.connector

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY='ksfdsdkfj12321'
)

db = mysql.connector.connect(
    host = 'leaf12.mysql.pythonanywhere-services.com',
    user = 'leaf12',
    password = '70242526e',
    database = 'leaf12$default'
)

cursor = db.cursor(dictionary=True)

@app.route('/')
def index():
    receta = None
    user_id = session.get('usuario_id')
    cursor.execute(
        'select permisos from user where id = %s',(user_id,)
    )
    permisos = cursor.fetchone()
    cursor.execute(
        'select * from receta'
    )
    receta = cursor.fetchall()
    return render_template('index.html',permisos=permisos,receta=receta)


@app.route('/register',methods=['POST','GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        error = None
        cursor.execute(
            'select * from user where username = %s',(username,)
        )
        user = cursor.fetchone()
        if user is not None:
            error = 'Usuario existente'
        if error is None and username == 'Jesus':
            cursor.execute(
                'insert into user (username,password,nombre,permisos) values (%s,%s,%s,%s)',(username,generate_password_hash(password),nombre,1)
            )
            db.commit()
            return redirect(url_for('login'))
        elif error is None and username != 'Jesus':
            cursor.execute(
                'insert into user (username,password,nombre,permisos) values (%s,%s,%s,%s)',(username,generate_password_hash(password),nombre,0)
            )
            db.commit()
            return redirect(url_for('login'))
        flash(error)
    return render_template('usuario/register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        cursor.execute(
            'select * from user where username = %s',(username,)
        )
        user = cursor.fetchone()
        if username == user['username'] and check_password_hash(user['password'],password):
            session.clear()
            session['usuario_id'] = user['id']
            return redirect(url_for('index'))
        else:
            error = 'Usuario invalido'
            return redirect(url_for('login'))
        flash(error)
    return render_template('usuario/login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/create',methods=['POST','GET'])
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        url = request.form['url']
        categoria = request.form['categoria']
        descripcion = request.form['descripcion']
        ingredientes = request.form['ingredientes']
        preparacion = request.form['preparacion']
        cursor.execute(
            'insert into receta (titulo,descripcion,ingredientes,preparacion,categoria,url) values (%s,%s,%s,%s,%s,%s)',(titulo,descripcion,ingredientes,preparacion,categoria,url)
        )
        db.commit()
        return redirect(url_for('index'))
    return render_template('receta/create.html')

@app.route('/categorias')
def categorias():
    receta = None
    user_id = session.get('usuario_id')
    cursor.execute(
        'select permisos from user where id = %s',(user_id,)
    )
    permisos = cursor.fetchone()
    cursor.execute(
        'select * from receta'
    )
    receta = cursor.fetchall()
    return render_template('receta/categorias.html',permisos=permisos,receta=receta)

@app.route('/<categoria>/index_categorias')
def index_categorias(categoria):
    receta = None
    user_id = session.get('usuario_id')
    cursor.execute(
        'select permisos from user where id = %s',(user_id,)
    )
    permisos = cursor.fetchone()
    cursor.execute(
        'select * from receta where categoria = %s',(categoria,)
    )
    receta = cursor.fetchall()
    return render_template('receta/index_categorias.html',receta=receta,permisos=permisos)

@app.route('/recetas')
def recetas():
    user_id = session.get('usuario_id')
    cursor.execute(
        'select permisos from user where id = %s',(user_id,)
    )
    permisos = cursor.fetchone()
    cursor.execute(
        'select * from receta'
    )
    receta = cursor.fetchall()
    return render_template('receta/recetas.html',permisos=permisos,receta=receta)

@app.route('/<titulo>/index_receta')
def index_receta(titulo):
    receta = None
    user_id = session.get('usuario_id')
    cursor.execute(
        'select permisos from user where id = %s',(user_id,)
    )
    permisos = cursor.fetchone()
    cursor.execute(
        'select * from receta where titulo = %s',(titulo,)
    )
    receta = cursor.fetchone()
    return render_template('receta/index_receta.html',receta=receta,permisos=permisos)