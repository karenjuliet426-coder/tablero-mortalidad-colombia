# Análisis de Mortalidad en Colombia (2019) - Aplicación Web Dinámica

## Introducción del Proyecto
Esta aplicación web interactiva ha sido desarrollada utilizando el lenguaje de programación Python, haciendo uso de las librerías Dash y Plotly. Permite explorar de forma intuitiva los microdatos demográficos y regionales de mortalidad del DANE para el año 2019 en Colombia.

## Objetivo
Transformar datos complejos de estadísticas vitales en representaciones visuales dinámicas para identificar patrones espaciales, tendencias temporales, brechas de género y las principales causas de fallecimiento en el territorio nacional.

## Estructura del Proyecto
- `app.py`: Archivo principal que contiene la lógica de los gráficos y el diseño del tablero web.
- `mortalidad_limpia.csv`: Base de datos optimizada y preprocesada a partir de los microdatos del DANE.
- `Procfile`: Instrucción de arranque para el servidor de producción (Gunicorn).
- `requirements.txt`: Listado de librerías y dependencias necesarias para la ejecución.

## Requisitos y Software Utilizado
- Python 3.10+
- Dash
- Dash Bootstrap Components
- Plotly Express
- Pandas
- Gunicorn (Servidor HTTP WSGI)

## Instalación Local
1. Clonar el repositorio.
2. Instalar dependencias: `pip install -r requirements.txt`
3. Ejecutar la aplicación: `python app.py`
4. Abrir en el navegador: `http://127.0.0.1:8050/`

## Despliegue en la Nube
La aplicación se encuentra desplegada de forma pública en la plataforma como servicio (PaaS) **Render**, asegurando su accesibilidad en línea de manera continua y responsiva.
