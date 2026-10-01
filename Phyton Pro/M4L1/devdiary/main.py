from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Conectando SQLite (nuestra base de datos local).
# El archivo diary.db se crea dentro de la carpeta "instance" del proyecto.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'

# Creación de la instancia de la base de datos
db = SQLAlchemy(app)


# ==========================================
# TICKET #1: MODELADO DE LA BASE DE DATOS
# ==========================================
# Esta clase es el "plano" de la tabla. Cada atributo será una COLUMNA.
# Necesitamos 4 columnas:
#   id       → número entero, es la llave primaria (identifica cada fila)
#   title    → texto corto, máximo 100 caracteres, obligatorio
#   subtitle → texto corto, máximo 300 caracteres, obligatorio
#   text     → texto largo, obligatorio
#
# Ejemplo de la primera columna:
#   id = db.Column(db.Integer, primary_key=True)
#
# Para las demás revisa en el README qué tipo de dato usar
# (db.String o db.Text) y cómo se marca que un campo es obligatorio.
#
# ⚠️ Si al ejecutar ves el error "could not assemble any primary key columns",
#    este ticket todavía no está terminado.
class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    subtitle = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)

    # Constructor (¡No tocar! Evita que tu editor marque errores falsos
    # al escribir Card(title=..., subtitle=..., text=...))
    def __init__(self, title, subtitle, text):
        self.title = title
        self.subtitle = subtitle
        self.text = text

    def __repr__(self):
        return f'<Card {self.id}>'


# ==========================================
# TICKET #2: CREAR LA BASE DE DATOS (observación)
# ==========================================
# Este bloque ya está escrito y se ejecuta solo cada vez que arrancas la app.
# create_all() lee tu clase Card y crea la tabla SI TODAVÍA NO EXISTE.
#
# Tu misión:
#   1. Ejecuta la app una vez.
#   2. Busca la carpeta "instance" y abre diary.db con SQLite Viewer.
#   3. Comprueba que la tabla "card" tiene las mismas 4 columnas de tu clase.
#
# Si no coinciden (o te sale "no such column"), es porque la tabla se creó
# antes de que terminaras el Ticket #1. create_all() NUNCA modifica una
# tabla que ya existe. Solución: pon RESET_DB = True, ejecuta UNA vez y
# vuelve a ponerlo en False (si no, borrarás tus entradas cada vez).
RESET_DB = False

with app.app_context():
    if RESET_DB:
        db.drop_all()   # borra todas las tablas
    db.create_all()     # crea las tablas que falten


# ==========================================
# TICKET #3: MOSTRAR TODAS LAS ENTRADAS
# ==========================================
@app.get('/')
def index():
    # TODO: Trae todas las tarjetas de la base de datos, de la más nueva a la
    # más antigua (orden descendente por id).
    # Pista: Card.query es la "puerta" a la tabla. Revisa en el README qué
    # métodos sirven para ordenar y para traer todos los resultados.
    cards = Card.query.order_by(Card.id.desc()).all()

    return render_template('index.html', cards=cards)


# ==========================================
# TICKET #4: MOSTRAR UNA ENTRADA ESPECÍFICA
# ==========================================
@app.get('/card/<int:id>')
def card(id):
    # TODO: Busca la tarjeta que tiene ese id.
    # Pista: usa db.get_or_404(). Necesita dos cosas: el MODELO (la clase)
    # y el id. Si la tarjeta no existe, muestra la página de error 404.
    card = Card.query.get_or_404(id)

    return render_template('card.html', card=card)


# ==========================================
# Formulario de nueva entrada
# ==========================================
# Misma dirección, dos funciones: una MUESTRA el formulario (GET)
# y la otra RECIBE los datos cuando se envía (POST).
@app.get('/create')
def create():
    return render_template('create_card.html')


# ==========================================
# TICKET #5: GUARDAR DATOS EN LA DB (POST)
# ==========================================
@app.post('/create')
def create_post():
    # Capturamos los datos del formulario HTML
    title = request.form['title']
    subtitle = request.form['subtitle']
    text = request.form['text']

    # TODO 1: Crea un objeto Card con los datos capturados.
    nueva_tarjeta = Card(title=title, subtitle=subtitle, text=text)

    # TODO 2: Añade la tarjeta a la sesión de la base de datos.
    # Pista: db.session.add(...)
    db.session.add(nueva_tarjeta)

    # TODO 3: La sesión es como un "borrador": nada se guarda de verdad hasta
    # que lo confirmas. ¿Qué método de db.session lo hace? (Mira el README)
    db.session.commit()

    # Después de guardar, volvemos a la página principal
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
