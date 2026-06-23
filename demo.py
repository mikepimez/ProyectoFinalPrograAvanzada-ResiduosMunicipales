import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

# Estilo global seaborn
sns.set_theme(style="whitegrid", palette="muted")

st.set_page_config(page_title="Residuos Municipales Perú", page_icon="🗑️", layout="wide")

# ── Datos ────────────────────────────────────────────────────────────────────
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

# ════════════════════════════════════════════════════════════════════════════
# TÍTULO
# ════════════════════════════════════════════════════════════════════════════
st.title("🗑️ Residuos Municipales en el Perú")
st.write(
    "Análisis interactivo de la generación de residuos municipales "
    "a nivel distrital entre **2014 y 2024**. "
    "Datos del Portal de Datos Abiertos del Gobierno Peruano."
)

st.divider()

# ════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — Evolución temporal (gráfico principal — matplotlib)
# ════════════════════════════════════════════════════════════════════════════
st.header("📈 ¿Cómo ha evolucionado la generación de residuos?")
st.write("Elige un departamento y mira cómo cambió la cantidad de residuos municipales año a año.")

dept_principal = st.selectbox(
    "Departamento:",
    options=sorted(df["DEPARTAMENTO"].unique()),
    index=sorted(df["DEPARTAMENTO"].unique()).index("LIMA")
)

df_p = (
    df[df["DEPARTAMENTO"] == dept_principal]
    .groupby("PERIODO")["QRESIDUOS_MUN"]
    .sum()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(10, 4))
ax1.plot(df_p["PERIODO"], df_p["QRESIDUOS_MUN"], marker="o", linewidth=2.5,
         color="#2ecc71", markerfacecolor="white", markeredgewidth=2, markersize=7)
ax1.fill_between(df_p["PERIODO"], df_p["QRESIDUOS_MUN"], alpha=0.15, color="#2ecc71")
ax1.set_xlabel("Año", fontsize=11)
ax1.set_ylabel("Cantidad de residuos municipales (ton)", fontsize=11)
ax1.set_title(f"Evolución de residuos municipales — {dept_principal}", fontsize=13, fontweight="bold")
ax1.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
plt.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

st.divider()
