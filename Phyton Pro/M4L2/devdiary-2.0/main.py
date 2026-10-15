from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# La session recuerda quién inició sesión: guarda sus datos en una cookie del
# navegador, firmada con esta clave. (En una app real la clave va en una variable
# de entorno, nunca escrita en el código.)
app.secret_key = 'mi_clave_secreta_super_segura'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
db = SQLAlchemy(app)


# ==========================================
# Tabla de la semana pasada (ya está lista)
# ==========================================
# Novedad: la columna user_email dice A QUIÉN pertenece cada tarjeta.
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    user_email = db.Column(db.String(100), nullable=False)

    def __init__(self, title, subtitle, text, user_email):
        self.title = title
        self.subtitle = subtitle
        self.text = text
        self.user_email = user_email

    def __repr__(self):
        return f'<Card {self.id}>'


# ==========================================
# TICKET #1 (parte A): LA TABLA DE USUARIOS
# ==========================================
# Una tabla gira en torno a una clase. Esta guardará a las personas que usen la app.
# ¿Qué columnas hacen falta para saber QUIÉN es alguien y comprobar que es esa persona?
class User(db.Model):
    # TODO: Declara las 3 columnas:
    #   id       → Integer, llave primaria
    #   email    → String(100), obligatorio y ÚNICO (no se puede repetir)
    #   password → String(255), obligatorio
    #
    # Ejemplo (la primera columna):
    #   id = db.Column(db.Integer, primary_key=True)
    #
    # Para email y password mira la chuleta del README (nullable=False, unique=True).
    # ¿Por qué password es String(255) y no String(100)? Lo descubrirás en el TICKET #3.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

    # Constructor (¡No tocar!)
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def __repr__(self):
        return f'<User {self.email}>'


# ==========================================
# TICKET #1 (parte B): ACTUALIZAR LA BASE DE DATOS
# ==========================================
# La base de datos de la semana pasada ya tiene la tabla Card SIN user_email, y
# create_all() NUNCA modifica una tabla que ya existe. Hay que reiniciarla:
#
#   1. Cuando termines la clase User, pon RESET_DB = True
#   2. Ejecuta la app UNA sola vez (verás un aviso ⚠️ en la terminal)
#   3. Vuelve a poner RESET_DB = False
#
# Si lo dejas en True, se borra TODO (usuarios y entradas) cada vez que guardas.
RESET_DB = False

with app.app_context():
    if RESET_DB:
        db.drop_all()
        print('⚠️  RESET_DB está en True: base de datos reiniciada. ¡Vuelve a ponerlo en False!')
    db.create_all()


# ==========================================
# El guardia (ya está listo, ¡no tocar!)
# ==========================================
# Se ejecuta ANTES de cada petición. Si la persona no inició sesión y quiere entrar
# a una página privada, la manda al login. Solo estas rutas son públicas:
@app.before_request
def guardia():
    publicas = ('login', 'login_post', 'reg', 'reg_post', 'static')
    if request.endpoint not in publicas and 'email' not in session:
        return redirect(url_for('login'))


# ==========================================
# El diario
# ==========================================
@app.get('/')
def index():
    # TICKET #4 (parte B): CADA QUIEN VE SOLO SU DIARIO
    # Ahora mismo se traen las tarjetas de TODAS las personas.
    # Cambia la consulta para traer solo las de quien inició sesión.
    # Pista: añade .filter_by(user_email=...) antes de .order_by(...)
    #        El correo de quien inició sesión está en session['email'].
    cards = Card.query.filter_by(user_email=session['email']).order_by(Card.id.desc()).all()

    return render_template('index.html', cards=cards)


@app.get('/card/<int:id>')
def card(id):
    card = db.get_or_404(Card, id)

    # (Ya está hecho) Sin esto, cualquiera podría leer la tarjeta de otra persona
    # escribiendo /card/1 en la barra de direcciones. Pruébalo con dos cuentas.
    if card.user_email != session['email']:
        abort(404)

    return render_template('card.html', card=card)


@app.get('/create')
def create():
    return render_template('create_card.html')


@app.post('/create')
def create_post():
    title = request.form['title']
    subtitle = request.form['subtitle']
    text = request.form['text']

    # (Ya está hecho) ¿De dónde sale el correo? De la session que llenarás en el TICKET #4.
    nueva_tarjeta = Card(title=title, subtitle=subtitle, text=text, user_email=session['email'])
    db.session.add(nueva_tarjeta)
    db.session.commit()

    return redirect(url_for('index'))


# ==========================================
# Registro
# ==========================================
@app.get('/reg')
def reg():
    return render_template('registration.html')


# ==========================================
# TICKET #3: GUARDAR AL USUARIO (REGISTRO)
# ==========================================
@app.post('/reg')
def reg_post():
    # .strip().lower() quita espacios y pasa a minúsculas: Ana@x.com y ana@x.com son la misma persona
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # (Ya está hecho) Si el correo ya existe, avisamos y no creamos nada
    if User.query.filter_by(email=email).first():
        return render_template('registration.html', error='Ese correo ya está registrado')

    # TODO: Igual que con las tarjetas de la semana pasada, son 3 pasos:
    #   1. Crear el objeto User(email=..., password=...)
    #   2. Añadirlo a la sesión de la base de datos  (add)
    #   3. Confirmar los cambios                     (commit)
    #
    # ⚠️ La contraseña NO se guarda tal cual la escribió la persona: se guarda CIFRADA.
    #    Usa  password=generate_password_hash(password)
    # Cuando termines, registra un usuario, abre diary.db con SQLite Viewer
    # y mira la columna password. ¿Se puede leer?
    user = User(email=email, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login', registered=1))


# ==========================================
# Login
# ==========================================
@app.get('/login')
def login():
    return render_template('login.html', registered=request.args.get('registered'))


# ==========================================
# TICKET #4 (parte A): INICIAR SESIÓN
# ==========================================
@app.post('/login')
def login_post():
    email = request.form.get('email', '').strip().lower()
    password = request.form.get('password', '')

    # TODO 1: Busca en la tabla User a la persona con ese correo.
    # Pista: User.query.filter_by(email=email).first()
    #        .first() devuelve UN usuario, o None si no existe.
    user = User.query.filter_by(email=email).first()
    # TODO 2: Si el usuario existe Y la contraseña es correcta:
    #   - recuerda quién es:  session['email'] = ...
    #   - mándalo al diario:  return redirect(url_for(...))
    # Para comparar contraseñas: check_password_hash(user.password, password)
    # Pregunta: ¿por qué hay que comprobar PRIMERO que user exista?
    # Escribe aquí tu if:
    if user and check_password_hash(user.password, password):
        session['email'] = user.email
        return redirect(url_for('index'))
    # Si el código llega hasta aquí, el login falló.
    # (No decimos si falló el correo o la contraseña: así no ayudamos a quien intente adivinar.)
    error = 'Correo o contraseña incorrectos'
    return render_template('login.html', error=error)


@app.get('/logout')
def logout():
    session.pop('email', None)  # olvidar a la persona
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)
