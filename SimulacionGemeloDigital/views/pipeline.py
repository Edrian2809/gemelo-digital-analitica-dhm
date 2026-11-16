"""
Vista: Pipeline del Gemelo Digital
Muestra el flujo completo: ETL → Algoritmos → Resultados → Dashboard.
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.ui_components import hero, section, metric_col, callout, plot_dark


# ============================================================
# HELPER: aplica tema oscuro soportando ambos patrones de plot_dark
# ============================================================
def _dark(fig, height=400):
    out = plot_dark(fig, height)
    return out if out is not None else fig


# ============================================================
# ENTRYPOINT
# ============================================================
def show():
    hero(
        badge="⚙️ PIPELINE ANALÍTICO · GEMELO DIGITAL DHM",
        title="Del Dato Crudo al Gemelo Digital",
        subtitle="Arquitectura del flujo analítico: ETL, algoritmos, resultados y visualización",
        refs="Python · Streamlit · scikit-learn · Prophet · mlxtend · Plotly",
    )

    # --- Quick stats ---
    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Etapas", "4", "ETL → Modelos → Resultados → Dashboard", "info")
    metric_col(c2, "Algoritmos", "4", "K-Means · Prophet · Apriori · IF", "ok")
    metric_col(c3, "Archivos de salida", "4", "resultados_ml/*.csv", "warn")
    metric_col(c4, "Integración", "Parcial", "Algoritmos en paralelo", "danger")

    section(1, "Diagrama de Flujo", "Del CSV de entrada al tablero ejecutivo")
    _render_sankey()

    section(2, "Detalle de Etapas", "Qué entra y qué sale en cada paso")
    _render_stages()

    section(3, "Configuración de los Modelos", "Parámetros y archivos de salida")
    _render_models_table()

    section(4, "Estado de Integración", "Lo implementado y lo propuesto")
    _render_integration()


# ============================================================
# SUB-VISTAS
# ============================================================
def _render_sankey():
    nodos = [
        "1_demanda.csv", "2_clientes_rfm.csv", "3_canasta.csv",
        "K-Means", "Prophet", "Apriori", "Isolation Forest",
        "Clientes segmentados", "Pronóstico", "Combos", "Anomalías",
        "Dashboard DHM",
    ]
    colores = (
        ["#3b82f6"] * 3
        + ["#8b5cf6", "#22c55e", "#a855f7", "#ef4444"]
        + ["#f59e0b"] * 4
        + ["#06b6d4"]
    )

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=18, thickness=22,
            line=dict(color="black", width=0.4),
            label=nodos, color=colores,
        ),
        link=dict(
            source=[0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            target=[4, 6, 3, 5, 7, 8, 9, 10, 11, 11, 11, 11],
            value=[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            color="rgba(148,163,184,0.35)",
        ),
    )])
    fig.update_layout(
        title="Flujo completo: ETL → Modelos → Resultados → Dashboard",
        font=dict(size=12),
    )
    st.plotly_chart(_dark(fig, 480), use_container_width=True)

    callout(
        "Los cuatro modelos corren en **paralelo** y escriben cuatro archivos CSV. "
        "Power BI y Streamlit los consumen de forma independiente. La integración entre "
        "algoritmos es el siguiente paso (ver sección 4).",
        "info",
    )


def _render_stages():
    with st.container(border=True):
        st.markdown("### 📥 Etapa 1 · Extracción (ETL)")
        st.caption("Entradas crudas que alimentan al sistema")
        entradas = pd.DataFrame({
            "Archivo": ["1_demanda.csv", "2_clientes_rfm.csv", "3_canasta.csv"],
            "Contenido": [
                "Ventas diarias (ds, Cantidad)",
                "Clientes con Recencia, Frecuencia y Monto",
                "Líneas de factura (Factura_ID, Producto)",
            ],
            "Alimenta a": ["Prophet, Isolation Forest", "K-Means", "Apriori"],
        })
        st.dataframe(entradas, use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.markdown("### ⚙️ Etapa 2 · Transformación (Modelos)")
        st.caption("Cuatro algoritmos en paralelo, cada uno con su propio dataset de entrada")
        st.markdown(
            "- **K-Means:** estandariza Recencia/Frecuencia/Monto → 4 clústeres → asigna segmento de negocio.\n"
            "- **Prophet:** serie diaria de Cantidad → descomposición en tendencia + estacionalidad semanal y anual → pronóstico a 90 días con banda del 80%.\n"
            "- **Apriori:** matriz factura × producto → conjuntos frecuentes → reglas con Lift > 1.0.\n"
            "- **Isolation Forest:** serie diaria de Cantidad → detección de días atípicos (contamination=0.02).\n"
        )

    with st.container(border=True):
        st.markdown("### 📊 Etapa 3 · Carga (Resultados)")
        st.caption("Archivos CSV exportados a `resultados_ml/`")
        salidas = pd.DataFrame({
            "Archivo": [
                "1_clientes_segmentados.csv",
                "2_prediccion_demanda_prophet.csv",
                "3_combos_apriori.csv",
                "4_anomalias_detectadas.csv",
            ],
            "Contenido": [
                "Cliente, Cluster, Recencia, Frecuencia, Monto, Segmento_Instacart",
                "ds, yhat, yhat_lower, yhat_upper",
                "Antecedente, Consecuente, support, confidence, lift",
                "ds, Cantidad",
            ],
            "Filas aprox.": ["514", "811", "234", "15"],
        })
        st.dataframe(salidas, use_container_width=True, hide_index=True)

    with st.container(border=True):
        st.markdown("### 📈 Etapa 4 · Visualización (Dashboard)")
        st.caption("Streamlit y Power BI consumen los CSV de forma independiente")
        st.markdown(
            "- **Streamlit:** este Gemelo Digital (secciones K-Means, Prophet, Apriori, Isolation Forest, What-If).\n"
            "- **Power BI:** tablero ejecutivo con dispersión de clústeres, líneas con bandas, tabla de reglas y barras de anomalías.\n"
            "- **Integración actual:** los modelos no se retroalimentan entre sí; el dashboard los reúne visualmente.\n"
        )


def _render_models_table():
    modelos = pd.DataFrame({
        "Algoritmo": ["K-Means", "Prophet", "Apriori", "Isolation Forest"],
        "Tipo de análisis": ["Descriptivo", "Predictivo", "Prescriptivo", "Diagnóstico"],
        "Pregunta": [
            "¿Quién es el cliente?",
            "¿Cuánto se venderá?",
            "¿Qué ofrecer junto?",
            "¿Qué día es anómalo?",
        ],
        "Configuración": [
            "K=4 · StandardScaler · random_state=42",
            "90 días · estacionalidad anual+semanal · interval 80%",
            "min_support=0.01 · lift mínimo 1.0",
            "contamination=0.02 · random_state=42",
        ],
        "Salida": [
            "1_clientes_segmentados.csv",
            "2_prediccion_demanda_prophet.csv",
            "3_combos_apriori.csv",
            "4_anomalias_detectadas.csv",
        ],
    })
    st.dataframe(modelos, use_container_width=True, hide_index=True)


def _render_integration():
    inter = pd.DataFrame({
        "Interacción": [
            "K-Means → Apriori",
            "Prophet ↔ Isolation Forest",
            "K-Means → Prophet",
            "K-Means → Isolation Forest",
            "Todos → Power BI / Streamlit",
        ],
        "Mecanismo": [
            "Reglas por segmento",
            "Alertas como residuos",
            "Pronóstico por segmento",
            "Atribuir picos a clientes",
            "Visualización conjunta",
        ],
        "Estado": ["Propuesta", "Propuesta", "Propuesta", "Propuesta", "Implementado"],
    })
    st.dataframe(inter, use_container_width=True, hide_index=True)

    callout(
        "**Hoy:** cuatro modelos en paralelo, cuatro CSV, un dashboard que los reúne visualmente.\n\n"
        "**Siguiente paso:** que Apriori reciba la segmentación, que Isolation Forest use los "
        "residuos de Prophet, y que los cuatro se retroalimenten en un simulador de decisiones.",
        "warn",
    )