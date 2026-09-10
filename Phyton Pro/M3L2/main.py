from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('C:/Users/USUARIO/OneDrive/Desktop/Phyton Pro/M3L2/index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

app.run(debug=True)
