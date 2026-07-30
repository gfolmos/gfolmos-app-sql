# Ejemplo scm efecto latigo (bom)
# Autor: Gerardo Figueroa
# Fecha: 27/07/26
import numpy as np
import pandas as pd
import streamlit as st
from supabase import create_client, Client

url: str = "https://cvduaagsbsxjknebpdtb.supabase.co"
key: str = st.secrets["SUPEBASE_API_KEY"]


# Inicializar cliente de Supabase
supabase: Client = create_client(url, key)

# Configuración inicial de la página
st.set_page_config(
    page_title="Simulador MRP e Inventario - Efecto Látigo",
    page_icon="📦",
    layout="wide",
)

def load_data():
    """Lee los datos directamente desde las tablas de Supabase y los convierte a DataFrames."""
    
    # 1. Obtener datos de la tabla inventario
    response_inv = supabase.table("inventario").select("*").execute()
    df_inv = pd.DataFrame(response_inv.data)
    
    # 2. Obtener datos de la tabla estructura_upc
    response_u = supabase.table("estructura_upc").select("*").execute()
    df_u = pd.DataFrame(response_u.data)
    
    return df_inv, df_u

# Llamada a la función respetando tus nombres de variables originales
df_inventario, df_upc = load_data()

#""" cargar solo archivos csv, para no depender de la base de datos supabase
# Cargar los archivos CSV
#@st.cache_data
#def load_data():
#  df_inv = pd.read_csv("inventario.csv")
#  df_u = pd.read_csv("estructura_upc.csv")
#  return df_inv, df_u
#df_inventario, df_upc = load_data()
#"""

# ==========================================
# A.- PANEL LATERAL (SIDEBAR)
# ==========================================
st.sidebar.image("images/logo_verde.png") #, width=120)
st.sidebar.header("⚙️ Parámetros de Simulación")

# 1. Selectbox para elegir UPC
upcs_disponibles = df_upc["upc"].unique()
upc_seleccionado = st.sidebar.selectbox(
    "Selecciona el UPC / Producto Final:", upcs_disponibles
)

# Filtrar df_upc con el producto seleccionado
df_upc_filtrado = df_upc[df_upc["upc"] == upc_seleccionado].copy()

# 2. Slider para elegir número de semana (hasta 52)
semana_seleccionada = st.sidebar.slider(
    "Selecciona la Semana:", min_value=1, max_value=52, value=1
)

# 3. Slider para elegir la cantidad_seleccionada (hasta 500 piezas)
cantidad_seleccionada = st.sidebar.slider(
    "Cantidad de UPCs a Producir (Piezas):",
    min_value=1,
    max_value=1500,
    value=50,
)


# ==========================================
# B.- PÁGINA PRINCIPAL
# ==========================================
col1, col2 = st.columns([1, 2])  # proporción: más espacio para el título
with col1:
    st.image("images/img_planta.png", width=150)
with col2:
    st.header("🏭SQL Busqueda de Requerimientos de Materiales e Inventario (BOM)")
    st.write("Utiliza API-REST para conectarce a BD PostgreSQL como motor de busqueda")
# Explicacion del programa
with st.expander("Explicación del Programa"):
    st.write("""
            Analiza los datos de requisición de inventarios, al generarse una orden de producción, se generaría una orden de requisión de materiales.
            Es este simulador se analiza la estructura del producto (BOM) y el inventario disponible en la fábrica, para determinar si es posible cumplir 
            con la orden de producción solicitada. Al seleccionar el producto, la semana y la posible producción, el resultado muestra la disponibilidad
            del almacen para surtir la orden. Al incluir algunas existencias, podriamos estimar el el efecto látigo (bullwhip effect) con la siguiente
            formula: BWE = (demanda_cliente_final) / (pedido_fabrica_a_proveedor) contenidas en el dataframe origial. 
             """)
    
#*****
#st.title("🏭 Dashboard de Requerimientos de Materiales e Inventario")
st.markdown(
    f"**Producto:** `{upc_seleccionado}` | **Semana:** `{semana_seleccionada}` |"
    f" **Orden:** `{cantidad_seleccionada} unidades`"
)

# 1. Expander con la estructura del UPC (filtrado)
with st.expander(
    "📌 Ver Estructura del Producto (Bill of Materials - BOM)", expanded=False
):
  st.dataframe(
      df_upc_filtrado[["upc", "sku", "descripcion", "cantidad"]],
      use_container_width=True,
  )

# 2. Construcción del DataFrame final de análisis
# Filtrar inventario por la semana seleccionada
df_inv_semana = df_inventario[
    df_inventario["semana"] == semana_seleccionada
].copy()

# Unir la estructura del producto filtrada con el inventario de la semana seleccionada
df_resultado = pd.merge(
    df_upc_filtrado[["sku", "cantidad"]],
    df_inv_semana,
    on="sku",
    how="inner",
)

# Cálculo de columnas solicitadas:
# 'pedido' = cantidad_seleccionada * df_upc.cantidad
df_resultado["pedido"] = cantidad_seleccionada * df_resultado["cantidad"]

# 'faltante' = pedido - inventario_fabrica
df_resultado["faltante"] = (
    df_resultado["pedido"] - df_resultado["inventario_fabrica"]
)

# Selección e integración del orden 
columnas_solicitadas = [
    "semana",
    # "fecha_inicio_semana",
    "sku",
    "descripcion",
    # "inventario_retailer",
    "inventario_distribuidor",
    "inventario_fabrica",
    "pedido",
    "faltante",
]

df_final = df_resultado[columnas_solicitadas]

# Mostrar la tabla en la página principal
st.subheader("📋 Estado de Inventario y Requerimientos por Componente")
st.dataframe(df_final, use_container_width=True)

# Alertas dinámicas sobre disponibilidad
componentes_faltantes = df_final[df_final["faltante"] > 0]

if not componentes_faltantes.empty:
  st.error(
      f"⚠️ **Alerta de Desabasto:** Existen {len(componentes_faltantes)}"
      " componentes con faltante en la fábrica para cubrir la orden."
  )
else:
  st.success(
      "✅ **Stock Suficiente:** La fábrica cuenta con inventario necesario"
      " para completar la producción solicitada."
  )