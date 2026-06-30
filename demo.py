import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

sns.set_theme(style="whitegrid", palette="muted")

st.set_page_config(page_title="Dashboard de Residuos Municipales", page_icon="♻️", layout="wide")

# Datos
@st.cache_data
def cargar_datos():
    df = pd.read_csv(
        "residuos_municipales.csv",
        encoding="latin1", sep=";"
    )
    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].str.strip().str.upper()
    df["DEPARTAMENTO"] = df["DEPARTAMENTO"].replace({
        "APURIMAC": "APURÍMAC", "HUANUCO": "HUÁNUCO",
        "JUNIN": "JUNÍN", "SAN MARTIN": "SAN MARTÍN", "ANCASH": "ÁNCASH"
    })
    df["PERIODO"] = pd.to_numeric(df["PERIODO"], errors="coerce")
    return df

COORDS = {
    "AMAZONAS": (-6.23, -77.87), "ÁNCASH": (-9.53, -77.52),
    "APURÍMAC": (-14.05, -73.08), "AREQUIPA": (-16.41, -71.54),
    "AYACUCHO": (-13.16, -74.22), "CAJAMARCA": (-7.16, -78.51),
    "CALLAO": (-12.05, -77.12), "CUSCO": (-13.53, -71.97),
    "HUANCAVELICA": (-12.78, -74.97), "HUÁNUCO": (-9.93, -76.24),
    "ICA": (-14.07, -75.73), "JUNÍN": (-11.99, -75.00),
    "LA LIBERTAD": (-8.11, -78.02), "LAMBAYEQUE": (-6.70, -79.91),
    "LIMA": (-12.04, -77.03), "LORETO": (-4.00, -75.00),
    "MADRE DE DIOS": (-11.60, -70.80), "MOQUEGUA": (-17.19, -70.93),
    "PASCO": (-10.68, -75.72), "PIURA": (-5.19, -80.62),
    "PUNO": (-15.84, -70.02), "SAN MARTÍN": (-6.94, -76.36),
    "TACNA": (-18.01, -70.25), "TUMBES": (-3.57, -80.45),
    "UCAYALI": (-8.38, -74.55)
}

df = cargar_datos()

# Título
st.title("♻️ Dashboard de Residuos Municipales en el Perú")
st.write("Análisis visual sobre generación de residuos, población y regiones naturales.")

st.subheader("🔎 Filtros del dashboard")

# filtros 
anio_min = int(df["PERIODO"].min())
anio_max = int(df["PERIODO"].max())

rango_anios = st.slider(
    "Rango de años",
    anio_min, anio_max,
    (anio_min, anio_max)
)

anio_inicio = rango_anios[0]
anio_fin = rango_anios[1]
df_filtrado = df[
    (df["PERIODO"] >= anio_inicio) &
    (df["PERIODO"] <= anio_fin)
]

col_departamento, col_provincia, col_distrito = st.columns(3)

departamentos = ["Todos"] + sorted(df["DEPARTAMENTO"].dropna().unique())
with col_departamento:
    departamento_seleccionado = st.selectbox("Departamento", departamentos)

if departamento_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["DEPARTAMENTO"] == departamento_seleccionado]

provincias = ["Todos"] + sorted(df_filtrado["PROVINCIA"].dropna().unique())
with col_provincia:
    provincia_seleccionada = st.selectbox("Provincia", provincias)

if provincia_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado["PROVINCIA"] == provincia_seleccionada]

distritos = ["Todos"] + sorted(df_filtrado["DISTRITO"].dropna().unique())
with col_distrito:
    distrito_seleccionado = st.selectbox("Distrito", distritos)

if distrito_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado["DISTRITO"] == distrito_seleccionado]

st.markdown("---")

# Tabs
inicio, evolucion, tipos, region_tab, gpc_tab, mapa_tab = st.tabs([
    "🏠 Inicio",
    "📈 Residuos por año",
    "🏘️ Tipos de residuos",
    "🌎 Residuos por región",
    "📊 GPC promedio",
    "📍 Mapa"
])

# Tab1-inicio
with inicio:
    st.header("🏠 Introducción")
    st.write("""
    Debido al crecimiento de la población, la expansión urbana y los cambios
    en los hábitos de consumo, la generación de residuos se ha convertido en una 
    problemática grave en el Perú. 
    Cada año, las ciudades producen grandes cantidades de residuos que deben ser 
    recolectados, transportados y tratados adecuadamente.
    """)
    st.write("""
    Cuando la gestión de residuos no es eficiente, recae en problemas como la
    contaminación del suelo, acumulación de basura y afectación a la salud pública. 
    Por ello, analizar estos datos contribuye a una concientización y permite comprender 
    mejor sobre cómo se distribuyen los residuos según el año, departamento y población.
    """)
    st.write("🎯 **Objetivo:** Visualizar la generación de residuos municipales mediante gráficos hechos con Matplotlib y Seaborn.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Años analizados", f"{rango_anios[0]} - {rango_anios[1]}")
    with col2:
        st.metric("Registros filtrados", len(df_filtrado))
    with col3:
        st.metric("Distrito seleccionado", distrito_seleccionado)

    st.divider()

    img1, img2, img3 = st.columns(3)
    with img1:
        st.image("https://images.unsplash.com/photo-1532996122724-e3c354a0b15b?auto=format&fit=crop&w=800&q=80", caption="Reciclaje y residuos")
    with img2:
        st.image("https://images.unsplash.com/photo-1604187351574-c75ca79f5807?auto=format&fit=crop&w=800&q=80", caption="Gestión ambiental")
    with img3:
        st.image("https://images.unsplash.com/photo-1611284446314-60a58ac0deb9?auto=format&fit=crop&w=800&q=80", caption="Tipos de residuos")

    st.divider()
    st.subheader("📌 Gráficos de análisis")
    st.write("""
    - 📈 **Residuos municipales por año:** Evolución de residuos en el tiempo.    
    - 🏘️ **Tipos de residuos:** Porcentaje de residuos domiciliarios vs no domiciliarios.  
    - 🌎 **Residuos por región natural:** Porcentaje de residuos municipales según región.  
    - 📊 **GPC doméstico promedio:** Generación per cápita de residuos domiciliarios.
    - 📍 **Mapa:** Densidad de residuos por departamento en el Perú.
    """)

# Tab2-Residuos municipales por año (matplotlib con área sombreada)
with evolucion:
    st.header("📈 Residuos municipales por año")
    st.write("Muestra cómo ha cambiado la cantidad total de residuos municipales a lo largo de los años.")

    residuos_anio = df_filtrado.groupby("PERIODO")["QRESIDUOS_MUN"].sum()

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(residuos_anio.index, residuos_anio.values, marker="o", linewidth=2.5,
            color="#2ecc71", markerfacecolor="white", markeredgewidth=2, markersize=7)
    ax.fill_between(residuos_anio.index, residuos_anio.values, alpha=0.15, color="#2ecc71")
    ax.set_title(f"Residuos municipales por año — {departamento_seleccionado}", fontsize=13, fontweight="bold")
    ax.set_xlabel("Año", fontsize=11)
    ax.set_ylabel("Residuos municipales (ton)", fontsize=11)
    ax.grid(True)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# Tab4-Tipos de residuos
with tipos:
    st.header("🏘️ Residuos Domiciliarios vs no Domiciliarios")
    st.write("""
    Este gráfico compara:
    - **Residuos domiciliarios:** generados en los domicilios a nivel distrital.
    - **Residuos no domiciliarios:** generados por las actividades económicas e institucionales y limpieza de espacios públicos, a nivel distrital.
    """)

    total_dom = df_filtrado["QRESIDUOS_DOM"].sum()
    total_no_dom = df_filtrado["QRESIDUOS_NO_DOM"].sum()

    fig3, ax3 = plt.subplots(figsize=(6, 6))
    ax3.pie(
        [total_dom, total_no_dom],
        labels=["Domiciliarios", "No Domiciliarios"],
        autopct="%.2f%%",
        startangle=90,
        colors=["#2ecc71", "#3498db"]
    )
    ax3.set_title("Porcentaje de residuos domiciliarios y no domiciliarios", fontsize=13, fontweight="bold")
    st.pyplot(fig3)
    plt.close(fig3)

# Tab5- Residuos municipales por región natural
with region_tab:
    st.header("🌎 Distribución de residuos municipales por región natural")
    st.write("Muestra qué porcentaje de residuos municipales corresponde a cada región natural.")

    region = df_filtrado.groupby("REG_NAT")["QRESIDUOS_MUN"].sum()

    fig4, ax4 = plt.subplots(figsize=(6, 6))
    ax4.pie(
        region.values,
        labels=region.index,
        autopct="%.2f%%",
        startangle=90,
        colors=sns.color_palette("Set2", len(region))
    )
    ax4.set_title("Distribución de residuos por región natural", fontsize=13, fontweight="bold")
    st.pyplot(fig4)
    plt.close(fig4)

# Tab6-GPC (barras horizontales con seaborn)
with gpc_tab:
    st.header("📊 GPC doméstico promedio")
    st.write("""
    Muestra la generación per cápita (GPC) doméstica promedio por departamento.
    Corresponde a la cantidad de residuos sólidos generados diariamente por habitante (kg/hab/día).
    """)

    gpc = (
        df_filtrado.groupby("DEPARTAMENTO")["GPC_DOM"]
        .mean()
        .sort_values(ascending=True)
        .reset_index()
    )

    fig5, ax5 = plt.subplots(figsize=(8, 5))
    colores = sns.color_palette("Blues_r", len(gpc))
    bars = ax5.barh(gpc["DEPARTAMENTO"], gpc["GPC_DOM"], color=colores)
    ax5.bar_label(bars, fmt="%.3f", padding=3)
    ax5.set_xlabel("GPC doméstico promedio (kg/hab/día)", fontsize=11)
    ax5.set_title("Generación per cápita de residuos domiciliarios", fontsize=13, fontweight="bold")
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close(fig5)

# Tab7- Mapa
with mapa_tab:
    st.header("📍 ¿Dónde se generan más residuos?")
    st.write("Mayor densidad de puntos = más residuos en ese departamento.")

    df_mapa = (
        df_filtrado.groupby("DEPARTAMENTO")["QRESIDUOS_MUN"]
        .sum().reset_index()
    )
    df_mapa["lat"] = df_mapa["DEPARTAMENTO"].map(lambda d: COORDS.get(d, (0, 0))[0])
    df_mapa["lon"] = df_mapa["DEPARTAMENTO"].map(lambda d: COORDS.get(d, (0, 0))[1])
    df_mapa = df_mapa[df_mapa["lat"] != 0]

    if not df_mapa.empty:
        minv, maxv = df_mapa["QRESIDUOS_MUN"].min(), df_mapa["QRESIDUOS_MUN"].max()
        df_mapa["reps"] = (((df_mapa["QRESIDUOS_MUN"] - minv) / (maxv - minv + 1) * 79 + 1)).astype(int)

        filas = []
        for _, row in df_mapa.iterrows():
            for _ in range(row["reps"]):
                filas.append({
                    "lat": row["lat"] + np.random.uniform(-0.4, 0.4),
                    "lon": row["lon"] + np.random.uniform(-0.4, 0.4),
                })
        st.map(pd.DataFrame(filas))
        st.caption("Puntos generados proporcionalmente a los residuos según filtros aplicados.")
    else:
        st.info("No hay datos para mostrar en el mapa con los filtros actuales.")

st.divider()
st.write("📊 Fuente: [Datos Abiertos del Perú](https://www.datosabiertos.gob.pe) · Hecho con **Streamlit**")
