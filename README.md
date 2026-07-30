Autor: Gerardo Figueroa Fecha: 29/07/26
# 📦 SQL Simulador MRP e Inventario - Efecto Látigo
Una aplicación web interactiva desarrollada con Streamlit y Supabase (PostgreSQL) diseñada para simular la Planificación de Requerimientos de Materiales (MRP), analizar la estructura de productos (BOM) y estimar el impacto del efecto látigo (Bullwhip Effect) en la cadena de suministro.

## 🌟 Características Principales (Features)
Conexión a Base de Datos en Tiempo Real: Integración mediante API-REST con Supabase BD SQL Postgresql para recuperar los registros de inventario y la estructura de productos (BOM).

Parámetros de Simulación Dinámicos: Panel lateral con selectores interactivos para elegir el producto (UPC), la semana de análisis y el volumen de producción deseado.

Cálculo Automático de Requerimientos: Cruce de datos relacionales para calcular de forma inmediata los pedidos necesarios por componente y detectar posibles faltantes en la fábrica.

Sistema de Alertas Inteligentes: Notificaciones visuales en tiempo real sobre el estatus del stock (desabasto vs. inventario suficiente).

Análisis del Efecto Látigo: Herramienta conceptual integrada para evaluar la amplificación de la demanda a lo largo de los niveles de la cadena de suministro.

## 🏗️ Estructura del Proyecto
El repositorio cuenta con una distribución modular que separa el código de la interfaz de la lógica de negocio, las simulaciones matemáticas y el análisis en cuadernos de ciencia de datos:Plaintext.

```text
.
├── images/
│   ├── img_planta.png                   # Identidad visual de la planta manufacturera
│   └── logo_verde.png                   # Logotipo corporativo para el panel lateral
├── app.py                               # Orquestador e interfaz principal de Streamlit
├── inventario.csv                       # Datos del inventario actual de la planta y sus proveedores
├── estructura_upc.csv                   # Set de datos con de las estructura de productos 
└── requirements.txt                     # Dependencias empaquetadas del entorno de ejecución
´´´´

## 🛠️ Tecnologías Principales
Python (Lenguaje base)

Streamlit (Framework para la interfaz web interactiva)

Pandas & NumPy (Manipulación, limpieza y análisis de datos)

Supabase / SQL PostgreSQL (Backend as a Service / Motor de base de datos relacional)

## 🚀 Guía de Instalación y Configuración Local (Getting Started)
⚙️ Pasos para Clonar e Instalar
Abre tu terminal y ejecuta los siguientes comandos:

Bash
1. Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]
cd [NOMBRE_DEL_DIRECTORIO]

2. Crear y activar un entorno virtual (Recomendado)
python -m venv venv
En Windows:
venv\Scripts\activate
3. Instalar las dependencias del proyecto
pip install streamlit pandas numpy supabase

## ▶️ Instrucciones de Uso (Cómo Ejecutarlo)
Una vez completada la instalación y configuración de las credenciales, inicia la aplicación ejecutando el siguiente comando en la terminal:

Bash
streamlit run app.py
