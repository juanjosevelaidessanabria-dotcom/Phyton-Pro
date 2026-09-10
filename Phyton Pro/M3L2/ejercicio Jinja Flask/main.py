from flask import Flask, render_template

app = Flask(__name__)

def result_calculate(size: int, lights: int, devices: int) -> float:
    home_coef = 100   # kWh base por tamaño del hogar
    light_coef = 2.0   # kWh por lámpara
    devices_coef = 5   # kWh por aparato eléctrico
    return size * home_coef + lights * light_coef + devices * devices_coef

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

if __name__ == '__main__':
    # debug=True muestra errores detallados y recarga automáticamente.
    # ¡Recuerda cambiarlo a False antes de publicar una app real!
    app.run(debug=True)
