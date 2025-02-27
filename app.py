import os
from flask import Flask, request, render_template, send_file
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from werkzeug.utils import secure_filename
from time_series_analysis import generate_time_series_analysis
from report_generator import create_pdf_report

# Configuración de Flask
app = Flask(__name__)

# Definir carpetas
UPLOAD_FOLDER = 'uploads'
REPORT_FOLDER = 'reports'
STATIC_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['REPORT_FOLDER'] = REPORT_FOLDER
app.config['STATIC_FOLDER'] = STATIC_FOLDER

# Crear carpetas si no existen
for folder in [UPLOAD_FOLDER, REPORT_FOLDER, STATIC_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Función para verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    """ Página principal para cargar y mostrar datos """
    data = None
    filename = None

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            try:
                df = pd.read_excel(filepath)
                df.columns = df.columns.str.lower()
                data = df.head(10)
            except Exception as e:
                return f"Error al procesar el archivo: {str(e)}"

    return render_template('index.html', data=data, filename=filename)

@app.route('/analizar/<filename>')
def analizar(filename):
    """ Genera gráficos de series de tiempo y resumen de análisis """
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return "Error: El archivo no se encontró en el servidor."
    
    try:
        img_paths, resumen, pdf_filename = generate_time_series_analysis(filepath, app.config['STATIC_FOLDER'], app.config['REPORT_FOLDER'])
    except Exception as e:
        return f"Error en el análisis de series de tiempo: {str(e)}"

    return render_template('analisis.html', img_paths=img_paths, resumen=resumen, pdf_filename=pdf_filename)

@app.route('/descargar_pdf/<pdf_filename>')
def descargar_pdf(pdf_filename):
    """ Permite descargar el informe en PDF """
    return send_file(os.path.join(app.config['REPORT_FOLDER'], pdf_filename), as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))  # Render asigna un puerto dinámico
    app.run(host='0.0.0.0', port=port, debug=True)
