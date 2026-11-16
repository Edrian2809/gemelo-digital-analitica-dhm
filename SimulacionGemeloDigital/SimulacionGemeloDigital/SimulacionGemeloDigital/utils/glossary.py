# utils/glossary.py
import streamlit as st
import re

GLOSSARY = {
    "XGBoost": "eXtreme Gradient Boosting. Algoritmo de árboles de decisión muy potente que Instacart usa para predecir la probabilidad de que un producto esté en el estante.",
    "Bandidos Contextuales": "Algoritmo de aprendizaje por refuerzo. Resuelve el dilema de 'explorar' vs 'explotar' basándose en el contexto.",
    "Contextual Bandits": "Ver 'Bandidos Contextuales'. Técnica de aprendizaje por refuerzo para personalización en tiempo real.",
    "Embeddings": "Representación de palabras o productos como vectores numéricos en un espacio geométrico.",
    "Transformers": "Arquitectura de redes neuronales que usa mecanismos de atención para procesar texto.",
    "ETL": "Extract, Transform, Load. Proceso de extraer datos, limpiarlos y cargarlos en un destino final.",
    "Kafka": "Apache Kafka. Plataforma de streaming de eventos en tiempo real.",
    "Snowflake": "Data Warehouse en la nube. Almacén centralizado de datos analíticos.",
    "Griffin 2.0": "Plataforma interna de MLOps de Instacart para entrenar y desplegar modelos.",
    "Contrafactual": "Modelado de escenarios hipotéticos. Estimar lo que habría pasado si X hubiera ocurrido.",
    "Churn": "Tasa de abandono de clientes.",
    "RFM": "Recencia, Frecuencia, Monto. Metodología para segmentar clientes.",
    "ROP": "Re-order Point (Punto de Reorden). Nivel de inventario para hacer un nuevo pedido.",
    "EOQ": "Economic Order Quantity. Volumen óptimo de compra.",
    "Lift": "Métrica de Apriori. Mide la fuerza de una asociación (Lift > 1 indica relación).",
    "MLOps": "Machine Learning Operations. Prácticas para mantener modelos de IA en producción.",
    "Batch": "Procesamiento por lotes. Procesar datos en bloques.",
    "Mock Data": "Datos sintéticos o falsos creados para probar un sistema.",
    "SQLite": "Base de datos relacional ligera basada en archivos.",
    "Prophet": "Algoritmo de pronóstico de series temporales desarrollado por Meta.",
    "K-Means": "Algoritmo de clustering no supervisado que agrupa datos en K grupos.",
    "Apriori": "Algoritmo de reglas de asociación que encuentra productos que se compran juntos.",
    "Isolation Forest": "Algoritmo no supervisado para detectar anomalías."
}

def init_session():
    if "seen_terms" not in st.session_state:
        st.session_state.seen_terms = set()

def render_text(text):
    init_session()
    
    # Buscar todas las palabras del glosario
    pattern = r'\b(' + '|'.join(map(re.escape, GLOSSARY.keys())) + r')\b'
    parts = re.split(pattern, text, flags=re.IGNORECASE)

    for part in parts:
        if not part:
            continue
            
        matched_term = next((t for t in GLOSSARY if t.lower() == part.lower()), None)

        if matched_term:
            if matched_term in st.session_state.seen_terms:
                st.markdown(f"**{part}**", unsafe_allow_html=True)
            else:
                # Usamos un expander simple. Al abrirlo, ya se marca como leído.
                with st.expander(f"❓ {part} (Clic para ver definición)"):
                    st.write(GLOSSARY[matched_term])
                    # Un botón simple para cerrar y guardar en memoria
                    if st.button(f"Entendido ✔️", key=f"close_{part}_{len(text)}"):
                        st.session_state.seen_terms.add(matched_term)
                        st.rerun()
        else:
            # Limpiar texto normal
            clean_part = part.strip()
            if clean_part and not re.fullmatch(r'\*+', clean_part):
                st.markdown(clean_part, unsafe_allow_html=True)

def smart_term(term, definition, display_text=None):
    init_session()
    if term not in GLOSSARY:
        GLOSSARY[term] = definition

    if display_text is None:
        display_text = term

    if term in st.session_state.seen_terms:
        st.markdown(f"**{display_text}**", unsafe_allow_html=True)
    else:
        with st.expander(f"❓ {display_text} (Clic para ver definición)"):
            st.write(definition)
            if st.button(f"Entendido ✔️", key=f"close_{term}_{len(definition)}"):
                st.session_state.seen_terms.add(term)
                st.rerun()