from flask import Flask, render_template, request

app = Flask(__name__)

# ── Función auxiliar ──────────────────────────────────────────────────────────
def result_calculate(size: int, lights: int, devices: int) -> float:
    home_coef    = 100   # kWh base por tamaño del hogar
    light_coef   = 2.0   # kWh por lámpara
    devices_coef = 5     # kWh por aparato eléctrico
    return size * home_coef + lights * light_coef + devices * devices_coef

# ── Rutas de la calculadora ───────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/size/<int:size>')
def select_lights(size):
    return render_template('lights.html', size=size)

@app.route('/size/<int:size>/lights/<int:lights>')
def select_devices(size, lights):
    return render_template('electronics.html', size=size, lights=lights)

@app.route('/size/<int:size>/lights/<int:lights>/devices/<int:devices>')
def show_result(size, lights, devices):
    result = result_calculate(size, lights, devices)
    return render_template('end.html', result=result)

# ── Rutas del formulario ──────────────────────────────────────────────────────
@app.route('/form')
def form():
    return render_template('form.html')

# ────────────────────────────────────────────────────────────────────────────
# TAREA 6 · El backend del formulario
# ────────────────────────────────────────────────────────────────────────────
# Esta función recibe los datos que el usuario envió en el formulario.
# El decorador @app.route ya está listo; tú sólo tienes que completar
# el cuerpo de la función.
#
# Paso 1 — Leer los campos del formulario
# ─────────────────────────────────────────
# Usa request.form['...'] para leer cada campo por su atributo "name".
# El atributo "name" de cada <input> en form.html actúa como clave.
# Ya tienes un ejemplo con "name"; sigue el mismo patrón para el resto:
#
#     name    = request.form['name']
#     email   = request.form['...']    # ← escribe el name correcto
#     address = request.form['...']
#     date    = request.form['...']
#
# Paso 2 — Enviar los datos a la plantilla
# ──────────────────────────────────────────
# render_template() acepta tantos argumentos con nombre (keyword args)
# como variables necesites pasar. Sigue el ejemplo de "name=name" y
# añade las demás variables para que puedan usarse en form_result.html.
# ────────────────────────────────────────────────────────────────────────────
@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    # Declara aquí las variables para los campos restantes
    # (sigue el patrón de arriba)
    name    = request.form['name']
    email   = request.form['email']
    address = request.form['address']
    date    = request.form['date']

    with open('form.txt', 'a',encoding="utf-8",newline='\n') as f:
        f.write(name + '\n'+ email + '\n'+ address + '\n' + date + '\n\n')

    return render_template(
        'form_result.html',
        name=name,
        email=email,
        address=address,
        date=date
        # Pasa aquí las demás variables que acabas de declarar
    )

# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # debug=True muestra errores detallados y recarga automáticamente.
    # ¡Recuerda cambiarlo a False antes de publicar una app real!
    app.run(debug=True)
