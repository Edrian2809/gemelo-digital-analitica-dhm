# views/pipeline_data.py
import streamlit as st
import pandas as pd

def show():
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🏗️ Ingeniería de Datos: Pipeline ETL y Datos Sintéticos</h1>
        <p style='text-align: center; font-size: 1.2em;'>
            Cómo construimos el cimiento del Gemelo Digital (Fases 1 y 2 del Ciclo de Vida)
        </p>
        <hr>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔄 Arquitectura ETL", 
        "🧠 Lógica de Negocio", 
        "⚠️ Desafíos de Ingeniería", 
        "🔍 Auditoría y Limitaciones", 
        "📊 Contrato de Datos"
    ])

    with tab1:
        st.header("El Problema y la Solución")
        st.write("""
            **El problema:** DHM tenía un esquema de base de datos maduro, pero **vacío**. Sin datos, no hay series temporales que pronosticar.
            **La solución:** Generar un ecosistema de datos sintéticos (Mock Data) relacionalmente íntegro y auditable.
        """)
        
        st.subheader("Los Dos Ciclos ETL Encadenados")
        st.info("**ETL (Extract, Transform, Load):** Proceso de extraer datos, limpiarlos/transformarlos y cargarlos a un destino final.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Ciclo 1: `seed_mock_data.py`**\n\n"
                    "- **Extract:** Clona la base original a `MOCK.sqlite3`.\n"
                    "- **Transform:** Usa `random` y `Faker` para generar ~29,400 filas.\n"
                    "- **Load:** Inserta masivamente respetando claves foráneas.")
        with col2:
            st.success("**Ciclo 2: `01_preparar_datasets.py`**\n\n"
                       "- **Extract:** Consultas SQL con JOINs y GROUP BY.\n"
                       "- **Transform:** Uso de `pandas` para calcular Recencia.\n"
                       "- **Load:** Exportación a 3 archivos CSV para los modelos.")
        
        st.warning("🛡️ **Protección:** Todo se ejecuta sobre una copia. La base original jamás se altera.")

    with tab2:
        st.header("¿Qué reglas de negocio se inyectaron?")
        st.markdown("""
        *   🎯 **3 Perfiles:** "Alto Valor", "Sensibles a Descuento" y "En Riesgo". Define su límite de crédito.
        *   📉 **15% de Ventas Perdidas (Sustituciones):** Simulamos que el cliente pidió Blanco pero se le ofreció Rojo por falta de stock.
        *   📦 **Inventario Realista:** Lotes con vencimiento, compras a crédito (50%) y de contado (50%).
        """)
        st.divider()
        st.subheader("🚨 El Error Controlado (Fin de Semana)")
        st.write("Queríamos simular que los fines de semana había **más ventas**. El código movió las ventas de fin de semana hacia días hábiles... pero el resultado fue el opuesto.")
        st.error("**Hallazgo Crítico:** Al desplazar el 50% de las ventas, los fines de semana terminaron acumulando **la mitad de la demanda** de un día normal. *Esto demuestra por qué auditar los datos es obligatorio.*")

    with tab3:
        st.header("Resolución de Restricciones (Constraints)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.error("🚨 **UNIQUE (Fechas)**\n\nSe generaron fechas al azar pero chocaron. Solución: `random.sample()` para garantizar unicidad.")
        with col2:
            st.warning("⚠️ **NOT NULL (Nulos)**\n\nEl script no enviaba el nombre del contacto. Solución: `fake.name()` para poblarlo.")
        with col3:
            st.info("🧩 **Bindings (Tuplas)**\n\nEl SQL tenía 6 `?` pero la tupla enviaba 7. Solución: Alinear SQL y tupla.")

    with tab4:
        st.header("Auditoría del Dataset (Ética de Datos)")
        with st.expander("⚠️ 1. Independencia Total"):
            st.write("Como los productos se eligen al azar, **el Lift (fuerza de asociación) entre cualquier par de productos es 1**. Apriori solo encontrará ruido estadístico.")
        with st.expander("👥 2. Perfiles Desacoplados"):
            st.write("El cliente de cada factura se elige al azar. Un cliente 'En Riesgo' tiene la misma probabilidad de comprar que uno de 'Alto Valor'.")
        with st.expander("📉 3. Falta de Estacionalidad Real"):
            st.write("No hay efecto de diciembre, los precios son constantes (sin inflación) y el Kardex tiene saldos de relleno.")

    with tab5:
        st.header("Los 3 Datasets Exportados")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.info("📈 **1_demanda.csv**\n\n**Una fila es:** Un producto en un día específico.\n\n**¿Para qué sirve?** Para **Prophet** (aprendizaje de series temporales).")
        with c2:
            st.success("👥 **2_clientes_rfm.csv**\n\n**Una fila es:** Un cliente único.\n\n**¿Para qué sirve?** Para que **K-Means** agrupe clientes por Recencia, Frecuencia y Monto.")
        with c3:
            st.warning("🛒 **3_canasta.csv**\n\n**Una fila es:** Una línea de una factura.\n\n**¿Para qué sirve?** Para que **Apriori** encuentre patrones de compra conjunta.")
        
        st.error("**⚠️ Alerta de Datos:** Este archivo tiene 4,007 facturas (se mezclaron 7 preexistentes). Además, contiene el mismo producto varias veces en una factura. *Antes de pasarlo a Apriori, el script debe pivotar los datos a una matriz binaria.*")