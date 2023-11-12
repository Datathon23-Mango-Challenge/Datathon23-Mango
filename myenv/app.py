from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)


@app.route('/')
def show_images():
    data = pd.read_csv('./static/csvs/merged_data.csv')


    main_images = data.sample(n=8)  # Asumimos que esta muestra tiene las columnas necesarias


# ... (código previo)


    images_info = {}
    for _, main_row in main_images.iterrows():
        # Filtrar imágenes con el mismo 'cod_outfit', excluyendo la imagen principal
        related_images = data[
            (data['cod_outfit'] == main_row['cod_outfit']) &
            (data['des_filename'] != main_row['des_filename'])
        ].drop_duplicates(subset=['des_product_aggregated_family', 'des_product_family', 'des_product_type'])


        # Garantizar que haya al menos un 'Bottoms' y un 'Tops'
        bottoms = data[(data['des_product_category'] == "Bottoms") & (~data['des_filename'].isin(related_images['des_filename']))]
        tops = data[(data['des_product_category'] == "Tops") & (~data['des_filename'].isin(related_images['des_filename']))]


        # Si no hay suficientes imágenes relacionadas, buscar más imágenes por color
        if len(related_images) < 4:  # Dejamos espacio para 2 prendas adicionales
            additional_images = data[
                (data['des_agrup_color_eng'] == main_row['des_agrup_color_eng']) &
                (~data['des_filename'].isin(related_images['des_filename'])) &
                (data['des_product_category'] != "Bottoms") &  # Excluir 'Bottoms'
                (data['des_product_category'] != "Tops")      # Excluir 'Tops'
            ].drop_duplicates(subset=['des_product_aggregated_family', 'des_product_family', 'des_product_type'])


            related_images = pd.concat([related_images, additional_images]).drop_duplicates(subset=['des_product_family', 'des_product_type']).head(4)


            # Añadir al menos un 'Bottoms' y un 'Tops'
           
            if bottoms.empty or tops.empty:
                    # Manejo de casos donde no hay disponibles suficientes 'Bottoms' o 'Tops'
                pass
            else:
                additional_images = pd.concat([additional_images, bottoms.sample(1), tops.sample(1)])


       
        images_info[main_row['des_filename']] = related_images.head(6)['des_filename'].tolist()


    return render_template('index.html', images_info=images_info)




if __name__ == '__main__':
    app.run(debug=True)


