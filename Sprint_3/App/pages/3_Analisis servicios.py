import pandas as pd
import geopandas as gpd
import streamlit as st
import numpy as np
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt

#____________________ Page configuration


st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)

#_____________________ Source dataset reading.

g_data = r'Sprint_3\App\Data\Borough_Boundaries.geojson'
v_data = (r'Sprint_3\App\Data\green_taxis.csv')
y_data = (r'Sprint_3\App\Data\yellow_taxis.csv')


@st.cache_data   #cache the csv file
def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

@st.cache_data   #cache the csv file
def load_geoData(geo_file_path):
    df = gpd.read_file(geo_file_path)
    return df


df_verde = load_data(v_data)
df_amarillo = load_data(y_data)
gdf = load_geoData(g_data)

#______________________________________Sidebar

with st.sidebar:
    st.title('Boroughts')
    '---'
    selection = st.radio('Seleciona el Borough:',['Manhattan','Bronx', 'Queens', 'Brooklyn', 'Staten Island'], index=0,)
    
    if selection == 'Manhattan':        
        cordenada = [40.75151, -73.99014]
    elif selection == 'Bronx':        
        cordenada = [40.84500, -73.87071]
    elif selection == 'Queens':        
        cordenada = [40.67424, -73.82498]
    elif selection == 'Brooklyn':        
        cordenada = [40.65374, -73.94173]
    elif selection == 'Staten Island':        
        cordenada = [40.58202, -74.15513]

    

#______________________Dataframe



df = gdf[['boro_name', 'geometry']]
df_geo = df[df['boro_name'] == selection]

#________________________Body
st.subheader(f'Analisis mensual mes de febrero 2024')
col1, col2 = st.columns([2,1])

with col1:    
    m = folium.Map(location=cordenada,
                    tiles='Esri_WorldGrayCanvas', 
                    zoom_start=11,
                    zoom_control=False,
                    dragging=False,
                    scrollWheelZoom=False,
                    max_bounds=True,)   

    geo = folium.GeoJson(
        df_geo,
        name='geojson',
        style_function=lambda feature: {
            'fillColor': 'green',
            'color': 'gray',
            'weight': 2,
            'fillOpacity': 0.15
            },
       
            ).add_to(m)


    st_folium(m, width=500, height=520)

with col2:
    colors = ['#F3F490', '#67EB8D']
    bar_width = 0.5
    
    #_________ Cantidad Viajes
    categories = ['Taxi Amarillo', 'Taxi Verde']
    v1 = df_amarillo.loc[df_amarillo['boro_name'] == selection, 'cant_registros'].values[0]
    v2 = df_verde.loc[df_verde['boro_name'] == selection, 'cant_registros'].values[0] 
    values = [v1, v2]
    print(values)
    fig, ax = plt.subplots()
    ax.bar(categories, values, color=colors, width=bar_width)

    
    ax.set_title('Cantidad de viajes', fontsize=24)
    ax.set_xlabel('Taxis', fontsize=18)
    ax.set_ylabel('Valores', fontsize=18)
    
    st.pyplot(fig)
    
    #________________________________Ganancia total
    categories = ['Taxi Amarillo', 'Taxi Verde']
    v1 = df_amarillo.loc[df_amarillo['boro_name'] == selection, 'costo_total'].values[0]
    v2 = df_verde.loc[df_verde['boro_name'] == selection, 'costo_total'].values[0] 
    values = [v1, v2]
    print(values)
    fig1, ax = plt.subplots()
    ax.bar(categories, values, color=colors, width=bar_width)

    
    ax.set_title('Ganancias totales', fontsize=24)
    ax.set_xlabel('Taxis', fontsize=18)
    ax.set_ylabel('Valores', fontsize=18)
    
    st.pyplot(fig1)