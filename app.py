print("\n⏱️  [1/4] Cargando herramientas pesadas (Pandas, Dash, Plotly)... Espera unos segundos.")

import dash
from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests

print("✅ [2/4] Librerías cargadas con éxito.")
print("⏳ [3/4] Leyendo 'mortalidad_limpia.csv' (Procesando registros)...")

# 1. Inicializar la app con el estilo LUX
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
server = app.server 

# 2. Cargar los datos limpios
df = pd.read_csv('mortalidad_limpia.csv', low_memory=False)
print(f"✅ Datos listos para graficar. Total filas: {len(df)}")

print("⏳ [4/4] Construyendo las 7 visualizaciones obligatorias...")

# --- ELEMENTO 1: MAPA DE DEPARTAMENTOS ---
dept_clean_map = {
    '5': 'ANTIOQUIA', '05': 'ANTIOQUIA', 'ANTIOQUIA': 'ANTIOQUIA',
    '8': 'ATLANTICO', '08': 'ATLANTICO', 'ATLANTICO': 'ATLANTICO', 'ATLÁNTICO': 'ATLANTICO',
    '11': 'BOGOTA', 'BOGOTA': 'BOGOTA', 'BOGOTÁ': 'BOGOTA', 'BOGOTA D.C.': 'BOGOTA', 'BOGOTÁ, D.C.': 'BOGOTA', 'BOGOTA, D.C.': 'BOGOTA',
    '13': 'BOLIVAR', 'BOLIVAR': 'BOLIVAR', 'BOLÍVAR': 'BOLIVAR',
    '15': 'BOYACA', 'BOYACA': 'BOYACA', 'BOYACÁ': 'BOYACA',
    '17': 'CALDAS', 'CALDAS': 'CALDAS',
    '18': 'CAQUETA', 'CAQUETA': 'CAQUETA', 'CAQUETÁ': 'CAQUETA',
    '19': 'CAUCA', 'CAUCA': 'CAUCA',
    '20': 'CESAR', 'CESAR': 'CESAR',
    '23': 'CORDOBA', 'CORDOBA': 'CORDOBA', 'CÓRDOBA': 'CORDOBA',
    '25': 'CUNDINAMARCA', 'CUNDINAMARCA': 'CUNDINAMARCA',
    '27': 'CHOCO', 'CHOCO': 'CHOCO', 'CHOCÓ': 'CHOCO',
    '41': 'HUILA', 'HUILA': 'HUILA',
    '44': 'LA GUAJIRA', 'LA GUAJIRA': 'LA GUAJIRA', 'GUAJIRA': 'LA GUAJIRA',
    '47': 'MAGDALENA', 'MAGDALENA': 'MAGDALENA',
    '50': 'META', 'META': 'META',
    '52': 'NARINO', 'NARINO': 'NARINO', 'NARIÑO': 'NARINO',
    '54': 'NORTE DE SANTANDER', 'NORTE DE SANTANDER': 'NORTE DE SANTANDER',
    '63': 'QUINDIO', 'QUINDIO': 'QUINDIO', 'QUINDÍO': 'QUINDIO',
    '66': 'RISARALDA', 'RISARALDA': 'RISARALDA',
    '68': 'SANTANDER', 'SANTANDER': 'SANTANDER',
    '70': 'SUCRE', 'SUCRE': 'SUCRE',
    '73': 'TOLIMA', 'TOLIMA': 'TOLIMA',
    '76': 'VALLE DEL CAUCA', 'VALLE DEL CAUCA': 'VALLE DEL CAUCA', 'VALLE': 'VALLE DEL CAUCA',
    '81': 'ARAUCA', 'ARAUCA': 'ARAUCA',
    '85': 'CASANARE', 'CASANARE': 'CASANARE',
    '86': 'PUTUMAYO', 'PUTUMAYO': 'PUTUMAYO',
    '88': 'SAN ANDRES', 'SAN ANDRES': 'SAN ANDRES', 'SAN ANDRÉS': 'SAN ANDRES',
    '91': 'AMAZONAS', 'AMAZONAS': 'AMAZONAS',
    '94': 'GUAINIA', 'GUAINIA': 'GUAINIA', 'GUAINÍA': 'GUAINIA',
    '95': 'GUAVIARE', 'GUAVIARE': 'GUAVIARE',
    '97': 'VAUPES', 'VAUPES': 'VAUPES', 'VAUPÉS': 'VAUPES',
    '99': 'VICHADA', 'VICHADA': 'VICHADA'
}

def normalizar_departamento(x):
    s = str(x).strip().split('.')[0].upper()
    return dept_clean_map.get(s, s)

df_dept = df.groupby('DEPARTAMENTO').size().reset_index(name='TOTAL_MUERTES')
df_dept['DEPT_MATCH'] = df_dept['DEPARTAMENTO'].apply(normalizar_departamento)

geojson_url = "https://raw.githubusercontent.com/mancera/colombia-geojson/master/colombia.geo.json"

try:
    response = requests.get(geojson_url, timeout=10)
    colombia_geojson = response.json()
    
    fig_mapa = px.choropleth_mapbox(
        df_dept,
        geojson=colombia_geojson,
        locations='DEPT_MATCH',
        featureidkey='properties.NOMBRE_DPT',
        color='TOTAL_MUERTES',
        color_continuous_scale='YlOrRd',
        mapbox_style="carto-positron",
        center={"lat": 4.5709, "lon": -74.2973},
        zoom=4.2,
        labels={'TOTAL_MUERTES': 'Fallecidos', 'DEPT_MATCH': 'Departamento'}
    )
    fig_mapa.update_layout(title="Distribución Total de Muertes por Departamento", margin={"r":0,"t":40,"l":0,"b":0})
except Exception as e:
    df_dept_sorted = df_dept.sort_values(by='TOTAL_MUERTES', ascending=True)
    fig_mapa = px.bar(df_dept_sorted, x='TOTAL_MUERTES', y='DEPT_MATCH', orientation='h', title="Muertes por Departamento (Vista Lista)", color='TOTAL_MUERTES', color_continuous_scale='YlOrRd')

# --- ELEMENTO 2: GRÁFICO DE LÍNEAS ---
df_mes = df.groupby('MES').size().reset_index(name='TOTAL_MUERTES')
fig_lineas = px.line(
    df_mes, x='MES', y='TOTAL_MUERTES', 
    title='Variación de Muertes a lo Largo del Año', markers=True,
    labels={'MES': 'Mes del Año', 'TOTAL_MUERTES': 'Número de Fallecidos'}
)
fig_lineas.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1))

# --- ELEMENTO 3: GRÁFICO DE BARRAS (Homicidios X95) ---
df_homicidios = df[df['COD_MUERTE'].astype(str).str.contains('X95', na=False)]
if not df_homicidios.empty:
    df_ciudades_v = df_homicidios.groupby('MUNICIPIO').size().reset_index(name='HOMICIDIOS')
    df_top5_ciudades = df_ciudades_v.nlargest(5, 'HOMICIDIOS')
    fig_barras_violencia = px.bar(
        df_top5_ciudades, x='MUNICIPIO', y='HOMICIDIOS', 
        title='Top 5 Ciudades Más Violentas (Homicidios X95)',
        color='HOMICIDIOS', color_continuous_scale='Reds',
        labels={'MUNICIPIO': 'Municipio', 'HOMICIDIOS': 'Casos Registrados'}
    )
else:
    fig_barras_violencia = px.scatter(title="Alerta: No se encontraron códigos X95")

# --- ELEMENTO 4: GRÁFICO CIRCULAR ---
df_ciudades_m = df.groupby('MUNICIPIO').size().reset_index(name='TOTAL')
df_menor_mortalidad = df_ciudades_m.nsmallest(10, 'TOTAL')
fig_circular = px.pie(
    df_menor_mortalidad, values='TOTAL', names='MUNICIPIO',
    title='Top 10 Ciudades con Menor Índice de Mortalidad', hole=0.3
)

# --- ELEMENTO 5: TABLA INTERACTIVA (CORREGIDA CON DICCIONARIO SEGURO DANE/CIE-10) ---
top10_series = df['COD_MUERTE'].value_counts().head(10)

# Diccionario oficial de traducción de los códigos CIE-10 reflejados en tus datos
cie10_colombia_map = {
    'I219': 'Infarto agudo de miocardio, sin otra especificación',
    'J449': 'Enfermedad pulmonar obstructiva crónica (EPOC)',
    'J440': 'EPOC con infección aguda de vías respiratorias inferiores',
    'J189': 'Neumonía, no especificada',
    'C169': 'Tumor maligno del estómago',
    'C349': 'Tumor maligno de los bronquios o del pulmón',
    'X954': 'Agresión (Homicidio) con disparo de arma de fuego',
    'C509': 'Tumor maligno de la mama',
    'C61':  'Tumor maligno de la próstata',
    'I10':  'Hipertensión esencial (primaria)'
}

# Vinculamos las descripciones de manera segura limpiando los códigos
nombres_lista = [cie10_colombia_map.get(str(cod).strip().upper(), 'Otras causas de alta incidencia') for cod in top10_series.index]

df_tabla_render = pd.DataFrame({
    'Código': top10_series.index,
    'Causa de Muerte': nombres_lista,
    'Total Casos': top10_series.values
})

# --- ELEMENTO 6: BARRAS APILADAS ---
df_sexo_dept = df.groupby(['DEPARTAMENTO', 'SEXO']).size().reset_index(name='TOTAL')
fig_barras_apiladas = px.bar(
    df_sexo_dept, x='DEPARTAMENTO', y='TOTAL', color='SEXO',
    title='Comparación de Muertes por Sexo en cada Departamento', barmode='stack',
    color_discrete_map={'MASCULINO': '#3498db', 'FEMENINO': '#e74c3c', 'INDETERMINADO': '#95a5a6'},
    labels={'DEPARTAMENTO': 'Departamento', 'TOTAL': 'Total Casos', 'SEXO': 'Género'}
)

# --- ELEMENTO 7: HISTOGRAMA ---
orden_ciclo = [
    "Mortalidad neonatal", "Mortalidad infantil", "Primera infancia", 
    "Niñez", "Adolescencia", "Juventud", "Adultez temprana", 
    "Adultez intermedia", "Vejez", "Longevidad / Centenarios", "Edad desconocida"
]
df_ciclo = df.groupby('CICLO_VIDA').size().reset_index(name='TOTAL')
fig_histograma = px.bar(
    df_ciclo, x='CICLO_VIDA', y='TOTAL',
    title='Distribución de Mortalidad según Ciclo de Vida (DANE)',
    category_orders={'CICLO_VIDA': orden_ciclo},
    color='TOTAL', color_continuous_scale='Blues',
    labels={'CICLO_VIDA': 'Etapa de Vida', 'TOTAL': 'Número de Casos'}
)

print("✅ Todos los elementos visuales estructurados con éxito.")

# 3. DISEÑO VISUAL DE LA INTERFAZ
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Tablero de Análisis de Mortalidad en Colombia (2019)", className="text-center my-4 text-primary font-weight-bold"), width=12)
    ]),
    
    html.Hr(),
    
    dbc.Row([
        dbc.Col([
            html.H5("Análisis Geográfico Nacional", className="text-muted mb-2"),
            dcc.Graph(id='grafico-mapa', figure=fig_mapa)
        ], md=6),
        dbc.Col([
            html.H5("Distribución Demográfica", className="text-muted mb-2"),
            dcc.Graph(id='grafico-histograma', figure=fig_histograma)
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H5("Evolución Cronológica", className="text-muted mb-2"),
            dcc.Graph(id='grafico-lineas', figure=fig_lineas)
        ], md=6),
        dbc.Col([
            html.H5("Indicadores de Violencia Urbana", className="text-muted mb-2"),
            dcc.Graph(id='grafico-barras-v', figure=fig_barras_violencia)
        ], md=6)
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H5("Zonas de Menor Impacto", className="text-muted mb-2"),
            dcc.Graph(id='grafico-circular', figure=fig_circular)
        ], md=5),
        dbc.Col([
            html.H5("Brecha de Género por Región", className="text-muted mb-2"),
            dcc.Graph(id='grafico-apilado', figure=fig_barras_apiladas)
        ], md=7)
    ], className="mb-4"),
    
    html.Hr(),
    
    dbc.Row([
        dbc.Col([
            html.H3("Listado de las 10 Principales Causas de Muerte en Colombia", className="text-secondary mb-3 text-center"),
            dash_table.DataTable(
                id='tabla-causas',
                columns=[{"name": i, "id": i} for i in df_tabla_render.columns],
                data=df_tabla_render.to_dict('records'),
                style_table={'overflowX': 'auto', 'border': '1px solid #e0e0e0'},
                style_header={
                    'backgroundColor': '#2c3e50', 
                    'color': 'white', 
                    'fontWeight': 'bold', 
                    'textAlign': 'center'
                },
                style_data={
                    'backgroundColor': '#ffffff',
                    'color': '#2c3e50'
                },
                style_cell={
                    'textAlign': 'left', 
                    'padding': '12px', 
                    'fontFamily': 'sans-serif', 
                    'fontSize': '14px'
                },
                style_data_conditional=[{
                    'if': {'row_index': 'odd'},
                    'backgroundColor': '#f9f9f9',
                    'color': '#2c3e50'
                }],
                page_size=10
            )
        ], width=12)
    ], className="mb-5")
    
], fluid=True)

print("\n⚙️  ¡Servidor Web Encendido con Éxito! Disfruta del tablero completo.")
if __name__ == '__main__':
    app.run(debug=True)