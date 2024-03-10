import streamlit as st
from streamlit_option_menu import option_menu
import requests
from streamlit_lottie import st_lottie
import base64
from PIL import Image
import io

import folium
from streamlit_folium import folium_static




st.set_page_config(page_title='my portfolio', page_icon=':wave:', layout='wide')


# Obtener la ubicación del usuario (opcional)
# location = st.location()




background_image = """
<style>
[data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: 100vw 100vh;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    background-repeat: no-repeat;
}
</style>
"""

st.markdown(background_image, unsafe_allow_html=True)

def load_lottie(url):
    response= requests.get(url)
    if response.status_code !=200:
        return None
    return response.json()

# Temas
themes = ["Claro", "Oscuro","fondo_imagen"]
selected_theme = st.sidebar.radio("Selecciona un tema", themes)
# Cambiar el tema de la aplicación
if selected_theme == "Oscuro":
    st.write("""
    <style>
    [data-testid="stAppViewContainer"] > .main{
        background: #1E1E1E;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)
elif selected_theme == "Claro":
    st.write("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background: #FFFFFF;
        color: black;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.write(""" 
    <style>
          [data-testid="stAppViewContainer"] > .main {
    background-image: url("https://images.unsplash.com/photo-1542281286-9e0a16bb7366");
    background-size: cover;  # This sets the size to cover 100% of the viewport width and height
    background-position: center;  
    color: white;
}   
    </style>


""", unsafe_allow_html=True)





# Use local CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("estilos/estilos.css")






codigo_lottie= load_lottie("https://lottie.host/f6b9cd22-dde0-4035-9644-e2f47aff0432/hUS0bTQwi3.json")
codigo_lottie_proyectos= load_lottie("https://lottie.host/695aeef8-d4b0-415d-a016-00c3d9c5b0a8/hKURFkbXbT.json")
python_lottie = load_lottie("https://assets6.lottiefiles.com/packages/lf20_2znxgjyt.json")
js_lottie = load_lottie("https://lottie.host/fc1ad1cd-012a-4da2-8a11-0f00da670fb9/GqPujskDlr.json")
java_lottie = load_lottie("https://assets9.lottiefiles.com/packages/lf20_zh6xtlj9.json")
my_sql_lottie = load_lottie("https://assets4.lottiefiles.com/private_files/lf30_w11f2rwn.json")
git_lottie = load_lottie("https://assets9.lottiefiles.com/private_files/lf30_03cuemhb.json")
github_lottie = load_lottie("https://assets8.lottiefiles.com/packages/lf20_6HFXXE.json")
docker_lottie = load_lottie("https://assets4.lottiefiles.com/private_files/lf30_35uv2spq.json")

st.write('##')
st.subheader('Bienvenidos  A mi PORTAFOLIO :smile:')

st.write('''Mi  nombre  es  Juan, actualmente soy el ceo y fundador
         y  de una startup de inteligencia artificial y realidad aumentada, Recuerda,
         la palabra imposible borrala de Tu Vocabulario, 
         y lograras lo impensado!...''')

st.write('----')




#animacion 1 Cargar imágenes desde el sistema de archivos
image1 = Image.open("img/img1.jpg")
image2 = Image.open("img/img2.jpg")
image3 = Image.open("img/img3.jpg")
image4 = Image.open("img/img4.jpg")

# Lista de imágenes
images = [image1, image2, image3, image4]

# Título del slider carousel
st.title("Slider Carousel con Streamlit")

# Seleccionar la imagen actual mediante un slider
image_index = st.slider("Selecciona una imagen", 0, len(images)-1, 0)

# Mostrar la imagen actual
st.image(images[image_index], use_column_width=True)

#animacion 2 Cargar imágenes desde el sistema de archivos

uploaded_files = st.file_uploader("Cargar imágenes", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Verificar si se han cargado archivos
if uploaded_files:
    # Lista de imágenes
    images = [Image.open(file) for file in uploaded_files]

    # Título del slider carousel
    st.title("Slider Carousel con Streamlit")

    # Seleccionar la imagen actual mediante un slider
    image_index = st.slider("Selecciona una imagen", 0, len(images)-1, 0)

    # Mostrar la imagen actual
    st.image(images[image_index], use_column_width=True)


with st.container():
    selected = option_menu(
        menu_title= None,
        options= ['Acerca de mi',  'Contactame!..','Curriculum','skills'],
        icons=['person-check', 'code-slash', 'chat'],
        orientation = 'horizontal',
    )

if selected == 'Acerca de mi':
    with st.container():
        col1,col2= st.columns(2)
        with col1:
            st.write("##")
            st.subheader("Hola MI nombre es Juan  Quintero!")
            st.title("""
                     Soy un apasionado por la tecnologia, la inteligencia artificial 
                     el analisis de datos y desarollo web Fullstack Es un placer conocerlos!
                     y aun mas que cada vez nuestra comunidad de programadores crece a pasos
                     agigantados! 
                     """)
        with col2:
            st_lottie(codigo_lottie)



if selected == 'Contactame!..':
    with st.container():
        st.write("---")
        st.header("Enviame Un Mensaje!")
        st.write("##")

        contact_form = """
        <form action="https://formsubmit.co/jvera02@itfip.edu.co" method="POST">
            <input type="hidden" name="_captcha" value="false">
            <input type="text" name="name" placeholder="Tu Nombre" required>
            <input type="text" name="email" placeholder="Tu email" required>
            <textarea name="message" placeholder="Ingresa Tu Mensaje" required></textarea>
            <button type="submit">Enviar</button>
        </form>
        """
        left_column, right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            st_lottie(codigo_lottie)
        
        st.header("Mi Ubicacion")
        
       # Crear un mapa centrado en la ubicación del usuario
        m = folium.Map(location=[4.43889, -75.23222], zoom_start=10)

        # Añadir un marcador en la ubicación del usuario
        folium.Marker([4.43889, -75.23222], tooltip=" Aqui estoy").add_to(m)

        # Mostrar el mapa en la aplicación de Streamlit
        folium_static(m)

# Mostrar el mapa en la aplicación de Streamlit
if selected == 'Curriculum':
    with open("img/doc_aplicaciones.pdf","rb") as f:
      base64_pdf = base64.b64encode(f.read()).decode('utf-8')
      pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="1000mm" height="1000mm" type="application/pdf"></iframe>'
      st.markdown(pdf_display, unsafe_allow_html=True)
      
    def load_pdf(file_path):
            with open(file_path, "rb") as f:  # Abre el archivo en modo binario "rb"
                base64_pdf = base64.b64encode(f.read())  # Lee el archivo y lo codifica en base64
            return base64_pdf

        # Cargar el archivo PDF
    pdf_data = load_pdf("img/doc_aplicaciones.pdf")

        # Mostrar el PDF
    pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_data.decode()}" width="1000mm" height="1000mm" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

        # Agregar el botón de descarga

        # Función para crear el enlace de descarga
    def get_binary_file_downloader_html(bin_file, file_label='File', file_name='filename'):
            href = f'<a href="data:application/octet-stream;base64,{bin_file.decode()}" download="{file_name}">{file_label}</a>'
            return href

    st.markdown(get_binary_file_downloader_html(pdf_data, file_label='Descargar PDF', file_name='doc_aplicaciones.pdf'), unsafe_allow_html=True)

if selected == 'skills':
       with st.container():
        col1,col2= st.columns(2)
        with col1:
            st.write("##")
            st.subheader("Python")
            st.write(""" Mis conocimientos con este lenguaje son avanzados,
            dado que he logrado implementar aplicaciones web utilizando django y flask,
            al mismo tiempo aplicaciones de analisis de datos e inteligencia artificial usando
                     Streamlit""")
        with col2:
            st_lottie(python_lottie)
        
        st.markdown("---")

        with st.container():
            col1,col2= st.columns(2)
            with col1:
                st.write("##")
                st.subheader("javascript")
                st.write(""" Mis conocimientos con este lenguaje son de un nivel 
                          intermedio avanzado,
                           dado que he logrado implementar aplicaciones web utilizando react y angular,vue
                          al mismo tiempo aplicaciones Moviles con react Native""")
            with col2:
                st_lottie(js_lottie)
        st.markdown("---")

        with st.container():
            col1,col2= st.columns(2)
            with col1:
                st.write("##")
                st.subheader("java")
                st.write(""" Mis conocimientos con este lenguaje son de un nivel 
                          intermedio avanzado,
                           dado que he logrado implementar aplicaciones web utilizando Spring y Hibernate ,
                          al mismo tiempo aplicaciones Moviles con Kotlin y Android Estudio""")
            with col2:
                st_lottie(java_lottie)
        
        with st.container():
            col1,col2= st.columns(2)
            with col1:
                st.write("##")
                st.subheader("Mysql")
                st.write(""" Mis conocimientos con esta Base de datos  son de un nivel 
                           avanzado,
                           dado que he logrado implementar aplicaciones web utilizando esta base de datos""")
            with col2:
                st_lottie(my_sql_lottie)

            with st.container():
                col1,col2= st.columns(2)
                with col1:
                    st.write("##")
                    st.subheader("Git")
                    st.write(""" Mis conocimientos con Git son de un nivel 
                            avanzado,
                            dado que he logrado implementar la clonacion y migracion de distintas aplicaciones utilizando commit
                            y master""")
                with col2:
                    st_lottie(git_lottie)

            with st.container():
                col1,col2= st.columns(2)
                with col1:
                    st.write("##")
                    st.subheader("Github")
                    st.write(""" Mis conocimientos con Github  son de un nivel 
                            avanzado,
                            dado que he logrado implementar la clonacion y migracion de distintos repositorios  utilizando commit
                            y master""")
                with col2:
                    st_lottie(github_lottie)





        
