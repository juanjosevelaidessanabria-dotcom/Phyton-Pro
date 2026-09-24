from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # Diccionario con valores por defecto para la primera carga (GET)
    meme_data = {
        'selected_image': 'logo.svg',
        'text_top': '',
        'text_bottom': '',
        'text_top_y': '10',    
        'text_bottom_y': '10', 
        'selected_color': 'white',
        'text_size': '40'
    }

    if request.method == 'POST':
        # La imagen seleccionada y el tamaño del texto ya vienen configurados (¡Úsalos como guía!)
        meme_data['selected_image'] = request.form.get('image-selector', 'logo.svg')
        meme_data['text_size'] = request.form.get('text_size', '40')
        
        # Todo Asignación #2: Recepción de imagen y textos
        # Reemplaza los '...' con la función correcta para obtener los datos del formulario HTML
        meme_data['text_top'] = request.form.get('textTop', '')
        meme_data['text_bottom'] = request.form.get('textBottom', '')
        
        # Todo Asignación #3: Recepción de posición y color
        meme_data['text_top_y'] = request.form.get('textTop_y', '10')
        meme_data['text_bottom_y'] = request.form.get('textBottom_y', '10')
        meme_data['selected_color'] = request.form.get('color-selector', 'white')

    # Pasamos el diccionario desempaquetado a la plantilla
    return render_template('index.html', **meme_data)

if __name__ == '__main__':
    app.run(debug=True)