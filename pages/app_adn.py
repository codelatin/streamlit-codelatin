import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
from reportlab.pdfgen import canvas
from io import BytesIO
#import altair_viewer
#import base64



# Función para contar nucleótidos
def DNA_nucleotide_count(seq):
    return dict(A=seq.count('A'), T=seq.count('T'), G=seq.count('G'), C=seq.count('C'))

# Función para imprimir el diccionario
def print_dictionary(X):
    st.subheader('1. Print dictionary')
    st.write(X)

    # Convertir el DataFrame a CSV
    csv_file = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    st.download_button("Descargar Diccionario", csv_file.to_csv(index=False).encode('utf-8'), file_name="nucleotide_counts.csv", key="dictionary_download")

# Función para imprimir texto

def print_text(X):
    st.subheader('2. Print text')
    
    # Crear un objeto BytesIO para almacenar el PDF
    pdf_buffer = BytesIO()
    
    # Crear el archivo PDF usando reportlab
    pdf = canvas.Canvas(pdf_buffer)
    pdf.drawString(100, 750, 'Nucleotide Counts')
    y_position = 730
    
    for nucleotide, count in X.items():
        pdf.drawString(100, y_position, f'There are {count} {nucleotide} nucleotides')
        y_position -= 15
    
    pdf.save()
    
    # Descargar el archivo PDF
    st.download_button("Descargar Texto", pdf_buffer.getvalue(), file_name="nucleotide_counts.pdf", key="text_download")

# Función para mostrar DataFrame
def show_dataframe(X):
    st.subheader('3. Display DataFrame')
    df = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    st.write(df)







# Mostramos el Grafico de barras
def show_bar_chart(X):
    st.subheader('4. Gráfico de Barras')

    # Recopilar las preferencias del usuario
    bar_width = st.slider("Ancho de las barras", min_value=1, max_value=100, value=20)
    bar_color = st.color_picker("Color de las barras", value="#4682B4")
    background_color = st.color_picker("Color de fondo del gráfico", value="#FFFFFF")
    sort_bars = st.checkbox("Ordenar barras por recuento", value=True)

    df = pd.DataFrame.from_dict(X, orient='index').reset_index().rename(columns={'index': 'nucleotide', 0: 'count'})
    
    # Ordenar las barras si se ha seleccionado la opción
    if sort_bars:
        df = df.sort_values(by='count', ascending=False)

    # Aplicar las preferencias del usuario al gráfico
    chart = alt.Chart(df).mark_bar(color=bar_color).encode(
        x=alt.X('nucleotide', sort=None),  # Deshabilitar la ordenación automática de las barras
        y='count',
        tooltip=['nucleotide', 'count']
    ).properties(
        width=bar_width,  # Controla el ancho de las barras
        title='Nucleotide Count Bar Chart'
    )

    # Agregar etiquetas a las barras
    text = chart.mark_text(
        align='center',
        baseline='bottom',
        dx=0,  # Desplazamiento horizontal
        dy=5  # Desplazamiento vertical
    ).encode(
        text='count:Q'  # Utilizar el recuento como etiqueta
    )

    # Agregar título y etiquetas de ejes
    chart = (chart + text).properties(
        title='Nucleotide Count Bar Chart',
        width=600,
        height=400
    ).configure_axis(
        labelFontSize=12,  # Tamaño de fuente de las etiquetas de los ejes
        titleFontSize=14  # Tamaño de fuente del título del gráfico
    )

    # Personalizar el color de fondo del gráfico
    chart = chart.configure_view(
        fill=background_color  # Establecer el color de fondo del gráfico
    )

    # Convertir el gráfico a HTML
    chart_html = chart.to_html()

    st.altair_chart(chart)
    
    # Descargar el gráfico con las preferencias seleccionadas por el usuario
    st.download_button("Descargar Gráfico de Barras", chart_html, file_name="grafico_barras.html", key="chart_download")



# Función para validar la secuencia de ADN
def is_valid_dna_sequence(sequence):
    valid_characters = set('ATGC')
    return all(char.upper() in valid_characters for char in sequence)

# Configuración de la página
image = Image.open('pages/img_adn/adn.jpeg')
st.image(image, use_column_width=True)
st.markdown("# Nucleotidos**")

# Entrada de secuencia
st.header("Ingresar CADENA DE ADN")
# Entrada de secuencias
#sequence_input = ">DNA Query 2\AAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATC"
#sequence = st.text_area("Sequence input", sequence_input, height=250).splitlines()[1:]
#sequence = ''.join(sequence)
sequences_input = ">DNA Query 1\nAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATC"
sequences = st.text_area("Sequences input", sequences_input, height=250).splitlines()


# Validar las secuencias de ADN
valid_sequences = [seq for seq in sequences if is_valid_dna_sequence(seq)]

if valid_sequences:
    st.success("Valid DNA sequences!")

    # Mostrar histograma de longitudes
    st.header("Histograma de Longitudes")
    sequence_lengths = [len(seq) for seq in valid_sequences]
    hist_chart = alt.Chart(pd.DataFrame({'Length': sequence_lengths})).mark_bar().encode(
        alt.X('Length:Q', bin=alt.Bin(maxbins=30), title='Longitud'),
        alt.Y('count():O', title='Frecuencia'),
        tooltip=['Length:Q', 'count()']
    ).properties(
        width=600,
        height=400,
        title='Histograma de Longitudes de Secuencias de ADN'
    )
    st.altair_chart(hist_chart)

    # Mostrar resultados para cada secuencia
    for index, sequence in enumerate(valid_sequences, start=1):
        st.write(f"### Sequence {index}")
        st.write(sequence)

        # Resto del código para cada secuencia...

#fin codigo Histograma


# Validar la secuencia de ADN
if is_valid_dna_sequence(sequence):
    st.success("Valid DNA sequence!")
    # Mostrar entrada de secuencia
    st.write("***\n")
    st.header('INPUT (DNA Query)')
    st.write(sequence)

    # Contar nucleótidos y mostrar resultados
    st.header('OUTPUT (DNA Nucleotide Count)')
    X = DNA_nucleotide_count(sequence)


        # Función para calcular el porcentaje de cada nucleótido
    def calculate_pass(X, total_Log):
        return {nucleotide: count /total_Log * 100 for nucleotide, count in X.items()}

    # Obtener la longitud total de la secuencia
    total_Log = len(sequence)

    # Calcular el porcentaje de cada nucleótido
    PorcentageX = calculate_pass(X, total_Log)

    # Mostrar el porcentaje de cada nucleótido
    st.subheader('5. Display Nucleotide Percentage')
    for nucleotide, percentage in PorcentageX .items():
        st.write(f'The percentage of {nucleotide} is {percentage:.2f}%')

    # Mostrar gráfico de pastel
    st.subheader('6. Display Pie Chart')
    df_percentage = pd.DataFrame(list(PorcentageX.items()), columns=['nucleotide', 'percentage'])
    pie_chart = alt.Chart(df_percentage).mark_circle().encode(
        alt.X('nucleotide:N', axis=alt.Axis(title='Nucleotido')),
        alt.Y('percentage:Q', axis=alt.Axis(title='Porcentaje')),
        color='nucleotide:N',
        size='percentage:Q',
        tooltip=['nucleotide', 'percentage']
    ).properties(
        title='Nucleotide Percentage Pie Chart',
        width=500,
        height=500
    )
    st.altair_chart(pie_chart)

    # Encontrar el nucleótido más común
  
    nucleotide_mas_comun = max(X, key=X.get)
    most_common_count = X[nucleotide_mas_comun ]

    # Mostrar el nucleótido más común
    st.subheader('7. Most Common Nucleotide')
    st.write(f'The most common nucleotide is {nucleotide_mas_comun} with a count of {most_common_count}.')


        # Función para invertir la secuencia de ADN
    def reverse_dna_sequence(sequence):
        return sequence[::-1]

    # Invertir la secuencia de ADN
    reversed_sequence = reverse_dna_sequence(sequence)

# Mostrar la secuencia invertida
    st.subheader('8. Reversed DNA Sequence')
    st.write(reversed_sequence)



    # Mostrar resultados en diferentes secciones
    print_dictionary(X)
    print_text(X)
    show_dataframe(X)
    show_bar_chart(X)
else:
    st.error("se quencia invalidada'A', 'T', 'G', and 'C'.")
