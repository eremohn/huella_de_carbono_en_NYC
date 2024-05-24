import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


img = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\Imagenes_3\reduccion.jpg'
data_co2 = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_1\CSV\NYC_CO2.csv'

data_p = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\App\Data\Prediciones\co2_fix.csv'
@st.cache_data   #cache the csv file
def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)
    return df

df_c = load_data(data_co2)

df_p = load_data(data_p)

st.subheader('Contaminación anual de CO2 en la ciudad de Nueva York, período 1970 a 2021')
chart_1 = df_c['Total']
st.bar_chart(chart_1, color='#F5E32A',  height=300)
'---'
st.subheader('Predicción anual de contaminación por CO2 hasta 2030')
chart_2 = df_p[['Historico','Prediccion']]
st.bar_chart(chart_2, color=['#F5E32A','#3BF630'],  height=300)


with st.sidebar:
    '---'
    st.image(img)
    '---'