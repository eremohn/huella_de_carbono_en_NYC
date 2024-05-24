import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


data_a = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\App\Data\Prediciones\marzo_clean\ta_marzo.csv'
data_v = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\App\Data\Prediciones\marzo_clean\tv_marzo.csv'


@st.cache_data   #cache the csv file
def load_data(csv_file_path):
    df = pd.read_csv(csv_file_path)



df_a = pd.read_csv(data_a)
df_v = pd.read_csv(data_v)


#_______________________Side-Bar



with st.sidebar:
    
    '---'
    boro_sel = st.radio('Seleciona el Borought',['Manhattan',
                                                 'Brooklyn', 
                                                 'Bronx', 
                                                 'Queens',
                                                 'Staten Island'], index=0,)
print(boro_sel)    

df_a = df_a[df_a['boro_name'] == boro_sel]
df_v = df_v[df_v['boro_name'] == boro_sel]

    
#_______________________Body   

st.subheader(f'Prediccion para el mes de Marzo en {boro_sel}')
'---'
col1, col2 = st.columns([1,1])
with col1:
    st.subheader('Taxis amarillos')
    '---'
    st.write('Predicción cantidad de servicios')
    chart_1 = df_a[['cant_registros_Historico','cant_registros_Prediccion']]
    st.bar_chart(chart_1, color=['#F5E32A','#3BF630'],  height=300)
    '---'
    st.write('Predicción ganancias')
    chart_2 = df_a[['costo_total_Historico','costo_total_Prediccion']]
    st.bar_chart(chart_2, color=['#F5E32A','#3BF630'],  height=300)
    '---'
    st.write('Predicción pasaje promedio')
    chart_3 = df_a[['costo_promedio_Historico','costo_promedio_Prediccion']]
    st.bar_chart(chart_3, color=['#F5E32A','#3BF630'],  height=300)
    '---'


with col2:
    st.subheader('Taxis verdes')
    '---'
    st.write('_')
    chart_11 = df_v[['cant_registros_Historico','cant_registros_Prediccion']]
    st.bar_chart(chart_11, color=['#F5E32A','#3BF630'],  height=300)
    '---'
    st.write('_')
    chart_22 = df_v[['costo_total_Historico','costo_total_Prediccion']]
    st.bar_chart(chart_22, color=['#F5E32A','#3BF630'],  height=300)
    '---'
    st.write('_')
    chart_333 = df_v[['costo_promedio_Historico','costo_promedio_Prediccion']]
    st.bar_chart(chart_333, color=['#F5E32A','#3BF630'],  height=300)
    


