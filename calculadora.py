import streamlit as st
import pandas as pd
import numpy as np

col1, col2 = st.columns([3, 1])
with col1:
    st.title('CALCULADORA DE PRIMA TOTAL PARA UN SEGURO DE AUTOS')
with col2:
    url_imagen = "https://images.vexels.com/media/users/3/258908/isolated/preview/405070adc9b39a8331bb7d0a6a08a905-transporte-de-coche-deportivo-rojo.png"
    st.image(url_imagen, width=400)


st.text('Para el calculo de la prima total para un seguro de auto tomamos en cuenta cuatro datos proporcionados por el cliente, el deducible de daños materiales, el deducible de robo total, la suma asegurada de responsabilidad civil y la suma asegurada de gastos médicos.')

pb_dm = 4300/.90
pb_rt = 2500/1.05

# los posibles deducibles que el asegurado puede elegir segun la cobertura

deducibles_DM = ["2%", "4%","5%", "6%", "8%"] # daños materiales
deducibles_RT = ["6%", "8%","10%", "12%", "14%"] # robo total
ajuste = [.10, .05, .0, -.05, -.10] # el ajuste a la prima base segun el deducible

df_primaDM = pd.DataFrame({'DEDUCIBLE' : deducibles_DM, # DataFrame de daños materiales
                           'AJUSTE' : ajuste })
df_primaDM['PRIMA'] = pb_dm * (1 + df_primaDM['AJUSTE']) # Columna de la prima segun el deducible

df_primaRT = pd.DataFrame({'DEDUCIBLE' : deducibles_RT, # DataFrame de robo total
                           'AJUSTE' : ajuste })

df_primaRT['PRIMA'] = pb_rt * (1 + df_primaRT['AJUSTE']) # Columna de la prima segun el deducible

print(df_primaRT)
print(df_primaDM)

# funcion para calcular la prima de responsabilidad civil segun la suma asegurada
# SA base es de 500,000 (SA minima)
def prima_res(suma_asegurada_solicitada_rc): # se define la funcion para obtener la prima por la cobertura responsabilidad civil
  pb_respciv = 1200 # prima base de RC
  sa_base_responsacivil = 500000 # suma asegurada base de RC
  exceso = 50000 # Exceso de SA

  x = ((suma_asegurada_solicitada_rc - sa_base_responsacivil)/ exceso) * 50 # x nos da la prima extra que le cobraremos por el exceso de la sa base
  prima_total = pb_respciv + x
  return prima_total

# funcion para calcular la prima de gastos medicos segun la suma asegurada
# SA base es de 100,000 (SA minima)
def prima_gasm(suma_asegurada_solicitada_gm): # se define la funcion para obtener la prima por la cobertura responsabilidad civil
  pb_gm = 400 # prima base de RC
  sa_base_gastosm = 100000 # suma asegurada base de RC
  exceso = 10000 # Exceso de SA

  x = ((suma_asegurada_solicitada_gm - sa_base_gastosm)/ exceso) * 20 # x nos da la prima extra que le cobraremos por el exceso de la sa base
  prima_total = pb_gm + x
  return prima_total


# REPLICAMOS EL EJERCICIO EN CLASE
deducible_seleccionado_dm = st.selectbox('Selecciona el deducible de DAÑOS MATERIALES:', deducibles_DM) # seleccionamos el deducible de daños materiales
prima_dm = df_primaDM.loc[df_primaDM['DEDUCIBLE'] == deducible_seleccionado_dm, "PRIMA"].values[0] # el valor que se cambia aqui es el 4% segun el deducible que se quiera

deducible_seleccionado_rt = st.selectbox('Selecciona el deducible de ROBO TOTAL:', deducibles_RT) # seleccionamos el deducible de robo total
prima_rt = df_primaRT.loc[df_primaRT['DEDUCIBLE'] == deducible_seleccionado_rt, "PRIMA"].values[0] # el valor que se cambia aqui es el 14% segun el deducible que se quiera

SA_rc = [500000,550000,600000,650000,700000,750000,800000,850000,900000,950000,1000000] # Sumas aseguradas de responsabilidad civil
suma_asegurada_seleccionada_rc = st.selectbox('Selecciona la suma que quieres asegfurar para RESPONSABILIDAD CIVIL:', SA_rc) # seleccionamos la suma asegurada de responsabilidad civil
suma_asegurada_solicitada_rc = suma_asegurada_seleccionada_rc #ejemplo, debe ser la prima base de 500,000 + multimplos de 50,000
# el valor que cambia aqui son los 600000 segun la SA que se requiera
prima_rc = prima_res(suma_asegurada_solicitada_rc)

SA_rc = [100000,110000,120000,130000,140000,150000,160000,170000,180000,190000,200000] # Sumas aseguradas de responsabilidad civil
suma_asegurada_seleccionada_gm = st.selectbox('Selecciona la suma que quieres asegurar para GASTOS MÉDICOS:', SA_rc) # seleccionamos la suma asegurada de responsabilidad civil
suma_asegurada_solicitada_gm = suma_asegurada_seleccionada_gm #ejemplo, debe ser la prima base de 100,000 + multimplos de 50,000
# el valor que cambia aqui son los 150000 segun la SA que se requiera
prima_gm = prima_gasm(suma_asegurada_solicitada_gm)

if st.button("CALCULA LA PRIMA TOTAL"): # Boton para calcular la prima
    prima_total = float(prima_dm + prima_rt + prima_rc + prima_gm) # SUMA DE TODAS LAS PRIMAS
    st.success(f'La prima total es: ${prima_total}') # imprime la prima total

#print(prima_total)
