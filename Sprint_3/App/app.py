import pandas as pd
import geopandas as gpd
import streamlit as st
import folium
from streamlit_folium import st_folium
import branca.colormap as cm

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
    selection = st.radio('Seleciona el analisis',['Cantidad de viajes','Total ganancias', 'Promedio del pasaje', 'Total distancia recorrida'], index=0,)
    
    if selection == 'Cantidad de viajes':
        selection = 'cant_registros'
    elif selection == 'Total ganancias':
        selection = 'costo_total'
    elif selection == 'Promedio del pasaje':
        selection = 'costo_promedio'
    elif selection == 'Total distancia recorrida':
        selection = 'distancia_promedio'






#______________________Dataframe

df = gdf[['boro_name', 'geometry']]
df_cp = data[['boro_name',selection]]

#_____________________Merge

df_geo = df.merge(df_cp, on='boro_name')


#________________________Glabal Variables
#Color variable
myscale = (df_geo[selection].quantile((0,0.25,0.5,0.75,0.85,1))).tolist()



#________________________Body

st.subheader('Ciudad de Nueva York')
m = folium.Map(location=[40.71483, -73.99726],
                tiles='Esri_WorldGrayCanvas', 
                zoom_start=10,
                zoom_control=False,
                dragging=False,
                scrollWheelZoom=False,
                max_bounds=True,)

#folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)

# choropleth = folium.Choropleth(
#     geo_data=g_data
# )

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


