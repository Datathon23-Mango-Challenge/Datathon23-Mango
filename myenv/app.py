from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def show_images():
    # Carga los datos
    data = pd.read_csv('/home/pmorente/Documents/Projects/Datathon23-Mango/Datathon23-Mango/myenv/static/csvs/merged_data.csv')
    # Toma solo los primeros 5 registros
    #unique_merged_data = data.drop_duplicates(subset=['cod_modelo_color'])
    random_eight_unique_records = data.sample(n=8)
    images = random_eight_unique_records.head(8)['des_filename'].tolist()
    # No es necesario el prefijo '/static/images/' porque 'url_for' se encargará de eso
    # Renderiza la plantilla HTML con los nombres de las imágenes
    return render_template('index.html', image_paths=images)

if __name__ == '__main__':
    app.run(debug=True)
