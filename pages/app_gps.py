import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import plotly.graph_objs as go
import plotly.express as px
from folium.plugins import MarkerCluster, HeatMap
from folium import plugins
from folium.plugins import MarkerCluster
import pandas as pd
from streamlit_extras.metric_cards import style_metric_cards
#pip install streamlit-folium

#set width
st.set_page_config(page_title="Georeferenciacion", page_icon="📈", layout="wide")  

data = {
    'City': ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena','ibague',"Envigado", "Pereira"],
    'Latitude': [4.6097, 6.2442, 3.4516, 10.9639, 10.391,  4.43889, 6.17591, 4.81333],
    'Longitude': [-74.0817, -75.5812, -76.5320, -74.7964, -75.4794,  -75.23222, -75.59174, -75.69611]
}
df = pd.DataFrame(data)

# Función para agregar las ciudades colombianas al mapa
def add_colombian_cities_to_map(m, df):
    marker_cluster = MarkerCluster().add_to(m)
    for i, row in df.iterrows():
        popup_content = f"<b>{row['City']}</b>"
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            tooltip=row['City'],
            popup=popup_content
        ).add_to(marker_cluster)

# Crear un mapa centrado en Colombia
m = folium.Map(location=[4.5709, -74.2973], zoom_start=6)

# Agregar las ciudades colombianas al mapa
add_colombian_cities_to_map(m, df)

# Mostrar el mapa en Streamlit
st.title('Mapa de Ciudades Colombianas Codelatin start de tecnologia')
folium_static(m)

# load Style css
with open('pages/estilos_geo/style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)

theme_plotly = None 

load_df = pd.read_excel('pages/doc_geo/coordinates.xlsx')

 #logo
st.sidebar.image("pages/img_geo/geo.jpeg",caption="")
 
name=st.sidebar.multiselect(
    "SELECT OFFICE",
     options=load_df["Name"].unique(),
     default=load_df["Name"].unique(),
    )
df=load_df.query("Name==@name ")

#load dataset

try:
 st.header("Aplicacion Georeferenciacion  Codelatin Colombia ")
 items= load_df['Name'].count()
 total_price= float(load_df['TotalPrice'].sum())

 with st.expander("ANALisis"):
  a1,a2=st.columns(2)
  a1.metric(label="Ubicacion de Oficinas",value=items,help=f""" Total Price: {total_price} """,delta=total_price)
  a2.metric(label=" Precio Total",value=total_price,help=f""" Total Price: {total_price} """,delta=total_price)
  style_metric_cards(background_color="#FFFFFF",border_left_color="#00462F",border_color="#070505",box_shadow="#F71938")
#filter

#create a map
 m = folium.Map(location=[df['Latitude'].mean(), df['Longitude'].mean()], zoom_start=4)

 marker_cluster = MarkerCluster().add_to(m)
 for i, row in df.iterrows():
    popup_content = f"""
      <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
      <ul class="list-group">
      <h3>Information of {row['Name']}</h3>
      <hr class'bg-danger text-primary'>
      <div style='width:400px;height:200px;margin:10px;color:gray;text-size:18px;'>
      <li class="list-group-item"><b>Branch Manager:</b> {row['Manager']}</li>
      <li class="list-group-item"><b>Collection:</b> {row['Collection']} USD<br></li>
      <li class="list-group-item"><b>Name:</b> {row['Name']}<br></li>
      <li class="list-group-item"><b>Quantity:</b> {row['Quantity']}<br></li>
      <li class="list-group-item"><b>Unit Price:</b> {row['UnitPrice']}<br></li>
      <li class="list-group-item"><h4>Total Price:  {row['TotalPrice']} USD</b><br></li>
      <li class="list-group-item"><h4>Phone {row['Phone']}</h4></li>"""
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        tooltip=row['Name'],
        icon=folium.Icon(color='red', icon='fa-dollar-sign', prefix = 'fa'),
    ).add_to(marker_cluster).add_child(folium.Popup(popup_content, max_width=600))  

 # Heatmap Layer
 heat_data = [[row['Latitude'], row['Longitude']] for i, row in df.iterrows()]
 HeatMap(heat_data).add_to(m)

 # Fullscreen Control
 plugins.Fullscreen(position='topright', title='Fullscreen', title_cancel='Exit Fullscreen').add_to(m)

 # Drawing Tools
 draw = plugins.Draw(export=True)
 draw.add_to(m)

 def add_google_maps(m):
    tiles = "https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}"
    attr = "Google Digital Satellite"
    folium.TileLayer(tiles=tiles, attr=attr, name=attr, overlay=True, control=True).add_to(m)
    # Add labels for streets and objects
    label_tiles = "https://mt1.google.com/vt/lyrs=h&x={x}&y={y}&z={z}"
    label_attr = "Google Labels"
    folium.TileLayer(tiles=label_tiles, attr=label_attr, name=label_attr, overlay=True, control=True).add_to(m)
   
    return m

 with st.expander("Mapas De Oficinas Por Medio DE Coordenadas"):
  m = add_google_maps(m)

  m.add_child(folium.LayerControl(collapsed=False))
  #folium_static(m, width=1350, height=600)
  folium_static(m, width=1350, height=600)
  folium.LayerControl().add_to(m)  # Add layer control to toggle different layers

 # Show table data when hovering over a marker
 with st.expander("SELECCIONAR DATOS"):
  selected_city = st.selectbox("Selecciona una Ciudad", df['Name'])
  selected_row = df[df['Name'] == selected_city].squeeze()
  # Display additional information in a table
  st.table(selected_row)

#Graphs
 col1,col2=st.columns(2)
 with col1:
  #feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
  fig2 = go.Figure(
    data=[go.Bar(x=df['Name'], y=df['TotalPrice'])],
    layout=go.Layout(
        title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
     )
  )
  st.plotly_chart(fig2,use_container_width=True)

 with col2:
 # Create a donut chart
  fig = px.pie(df, values='TotalPrice', names='Name', title='TotalPrice by Name')
  fig.update_traces(hole=0.4)  # Set the size of the hole in the middle for a donut chart
  fig.update_layout(width=800)
  st.plotly_chart(fig, use_container_width=True)
  
except:
  st.error("Unable to display null, select at least one business location")

