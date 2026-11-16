import streamlit as st
import pandas as pd

def show():
    # Encabezado
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🏗️ Ingeniería de Datos: Pipeline ETL y Datos Sintéticos</h1>
        <p style='text-align: center; font-size: 1.2em;'>
            Cómo construimos el cimiento del Gemelo Digital (Fases 1 y 2 del Ciclo de Vida)
        </p>
        <hr>
    """, unsafe_allow_html=True)

    # Pestañas
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔄 Arquitectura ETL", 
        "🧠 Lógica de Negocio", 
        "⚠️ Desafíos de Ingeniería", 
        "🔍 Auditoría y Limitaciones", 
        "📊 Contrato de Datos"
    ])

    # ---------------------------------------------------------
    # TAB 1: ARQUITECTURA ETL
    # ---------------------------------------------------------
    with tab1:
        st.header("El Problema y la Solución")
        st.write("""
            **El problema:** DHM tenía un esquema de base de datos maduro, pero **vacío**. Sin datos, no hay series temporales que pronosticar ni clientes que segmentar. Esperar 2 años a tener datos reales habría detenido el proyecto.
            **La solución:** Generar un ecosistema de datos sintéticos (Mock Data) relacionalmente íntegro y auditable.
        """)
        
        st.subheader("Los Dos Ciclos ETL Encadenados")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("**Ciclo 1: `seed_mock_data.py`**")
            st.markdown("""
            *   **Extract:** Lee el catálogo de productos y usuarios existentes. Protege la base original clonándola a `db_huevos_mendez_MOCK.sqlite3`.
            *   **Transform:** Usa `random` y `Faker(es_ES)` para generar ~29,400 filas.
            *   **Load:** Inserta masivamente respetando la jerarquía de claves foráneas y la atomicidad (un solo `commit`).
            """)
            
        with col2:
            st.success("**Ciclo 2: `01_preparar_datasets.py`**")
            st.markdown("""
            *   **Extract:** Consultas SQL con `JOIN` y `GROUP BY` sobre la base MOCK.
            *   **Transform:** Uso de `pandas` para calcular Recencia, agrupar por día, etc.
            *   **Load:** Exportación a 3 archivos CSV en la carpeta `datasets_ml`.
            """)

        st.warning("🛡️ **Protección de la Fuente:** Todo el proceso se ejecuta sobre una copia. La base de datos original (`db_huevos_mendez.sqlite3`) jamás se altera.")

    # ---------------------------------------------------------
    # TAB 2: LÓGICA DE NEGOCIO (Punto 1 corregido)
    # ---------------------------------------------------------
    with tab2:
        st.header("¿Qué reglas de negocio se inyectaron?")
        st.write("Para que los algoritmos tengan algo que analizar, inyectamos reglas lógicas inspiradas en la realidad de DHM y el caso Instacart:")
        
        st.markdown("""
        *   🎯 **3 Perfiles de Cliente:** Creamos clientes de "Alto Valor", "Sensibles a Descuento" y "En Riesgo". Esto define su límite de crédito y saldo.
        *   📉 **15% de Ventas Perdidas (Sustituciones):** En 15 de cada 100 facturas, simulamos que el cliente pidió Huevo Blanco pero se le ofreció Huevo Rojo por falta de stock.
        *   📦 **Inventario Realista:** Simulamos lotes de huevos con fechas de vencimiento, compras a crédito (50%) y de contado (50%).
        """)
        
        st.divider()

        st.subheader("🚨 El Error Controlado (Fin de Semana)")
        st.write("Queríamos simular que los fines de semana había **más ventas**. El código intentó mover las ventas de sábado y domingo hacia días de semana para simular picos de demanda... pero el resultado fue el opuesto.")
        
        st.error("""
        **Hallazgo Crítico:** Al desplazar aleatoriamente el 50% de las ventas de sábado y domingo hacia días hábiles, los fines de semana terminaron acumulando **la mitad de la demanda** de un día normal. 
        *Esto demuestra por qué auditar los datos siempre es obligatorio.*
        """)

    # ---------------------------------------------------------
    # TAB 3: DESAFÍOS DE INGENIERÍA (Punto 2 corregido)
    # ---------------------------------------------------------
    with tab3:
        st.header("Resolución de Restricciones (Constraints)")
        st.write("Un pipeline que corre a la primera es sospechoso. Estos son los 3 errores de SQLite que resolvimos y nos enseñaron sobre calidad de datos:")
        
        # Usamos 3 columnas para que el diseño sea ejecutivo y sin scroll
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.error("🚨 **UNIQUE (Fechas)**")
            st.markdown("""
            **El Error:** `core_caja.fecha` falló. Se generaron 100 fechas al azar en 730 días, pero chocaron entre sí (Paradoja del Cumpleaños).
            **La Solución:** Usamos `random.sample()` que garantiza **fechas únicas** (sin reemplazo).
            *Dimensión:* Unicidad
            """)
            
        with col2:
            st.warning("⚠️ **NOT NULL (Nulos)**")
            st.markdown("""
            **El Error:** `core_proveedor.contacto` falló. El script no enviaba el nombre del contacto, un campo obligatorio.
            **La Solución:** Se agregó la columna y se pobló con `fake.name()`.
            *Dimensión:* Completitud
            """)
            
        with col3:
            st.info("🧩 **Bindings (Tuplas)**")
            st.markdown("""
            **El Error:** En `core_merma`, el SQL tenía 6 signos `?` pero la tupla de Python enviaba 7 valores.
            **La Solución:** Alineamos el SQL y la tupla, decidiendo usar la fecha simulada en lugar de `datetime('now')`.
            *Dimensión:* Consistencia
            """)

    # ---------------------------------------------------------
    # TAB 4: AUDITORÍA Y LIMITACIONES
    # ---------------------------------------------------------
    with tab4:
        st.header("Auditoría del Dataset (Ética de Datos)")
        st.write("La honestidad es clave. El dataset es excelente para probar la arquitectura, pero no es un sustituto de la realidad. Estas son sus limitaciones:")
        
        with st.expander("⚠️ 1. Independencia Total (Sin asociaciones reales)"):
            st.markdown("""
            Como los productos de cada factura se eligen de forma uniforme e independiente (`random.choice`), **el Lift teórico entre cualquier par de productos es 1**. 
            El algoritmo Apriori no encontrará reglas comerciales reales, sino solo ruido estadístico. Sirve para probar la mecánica del flujo, no para tomar decisiones de negocio.
            """)
            
        with st.expander("👥 2. Perfiles Desacoplados del Comportamiento"):
            st.markdown("""
            Aunque existen perfiles (Alto Valor, En Riesgo), el cliente de cada factura se elige al azar. Un cliente "En Riesgo" tiene la misma probabilidad de comprar que uno de "Alto Valor". Por lo tanto, la Frecuencia y el Monto no reflejan el perfil.
            """)
            
        with st.expander("📉 3. Falta de Estacionalidad Real"):
            st.markdown("""
            *   No hay efecto de diciembre (el código no tiene regla mensual).
            *   Los precios y costos son constantes durante los 730 días simulados (no hay inflación).
            *   El inventario (Kardex) tiene saldos de relleno que no cuadran contablemente.
            """)
            
        with st.expander("🧮 4. Recencia Sesgada (fillna(0))"):
            st.markdown("""
            Para los 9 clientes que no tienen compras, la Recencia se rellenó con `0`. En RFM, Recencia 0 significa "compró hoy", lo cual es incorrecto para alguien que nunca ha comprado.
            """)

    # ---------------------------------------------------------
    # TAB 5: CONTRATO DE DATOS (Punto 3 corregido)
    # ---------------------------------------------------------
    with tab5:
        st.header("Los 3 Datasets Exportados")
        st.write("El segundo ciclo ETL preparó los datos con la granularidad exacta que cada algoritmo necesita. Aquí te explicamos detalladamente qué significa 'Una fila' en cada archivo:")
        
        c1, c2, c3 = st.columns(3)
        
        with c1:
            st.info("📈 **1_demanda.csv**")
            st.markdown("""
            **Una fila es:** Un producto específico en un día específico.
            *(Ej: El Lunes 5 de mayo, se vendieron 15 cajillas de Huevo Blanco).*
            
            **¿Para qué sirve?** Para que **Prophet** aprenda la serie temporal y prediga cuánto se venderá mañana.
            """)
            
        with c2:
            st.success("👥 **2_clientes_rfm.csv**")
            st.markdown("""
            **Una fila es:** Un cliente único.
            *(Ej: Pulpería El Buen Precio, que compró por última vez hace 10 días, ha comprado 15 veces y gastó C$ 50,000).*
            
            **¿Para qué sirve?** Para que **K-Means** agrupe a los clientes según su Recencia, Frecuencia y Monto.
            """)
            
        with c3:
            st.warning("🛒 **3_canasta.csv**")
            st.markdown("""
            **Una fila es:** Una línea de una factura (el producto físico).
            *(Ej: Si una factura tiene 3 productos, habrá 3 filas distintas para esa misma factura).*
            
            **¿Para qué sirve?** Para que **Apriori** encuentre patrones del tipo "quien compra A, también compra B".
            """)
            
        st.error("""
        **⚠️ Alerta de Datos (3_canasta.csv):** 
        Este archivo tiene 4,007 facturas porque se mezclaron 7 facturas preexistentes de la base original con las 4,000 generadas. 
        Además, contiene el mismo producto varias veces en una factura (duplicados). *Antes de pasarlo a Apriori, el script debe pivotar los datos a una matriz binaria.*
        """)