# app.py
import streamlit as st
from config import PRECIO_CAJILLA, MARGEN_BRUTO_DEF
from utils.helpers import monto
from utils.data_loader import load_res
from utils.styles import CSS
import views.informe_resultados as informe_resultados
import views.pipeline as pipeline

st.set_page_config(
    page_title="DHM Digital Twin",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)

# Cargar datos
_c = load_res("1_clientes_segmentados.csv")
_p = load_res("2_prediccion_demanda_prophet.csv")
_k = load_res("3_combos_apriori.csv")
_a = load_res("4_anomalias_detectadas.csv")

# Importar vistas
from views import home, pipeline, kmeans, prophet, apriori, isolation_forest, what_if, equations
from views import ai_agent, instacart_presentation, pipeline_data, costo_beneficio

# --- SIDEBAR TECNOLÓGICO ---
with st.sidebar:
    # Logo/HUD Header
    st.markdown(
        "<div style='text-align: left; padding: 10px 0 20px 0; border-bottom: 1px solid rgba(6, 182, 212, 0.3);'>"
        "<div style='font-family: Share Tech Mono; color: #06b6d4; font-size: 12px; letter-spacing: 2px;'>SYS.INIT v4.0</div>"
        "<h2 style='color: #e6edf3; margin: 5px 0 0 0; font-size: 24px; font-family: Rajdhani; font-weight: 700;'>DHM // TWIN</h2>"
        "<p style='color: #8b949e; font-size: 11px; margin-top: 5px; font-family: Share Tech Mono;'>NODE: INSTACART_ALGORITHMS</p>"
        "</div>",
        unsafe_allow_html=True
    )

    # Navegación
    opciones = {
        "[ H ] Inicio": home.show,
        "[ AI ] Asistente": ai_agent.show,
        "[ C ] Caso Instacart": instacart_presentation.show,
        "[ E ] Pipeline ETL": pipeline_data.show,
        "[ P ] Pipeline Básico": pipeline.show,
        "[ I ] Informe de Resultados": informe_resultados.show,
        "[ $ ] Costo-Beneficio": costo_beneficio.show,
        "[ K ] K-Means": kmeans.show,
        "[ F ] Prophet": prophet.show,
        "[ A ] Apriori": apriori.show,
        "[ I ] Isolation Forest": isolation_forest.show,
        "[ W ] What-If": what_if.show,
        "[ M ] Ecuaciones": equations.show,
    }
    
    page = st.radio("NAVEGACIÓN", list(opciones.keys()), label_visibility="collapsed")
    
    st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)

    # Footer del sidebar
    st.markdown(
        "<div style='text-align: center; color: #484f58; font-size: 9px; margin-top: 30px; font-family: Share Tech Mono;'>"
        "AWAITING_INPUT...<br>SECURE_CONNECTION"
        "</div>",
        unsafe_allow_html=True
    )

# --- RENDERIZADO DE LA VISTA ---
opciones[page]()

# --- FOOTER PRINCIPAL ---
st.markdown("---")
st.markdown(
    "<div class='mono' style='text-align:center;padding:16px 0; color: #484f58;'>"
    "DHM DIGITAL TWIN // DATA ANALYTICS LIFECYCLE // SECURE NODE"
    "</div>",
    unsafe_allow_html=True,
)