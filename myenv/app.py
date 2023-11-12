from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')
def show_images():
    data = pd.read_csv('./static/csvs/merged_data.csv')
    # Asegurarse de que hay suficientes datos para la muestra
    if len(data) < 8:
        return "No hay suficientes datos para mostrar las imágenes."

    main_images = data.sample(n=8)  # Asumimos que esta muestra tiene las columnas necesarias

    images_info = {}
    for _, main_row in main_images.iterrows():
        # Filtrar imágenes con el mismo 'cod_outfit', excluyendo la imagen principal
        related_by_outfit = data[(data['cod_outfit'] == main_row['cod_outfit']) & (data['des_filename'] != main_row['des_filename'])]

        # Filtrar imágenes con el mismo 'des_agrup_color_eng' y diferente 'des_product_aggregated_family'
        related_by_color_family = data[(data['des_agrup_color_eng'] == main_row['des_agrup_color_eng']) & 
                                       (data['des_product_aggregated_family'] != main_row['des_product_aggregated_family']) & 
                                       (data['cod_outfit'] != main_row['cod_outfit'])]

        # Concatenar ambos conjuntos, eliminar duplicados y tomar una muestra de 6 imágenes
        related_images = pd.concat([related_by_outfit, related_by_color_family]).drop_duplicates('des_filename').sample(n=6, replace=True)

        images_info[main_row['des_filename']] = related_images['des_filename'].tolist()

    return render_template('index.html', images_info=images_info)

if __name__ == '__main__':
    app.run(debug=True)
