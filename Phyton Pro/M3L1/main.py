import random
from flask import Flask

app = Flask(__name__)

coin = ["head/cara","tails/sello"]

facts_list = [
    "La mayoría de las personas que sufren adicción tecnológica experimentan un fuerte estrés cuando se encuentran fuera del área de cobertura de la red o no pueden utilizar sus dispositivos.",
    "Según un estudio realizado en 2018, más del 50% de las personas de entre 18 y 34 años se consideran dependientes de sus smartphones.",

    "El estudio de la dependencia tecnológica es una de las áreas más relevantes de la investigación científica moderna",
    "Según un estudio de 2019, más del 60% de las personas responden a mensajes de trabajo en sus smartphones en los 15 minutos siguientes a salir del trabajo",

    "Una forma de combatir la dependencia tecnológica es buscar actividades que aporten placer y mejoren el estado de ánimo",

    "Elon Musk afirma que las redes sociales están diseñadas para mantenernos dentro de la plataforma, para que pasemos el mayor tiempo posible viendo contenidos",
    "Elon Musk aboga por la regulación de las redes sociales y la protección de los datos personales de los usuarios. Afirma que las redes sociales recopilan una enorme cantidad de información sobre nosotros, que luego puede utilizarse para manipular nuestros pensamientos y comportamientos",

    "Las redes sociales tienen aspectos positivos y negativos, y debemos ser conscientes de ambos cuando utilicemos estas plataformas"
                ]

@app.route("/")
def hello_world():
    return '<h1>Hello, World!</h1>' \
    '<a href="/random-facts">¡Ver un dato aleatorio!</a>\n'\
    '<a href="/flip-coin">¡Lanzar una moneda!</a>'\
    '<a href="/gen-pass">¡Generar una contraseña!</a>'

@app.route('/random-facts')
def rand_facts():
    return f'<p>{random.choice(facts_list)}</p>'\
    '<a href="/">Home</a>'

@app.route('/flip-coin')
def flip_coin():
    return f'<p>{random.choice(coin)}<p>'\
    '<a href="/">Home</a>'

@app.route('/gen-pass')
def gen_pass(pass_length=8):
    """Function creating a password."""
    elements = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM0123456789"
    password = ""
    for _ in range(pass_length):
        password += random.choice(elements)
    return f'<p>{password}</p>\n'\
    '<a href="/">Home</a>'

app.run(debug=True)
