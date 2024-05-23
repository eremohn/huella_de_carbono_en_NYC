import streamlit as st

img = r'D:\0_Respaldo\0_Proyectos_2024\Henry-PF\PF\huella_de_carbono_en_NYC\Sprint_3\Imagenes_3\logo_company.png'

cl1, cl2, cl3 = st.columns([1,2,1])

with cl2:
    '---'
    st.image(img, width=320)
    '---'
    st.subheader('Análisis de la contaminación de CO2 y el transporte')
    st.subheader('--- Nueva York 2024 ---')
    '---'
    '---'