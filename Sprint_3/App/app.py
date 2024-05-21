import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
from branca.colormap import linear
#____________________ Page configuration


st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)

#_____________________ Source dataset reading.


data = r"D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\App\Data\Borough Boundaries.geojson"
data1 = r"Sprint_3\App\Data\yellow_taxis.csv"
df = gpd.read_file(data)
df1 = pd.read_csv(data1)

#________________________Glabal Variables






#________________________Colormap

colormap = linear.YlGn_09.scale(
    df1.cant_registros.min(), df1.cant_registros.max()
)

#________________________Global Variables
color_dict = df1.set_index("boro_name")["cant_registros"]

#________________________Body


st.subheader('Ciudad de Nueva York')
m = folium.Map(location=[40.71483, -73.99726], 
            tiles='Esri_WorldGrayCanvas', 
            zoom_control=False, 
            zoom_start=10, 
            dragging=False,
            min_zoom=10,
            scrollWheelZoom=False,
            max_bounds=True,               
            )



folium.GeoJson(df,
    name="total_viajes",
    style_function=lambda feature: {
        "fillColor": colormap(color_dict.get(feature["properties"]["boro_name"], 0)),
        "color": "black",
        "weight": 1,
        "dashArray": "5, 5",
        "fillOpacity": 0.5,
        
    },
).add_to(m)








colormap.caption = "Total de viajes"
colormap.add_to(m)


st_data = st_folium(m, width=600, height=700)

