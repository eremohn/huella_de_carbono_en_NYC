import pandas as pd
import geopandas as gpd
import streamlit as st
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

data_t = (r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\App\Data\taxis_clean\taxis_clean.csv')


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

df_taxi = load_data(data_t)


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

df_taxi = df_taxi[df_taxi['boro_name'] == selection]
df_taxi = df_taxi[df_taxi['dia'] == '2024-02-01']
#df_taxi = df_taxi.set_index('dia')


#________________________Body

tab1, tab2, tab3 = st.tabs(['Análisis zonal', 'Comparacion mensual Taxis periodo (Enero-2022 a Febrero-2024)', 'Comparativa metricas ultimo mes'])


with tab1:
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
        
        a_totales = df_taxi['Costo_total_(TA)'] + df_taxi['Costo_total_(TV)']
        b_totales = (df_taxi['Costo_promedio_(TA)'] + df_taxi['Costo_promedio_(TV)'])/2
        c_totales = df_taxi['Total_viajes_(TA)'] + df_taxi['Total_viajes_(TV)']
        st.write('Datos totales servicio de taxis verdes y amarillos')
        '---'
        st.subheader(f'Ganancias = {int(a_totales)} US$')
        '---'
        st.subheader(f'Promedio pasaje = {int(b_totales)} US$')
        '---'
        st.subheader(f'Total de servicios = {int(c_totales)}')
        '---'
        
        
        
    

with tab2:
    st.write('Comparacion total de viajes')
    chart_1 = df_taxi[['Total_viajes_(TA)','Total_viajes_(TV)']]
    st.area_chart(chart_1, color=['#F5E32A','#3BF630'], height=300)
    '---'
    st.write('Comparacion costo promedio del servicio')
    chart_2 = df_taxi[['Costo_promedio_(TA)','Costo_promedio_(TV)']]
    st.area_chart(chart_2, color=['#F5E32A','#3BF630'], height=300)
    '---'
    st.write('Comparacion ganancias total del servicio mensualmente')
    chart_3 = df_taxi[['Costo_total_(TA)','Costo_total_(TV)']]
    st.area_chart(chart_3, color=['#F5E32A','#3BF630'], height=300)
    
    
with tab3:
    st.header('Metricas ultimo mes')   
    '---' 
    colors = ['#F5E32A','#3BF630']
    
    m1, m2, m3 = st.columns([1,1,1])
    
    with m1:
        st.write('Ganancias')
        a = 'Ganancia_(TA) (US$)'
        b = 'Ganancia_(TV) (US$)'
        
        c = df_taxi['Costo_total_(TA)'].iloc[0]
        d = df_taxi['Costo_total_(TV)'].iloc[0]
        
        x = [a,b]
        y = [c,d]
        
        fig5, ax = plt.subplots()
        ax.bar(x, y, color=colors)
        
        st.pyplot(fig5)
        
    with m2:
        st.write('Promedio costo pasaje')
        e = 'Pasaje promedio (TA) (US$)'
        f = 'Pasaje promedio (TV) (US$)'
        
        g = df_taxi['Costo_promedio_(TA)'].iloc[0]
        h = df_taxi['Costo_promedio_(TV)'].iloc[0]
        
        xx = [e,f]
        yy = [g,h]
        
        fig6, ax = plt.subplots()
        ax.bar(xx, yy, color=colors)
        
        st.pyplot(fig6)
        
    with m3:
        st.write('Promedio costo pasaje')
        i = 'Numero de viajes (TA) (US$)'
        j = 'Numero de viajes (TV) (US$)'
        
        k = df_taxi['Total_viajes_(TA)'].iloc[0]
        l = df_taxi['Total_viajes_(TV)'].iloc[0]
        
        xxx = [i,j]
        yyy = [k,l]
        
        fig7, ax = plt.subplots()
        ax.bar(xxx, yyy, color=colors)
        
        st.pyplot(fig7)