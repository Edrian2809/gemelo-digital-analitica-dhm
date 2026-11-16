# views/home.py
import streamlit as st
from utils.ui_components import hero, section, metric_col, callout
from utils.helpers import caj
from utils.data_loader import load_res

def show():
    _c = load_res("1_clientes_segmentados.csv")
    _p = load_res("2_prediccion_demanda_prophet.csv")
    _k = load_res("3_combos_apriori.csv")
    _a = load_res("4_anomalias_detectadas.csv")
    section("01", "Ciclo de Vida de Data Analytics", "Alineación metodológica del proyecto (Smith, 2021)")
    
    st.markdown("""
    <div style="display: flex; justify-content: space-between; text-align: center; margin-bottom: 20px;">
        <div style="flex: 1; padding: 10px; border-bottom: 3px solid #3b82f6;">
            <strong style="color: #3b82f6;">Fase 1 y 2</strong><br>
            <span style="font-size: 12px; color: #8b949e;">ETL & Data Prep</span>
        </div>
        <div style="flex: 1; padding: 10px; border-bottom: 3px solid #8b5cf6;">
            <strong style="color: #8b5cf6;">Fase 3 y 4</strong><br>
            <span style="font-size: 12px; color: #8b949e;">Planificación & Modelado</span>
        </div>
        <div style="flex: 1; padding: 10px; border-bottom: 3px solid #10b981;">
            <strong style="color: #10b981;">Fase 5</strong><br>
            <span style="font-size: 12px; color: #8b949e;">Comunicación</span>
        </div>
        <div style="flex: 1; padding: 10px; border-bottom: 3px solid #f59e0b;">
            <strong style="color: #f59e0b;">Fase 6</strong><br>
            <span style="font-size: 12px; color: #8b949e;">Operacionalización</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("💡 **Nota para el evaluador:** Cada vista de este menú lateral indica explícitamente a qué fase del ciclo de vida de Data Analytics corresponde. Los algoritmos (K-Means, Prophet, Apriori, Isolation Forest) responden a las fases de construcción, mientras que el Informe de Resultados y el Análisis Costo-Beneficio responden a las fases de comunicación y operacionalización.")
    hero(
        "Digital Twin - DHM",
        "Gemelo Digital de Distribuidora Huevos Mendez",
        "Lógica Analítica de Instacart para la generación de Algoritmos aplicados a una PyME distribuidora de huevos en Nicaragua. Cada modulo incluye un mini caso didactico.",
        "Smith (2021) - Alfaro Arriola (2026) - Taylor & Letham (2018) - Agrawal & Srikant (1994) - Liu, Ting & Zhou (2008) - Lloyd (1982)",
    )
    
    section("00", "Estado del gemelo digital")
    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Clientes segmentados", len(_c) if not _c.empty else "-", "K-Means aplicado", "pos")
    d90 = float(_p.tail(90)["yhat"].sum()) if not _p.empty else 0
    metric_col(c2, "Demanda 90 dias", caj(d90), "Proyeccion Prophet", "pos")
    metric_col(c3, "Reglas Apriori", len(_k) if not _k.empty else "-", "Combos detectados")
    metric_col(c4, "Dias anomalos", len(_a) if not _a.empty else "-", "Isolation Forest", "neg" if not _a.empty else "neu")

    section("01", "Arquitectura de los 4 pilares", "Instacart replicado en la operacion de DHM")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            "<div class='scenario' style='border-left: 4px solid #7c3aed; height: 140px;'>"
            "<div class='scenario-label' style='color:#a78bfa;'>👤 Personalization -> K-Means</div>"
            "<div style='color:#e6edf3; font-size:14px; font-weight:600; margin-bottom:8px;'>Segmentacion de Clientes</div>"
            "<div style='color:#8b949e; font-size:12px;'>Identifica clientes de Alto Valor, Sensibles a Descuento y en Riesgo para proteger ingresos.</div>"
            "</div>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='scenario' style='border-left: 4px solid #10b981; height: 140px;'>"
            "<div class='scenario-label' style='color:#6ee7b7;'>🛒 Frequently Bought Together -> Apriori</div>"
            "<div style='color:#e6edf3; font-size:14px; font-weight:600; margin-bottom:8px;'>Reglas de Asociacion</div>"
            "<div style='color:#8b949e; font-size:12px;'>Descubre que productos se compran juntos para aumentar el ticket promedio sin sacrificar margen.</div>"
            "</div>", unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            "<div class='scenario' style='border-left: 4px solid #06b6d4; height: 140px;'>"
            "<div class='scenario-label' style='color:#67e8f9;'>📈 Forecasting -> Prophet</div>"
            "<div style='color:#e6edf3; font-size:14px; font-weight:600; margin-bottom:8px;'>Pronostico de Demanda</div>"
            "<div style='color:#8b949e; font-size:12px;'>Predice cajillas por dia para evitar quiebres de stock y mermas por sobrecompra.</div>"
            "</div>", unsafe_allow_html=True
        )
        st.markdown(
            "<div class='scenario' style='border-left: 4px solid #f59e0b; height: 140px;'>"
            "<div class='scenario-label' style='color:#fcd34d;'>🕵️ Modeling the Unseen -> Isolation Forest</div>"
            "<div style='color:#e6edf3; font-size:14px; font-weight:600; margin-bottom:8px;'>Deteccion de Anomalias</div>"
            "<div style='color:#8b949e; font-size:12px;'>Detecta fraudes, errores de facturacion o mermas extraordinarias en los registros diarios.</div>"
            "</div>", unsafe_allow_html=True
        )

    section("02", "¿Como navegar este Gemelo Digital?")
    callout(
        "Usa el menu lateral izquierdo para explorar cada modulo. Cada seccion incluye un **Mini Caso Didactico** interactivo, "
        "las **Formulas matematicas** detras del algoritmo, y una **Simulacion con datos reales** de tu base de datos.",
        "info"
    )