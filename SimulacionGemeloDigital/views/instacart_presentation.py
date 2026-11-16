# views/instacart_presentation.py
import streamlit as st
import pandas as pd

def show():
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🛒 El Ecosistema de Instacart</h1>
        <p style='text-align: center; font-size: 1.2em;'>
            ¿Cómo una PyME como Huevos Méndez (DHM) puede aprender del gigante logístico de alimentos frescos?
        </p>
        <hr>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 ¿Qué es Instacart?", 
        "⚙️ El Estado del Arte (ML)", 
        "📊 Análisis de Brechas", 
        "🔄 Adaptación a DHM", 
        "🎯 Impacto en el Negocio"
    ])

    with tab1:
        st.header("El Modelo de Negocio de Instacart")
        st.write("""
            Instacart **no es dueño de los productos que entrega**. Funciona como una capa tecnológica y logística entre las tiendas (que poseen el inventario) y los compradores. 
            Toda su estrategia es un problema de **inferencia sobre un inventario que no controla**.
        """)
        
        st.subheader("¿Por qué Instacart y no Amazon, Netflix o Spotify?")
        col1, col2 = st.columns(2)
        with col1:
            st.info("**1. Logística sin control de inventario**\n\nDHM distribuye producto de terceros y no controla la oferta de sus proveedores, al igual que Instacart.")
            st.info("**2. Productos Perecederos**\n\nEn alimentos frescos (y huevos), el error de predicción tiene un costo asimétrico: sobreestimar genera mermas, subestimar genera pérdida de ventas.")
        with col2:
            st.info("**3. Disponibilidad y Sustituciones**\n\nSi un artículo no está disponible, el comprador recibe un reemplazo. DHM enfrenta la misma situación (Ej. Huevo Blanco Grande por Mediano).")
            st.info("**4. Demanda Perdida (Lost Demand)**\n\nVentas que no ocurrieron porque el producto no estaba. Instacart lo llama *'Modeling the Unseen'*.")

        st.warning("💡 **Conclusión de selección:** Netflix o Spotify resuelven problemas de descubrimiento en catálogos digitales. Instacart enfrenta el mismo problema físico y perecedero que DHM.")

    with tab2:
        st.header("Arquitectura de Machine Learning de Instacart")
        st.write("Instacart opera con un stack tecnológico de alto nivel:")
        
        st.markdown("""
        *   **Apache Kafka:** Captura de eventos en tiempo real (clics y compras al instante).
        *   **Snowflake:** Almacenamiento analítico (Data Warehouse) en la nube.
        *   **Griffin 2.0:** Plataforma de MLOps para entrenar y desplegar modelos de IA.
        """)
        
        st.subheader("Las 5 Capacidades Core de Instacart")
        
        with st.expander("1. Predicción de Disponibilidad (XGBoost)"):
            st.write("Usa **XGBoost** (un algoritmo de árboles de decisión potenciado por gradiente) para estimar la probabilidad (0 a 1) de que un producto esté físicamente en el estante.")
            
        with st.expander("2. Modelado de Demanda Perdida (Contrafactual)"):
            st.write("Usa **modelos contrafactuales** (escenarios hipotéticos) para estimar lo que se habría vendido si el producto hubiera estado disponible. `Demanda Perdida = Demanda Contrafactual - Demanda Observada`.")
            
        with st.expander("3. Personalización (Bandidos Contextuales)"):
            st.write("Usa **Bandidos Contextuales** (aprendizaje por refuerzo) para resolver el dilema de 'explorar' (mostrar algo nuevo) vs 'explotar' (mostrar lo que ya le gusta) basándose en el contexto del usuario.")
            
        with st.expander("4. Búsqueda Semántica (Embeddings y Transformers)"):
            st.write("Usa **Embeddings** (representación de productos como vectores numéricos) y **Transformers** (redes neuronales con mecanismos de atención) para encontrar productos similares aunque no compartan las mismas palabras.")
            
        with st.expander("5. Análisis de Canasta (Frequent Bought Together)"):
            st.write("Identifica productos que se compran juntos con frecuencia para recomendaciones del tipo *'Los clientes que compraron esto también compraron aquello'*.")

    with tab3:
        st.header("Gap Analysis: Instacart vs. DHM")
        gap_data = {
            "Dimensión": ["Escala del catálogo", "Infraestructura", "Equipo", "Temporalidad", "Algoritmos de stock", "Personalización"],
            "Instacart (Gigante)": ["200 millones de ítems", "Kafka, Snowflake", "Cientos de ingenieros", "Tiempo real", "XGBoost (árboles)", "Bandidos Contextuales"],
            "DHM (PyME)": ["6 productos", "SQLite, Python, CSVs", "Analista único", "Batch diario", "Prophet (series temporales)", "K-Means (Clustering)"],
        }
        st.dataframe(pd.DataFrame(gap_data), use_container_width=True, hide_index=True)
        st.info("**Principio de Adaptación:** Conservar la lógica analítica, simplificar la ingeniería.")

    with tab4:
        st.header("¿Cómo replicamos esto en el Gemelo Digital de DHM?")
        st.write("Debido a las brechas, se reemplazó el mecanismo por uno proporcional a los recursos de DHM:")
        
        adapt_data = {
            "Técnica de Instacart": ["Disponibilidad en tiempo real (XGBoost)", "Bandidos contextuales", "Búsqueda con embeddings", "Modelado de fraude y demanda perdida"],
            "Algoritmo adaptado en DHM": ["Prophet", "K-Means", "Apriori", "Isolation Forest"],
            "Pregunta de negocio en DHM": [
                "¿Cuánta demanda habrá en los próximos días?", 
                "¿Qué grupos de clientes existen y qué oferta corresponde?", 
                "¿Qué productos se compran juntos o se sustituyen?", 
                "¿Qué días tuvieron un comportamiento anormal?"
            ]
        }
        st.dataframe(pd.DataFrame(adapt_data), use_container_width=True, hide_index=True)

        st.divider()
        st.subheader("Justificación de la Adaptación")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.expander("📏 1. Brecha de Escala"):
                st.markdown("""
                *   **Instacart:** Necesita *embeddings* (vectores densos) para buscar en un catálogo gigantesco.
                *   **DHM:** Con solo 6 productos, el algoritmo **Apriori** es matemáticamente superior porque evalúa todas las combinaciones de forma exhaustiva y arroja reglas 100% interpretables (Ej. Lift de 12.4).
                """)
            with st.expander("🏗️ 2. Brecha de Infraestructura"):
                st.markdown("""
                *   **Instacart:** Usa flujos de eventos en tiempo real con Apache Kafka.
                *   **DHM:** Usamos un **pipeline ETL por lotes (Batch)** con SQLite. **Prophet** es ideal porque se entrena sobre ventas diarias agregadas.
                """)
        with col2:
            with st.expander("👨‍💻 3. Brecha de Equipo"):
                st.markdown("""
                *   **Instacart:** Equipos de MLOps mantienen modelos complejos de aprendizaje por refuerzo.
                *   **DHM:** Usamos **K-Means**, que ofrece una segmentación estática (RFM) fácil de interpretar y accionar por un solo analista.
                """)
            with st.expander("⏱️ 4. Brecha de Temporalidad"):
                st.markdown("""
                *   **Instacart:** Predice la probabilidad de que un huevo esté en el estante *en este instante*.
                *   **DHM:** La decisión de compra es diaria. Usar **Isolation Forest** detecta caídas anómalas (quiebres de stock) sin necesidad de etiquetas previas.
                """)
        
        st.success("💡 **Principio de Ingeniería Inversa:** Conservar la pregunta de negocio y reemplazar el mecanismo por uno proporcional a nuestros recursos.")

    with tab5:
        st.header("Impacto en el Negocio: Instacart vs. DHM")
        
        st.subheader("1. Gestión de Mermas y Exceso de Inventario")
        col_i1, col_d1 = st.columns(2)
        with col_i1:
            st.info("**En Instacart:** Usa XGBoost para predecir la disponibilidad y **ocultar dinámicamente** los productos con alta probabilidad de estar agotados, mejorando la experiencia de compra.")
        with col_d1:
            st.success("**En DHM:** Usa **Prophet + K-Means** para proyectar la demanda diaria, ajustar compras al proveedor y dirigir promociones de rotación a clientes específicos.")

        st.subheader("2. Quiebres de Stock y Demanda Perdida")
        col_i2, col_d2 = st.columns(2)
        with col_i2:
            st.warning("**En Instacart:** Aborda el *Lost Demand* con *Modeling the Unseen*: estiman qué se habría vendido si el producto estuviera ahí, corrigiendo el sesgo de sus recomendaciones.")
        with col_d2:
            st.success("**En DHM:** Usamos **Isolation Forest** para detectar días anómalos (caídas atípicas) y **Prophet** para distinguir si la caída fue por un feriado o por un faltante real.")

        st.subheader("3. Ventas Cruzadas (Cross-Selling)")
        col_i3, col_d3 = st.columns(2)
        with col_i3:
            st.info("**En Instacart:** Usan Embeddings y Transformers para calcular similitud semántica y recomendaciones de 'Frequent Bought Together'.")
        with col_d3:
            st.success("**En DHM:** Usamos **Apriori**, que es transparente y directo. Descubrimos reglas con un **Lift de 12.4** (asociación fuerte) para ofrecer productos asociados o sugerir reemplazos.")

        st.subheader("4. Personalización y Ofertas")
        col_i4, col_d4 = st.columns(2)
        with col_i4:
            st.info("**En Instacart:** Utilizan Bandidos Contextuales para decidir en tiempo real si mostrar un producto conocido o uno nuevo y maximizar la recompensa.")
        with col_d4:
            st.success("**En DHM:** Usamos **K-Means** para crear una segmentación estática basada en RFM (Recencia, Frecuencia, Monto). Prescribimos ofertas fijas por clúster.")

        st.divider()
        st.subheader("Evolución de los 4 Tipos de Análisis")
        st.markdown("""
        *   **1. Descriptivo:** En DHM, describe co-ocurrencias con **Apriori** y comportamiento **RFM** con **K-Means**.
        *   **2. Diagnóstico:** **Isolation Forest** señala caídas anómalas compatibles con quiebres de stock.
        *   **3. Predictivo:** **Prophet** proyecta ventas con tendencia y estacionalidad.
        *   **4. Prescriptivo:** Las reglas definen ofertas por segmento y reposición.
        """)