import pandas as pd
import geopandas as gpd
import streamlit as st
#import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium


#____________________ Page configuration


st.set_page_config(
    layout='wide',
    initial_sidebar_state='auto'
)

#_____________________ Source dataset reading.

g_data = r'Sprint_3\App\Data\Borough_Boundaries.geojson'
data = (r'Sprint_3\App\Data\yellow_taxis.csv')

@st.cache_data   #cache the csv file
def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

@st.cache_data   #cache the csv file
def load_geoData(geo_file_path):
    df = gpd.read_file(geo_file_path)
    return df


data = load_data(data)
gdf = load_geoData(g_data)

#______________________________________Sidebar

with st.sidebar:
    st.title('Analisis')
    '---'
    selection = st.radio('Seleciona el analisis',['Cantidad de viajes','Total ganancias', 'Promedio del pasaje', 'Promedio distancia recorrida'], index=0,)
    
    if selection == 'Cantidad de viajes':
        selection = 'cant_registros'
        sel = 'Cantidad de viajes'
    elif selection == 'Total ganancias':
        selection = 'costo_total'
        sel = 'Total ganancias'
    elif selection == 'Promedio del pasaje':
        selection = 'costo_promedio'
        sel = 'Promedio del pasaje'
    elif selection == 'Promedio distancia recorrida':
        selection = 'distancia_promedio'
        sel = 'Distancia promedio'

    

#______________________Dataframe

df = gdf[['boro_name', 'geometry']]
df_cp = data[['boro_name',selection]]

df_s = df_cp.sort_values(by=selection, ascending=False)

#borough_list = df_s.to

#_____________________Merge

df_geo = df.merge(df_cp, on='boro_name')

#________________________Glabal Variables
#Color variable
myscale = (df_geo[selection].quantile((0,0.25,0.5,0.75,0.85,1))).tolist()
img = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\Imagenes_3\Leyenda_01.jpg'


#________________________Body
st.subheader(f'Analisis mensual mes de febrero 2024')
st.subheader(f'{sel} servicio taxis amarillos en la ciudad de Nueva York ')
col1, col2 = st.columns([2,1])

with col1:    
    m = folium.Map(location=[40.71483, -73.99726],
                    tiles='Esri_WorldGrayCanvas', 
                    zoom_start=10,
                    zoom_control=False,
                    dragging=False,
                    scrollWheelZoom=False,
                    max_bounds=True,)

   

    choropleth = folium.Choropleth(
        geo_data=g_data,
        name='Choropleth',
        legend_name='Cantidad de viajes',
        data=df_geo,
        columns=['boro_name',selection],
        key_on="feature.properties.boro_name",
        fill_color='YlGnBu',   #YlGnBu
        threshold_scale=myscale,
        fill_opacity=.5,
        line_opacity=.75,
        line_weight=2,
        line_color='darkgray',    
        smooth_factor=0  
    )
    choropleth.geojson.add_to(m)


    st_folium(m, width=500, height=700)

with col2:
    '---'
    st.image(img)
    '---'
    st.write(f'(A) Borought ({df_s.iloc[0,0]}), -- ({int(df_s.iloc[0,1])})')
    '---'
    st.write(f'(B) Borought ({df_s.iloc[1,0]}), -- ({int(df_s.iloc[1,1])})')
    '---'
    st.write(f'(C) Borought ({df_s.iloc[2,0]}), -- ({int(df_s.iloc[2,1])})')
    '---'
    st.write(f'(D) Borought ({df_s.iloc[3,0]}), -- ({int(df_s.iloc[3,1])})')
    '---'
    st.write(f'(E) Borought ({df_s.iloc[4,0]}), -- ({int(df_s.iloc[4,1])})')
    