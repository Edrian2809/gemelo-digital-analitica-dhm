"""
Vista: Análisis Costo-Beneficio con Evaluación de Riesgos
Fase 6 del ciclo de vida (Operacionalización) — Smith (2021).
Gemelo Digital de Huevos Méndez (DHM) · Analista a C$400/día.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.ui_components import hero, section, metric_col, callout, plot_dark, fase_ciclo_vida


# ============================================================
# HELPERS
# ============================================================
def _dark(fig, height=400):
    out = plot_dark(fig, height)
    return out if out is not None else fig


def _explain(texto: str):
    """Bloque explicativo antes de cada matriz. Se usa st.info para separarlo visualmente."""
    st.info(f"**📘 ¿Qué muestra esta matriz?** {texto}")


# ============================================================
# ENTRYPOINT
# ============================================================
def show():
    fase_ciclo_vida(6, "Operacionalización", "Evaluación de costos, retorno de inversión (ROI) y riesgos para la puesta en producción.")
    hero(
        badge="💰 FASE 6 · OPERACIONALIZACIÓN",
        title="Análisis Costo-Beneficio con Evaluación de Riesgos",
        subtitle="Gemelo Digital de Huevos Méndez (DHM) · Versión realista con analista a C$400/día",
        refs="Córdobas (C\$) · Smith (2021) · UNI · 2026",
    )

    _render_resumen()
    _render_supuestos()
    _render_volumetria()
    _render_costos()
    _render_ahorros()
    _render_financiera()
    _render_riesgos()
    _render_recomendaciones()
    _render_conclusion()


# ============================================================
# 1. RESUMEN EJECUTIVO
# ============================================================
def _render_resumen():
    section(1, "Resumen Ejecutivo", "El proyecto se paga en el primer año en la mayoría de escenarios")

    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Costo inicial", "C\$35,000", "495 h + licencias + 12% contingencia", "warn")
    metric_col(c2, "Costo anual completo", "C\$28,000", "C\$5,000 incremental si analista ya en nómina", "info")
    metric_col(c3, "Ahorro anual base", "C\$70,000", "Rango C\$31,000 – C\$105,000", "ok")
    metric_col(c4, "Payback base", "0.8 años", "0.4 años en escenario optimista", "ok")

    st.write("") # Espaciador
    callout(
        "**Diferencia clave:** si el analista ya está en nómina (costo hundido), "
        "el **desembolso incremental es solo C\$5,000/año** (licencias y varios). "
        "En ese caso, el proyecto se paga en el primer año incluso en el escenario conservador.",
        "ok",
    )

    callout(
        "**Riesgo principal:** no es financiero, sino **de decisión**. Usar datos sintéticos "
        "o modelos no validados como evidencia real (Apriori sintético, Prophet sin validar, "
        "Isolation Forest univariado). La mayor exposición identificada es lanzar combos "
        "basados en Apriori sintético: **C\$40,000–50,000/año en descuentos sin margen incremental**.",
        "danger",
    )


# ============================================================
# 2. SUPUESTOS DE PRECIOS
# ============================================================
def _render_supuestos():
    section(2, "Supuestos de Precios por Producto", "Base para valorar inventario y margen perdido")

    _explain(
        "esta tabla fija los costos y precios de venta **estimados** de las seis referencias "
        "que maneja DHM. No son precios reales: son supuestos de trabajo con un margen bruto "
        "aproximado del 25%. Estos números son los que después se usan para valorar **mermas** "
        "(costo × cajilla perdida) y **margen incremental** (margen × cajilla vendida adicional)."
    )

    precios = pd.DataFrame({
        "Producto": [
            "Huevos Pequeños Económicos Rojos",
            "Huevo Blanco Mediano",
            "Huevo Rojo Mediano",
            "Huevo Blanco Grande",
            "Huevo Rojo Grande",
            "Huevo Extra Grande",
        ],
        "Costo aprox./cajilla": ["C\$165", "C\$180", "C\$185", "C\$195", "C\$200", "C\$210"],
        "Precio venta estimado": ["C\$206", "C\$225", "C\$231", "C\$244", "C\$250", "C\$263"],
        "Margen bruto": ["C\$41", "C\$45", "C\$46", "C\$49", "C\$50", "C\$53"],
    })
    st.dataframe(precios, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    callout(
        "**Valores de referencia para el análisis:** se usa **C\$189/cajilla** como costo promedio "
        "ponderado para valorar inventario y merma, y **C\$47/cajilla** como margen bruto promedio "
        "para valorar ventas perdidas o incrementales.",
        "info",
    )


# ============================================================
# 3. VOLUMETRÍA BASE
# ============================================================
def _render_volumetria():
    section(3, "Volumetría Base", "Indicadores documentados que escalan los ahorros")

    _explain(
        "esta matriz resume las **tres cifras que anclan todos los cálculos** de ahorro. "
        "Los 730 días del dataset (dos años) se convierten a una base anual dividiendo entre dos. "
        "A partir de estas tres cifras se estiman los ahorros por merma, quiebres, cross-sell "
        "y auditoría."
    )

    vol = pd.DataFrame({
        "Indicador": ["Cajillas vendidas (730 días)", "Cajillas vendidas (base anual)", "Facturas (730 días)", "Facturas (base anual)"],
        "Valor documentado": ["84,070", "—", "4,007", "—"],
        "Base anual usada": ["—", "42,035", "—", "2,004"],
    })
    st.dataframe(vol, use_container_width=True, hide_index=True)


# ============================================================
# 4. COSTOS ESTIMADOS
# ============================================================
def _render_costos():
    section(4, "Costos Estimados", "Inversión inicial y costo recurrente anual")

    # --- 4.1 Inicial ---
    st.markdown("#### 4.1 · Costo inicial (una sola vez)")
    _explain(
        "esta matriz desglosa la **inversión inicial del proyecto** por rubro y horas de "
        "analista (495 horas a C\$50/h). Incluye un 12% de contingencia sobre el subtotal de "
        "horas + licencias. El total redondeado se usa en el cálculo del payback."
    )

    inicial = pd.DataFrame({
        "Rubro": ["Diseño y levantamiento", "ETL y preparación de datos", "Modelado ML",
                  "Visualización Power BI", "Validación y documentación", "Capacitación",
                  "Subtotal horas", "Licencias y varios", "Contingencia 12%", "Total inicial aproximado"],
        "Horas": ["50", "110", "150", "55", "90", "40", "495", "—", "—", "—"],
        "Tarifa": ["C\$50/h"] * 7 + ["—", "—", "—"],
        "Costo": ["C\$2,500", "C\$5,500", "C\$7,500", "C\$2,750", "C\$4,500",
                  "C\$2,000", "C\$24,750", "C\$5,000", "C\$3,570", "C\$35,000"],
    })
    st.dataframe(inicial, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    # --- 4.2 Recurrente ---
    st.markdown("#### 4.2 · Costo recurrente anual")
    _explain(
        "esta matriz separa el **costo completo** (que imputa el tiempo del analista) del "
        "**costo incremental** (que solo cuenta desembolsos nuevos). Es la distinción más "
        "importante del análisis: si el analista ya está en nómina, el proyecto cuesta solo "
        "C\$5,000/año, no C\$28,000."
    )

    recurrente = pd.DataFrame({
        "Rubro": [
            "Analista: reentrenamiento y validación",
            "Analista: soporte y cambios",
            "Analista: análisis y reportes",
            "Subtotal analista",
            "Licencias Power BI y varios",
            "Total completo",
            "Costo incremental (si analista ya en nómina)",
        ],
        "Horas/mes": ["8", "6", "20", "34 h/mes", "—", "—", "—"],
        "Costo anual": [
            "C\$4,800", "C\$3,600", "C\$12,000",
            "C\$20,400", "C\$5,000", "C\$28,000", "C\$5,000",
        ],
    })
    st.dataframe(recurrente, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    # --- Gráficos de composición ---
    col_a, col_b = st.columns(2)
    with col_a:
        fig = px.pie(
            names=["Horas analista", "Licencias", "Contingencia"],
            values=[24750, 5000, 3570],
            title="Composición del costo inicial (C\$35,000)",
            color_discrete_sequence=["#3b82f6", "#f59e0b", "#ef4444"],
            hole=0.45,
        )
        st.plotly_chart(_dark(fig, 340), use_container_width=True)

    with col_b:
        fig2 = px.pie(
            names=["Reentrenamiento", "Soporte", "Análisis y reportes", "Licencias"],
            values=[4800, 3600, 12000, 5000],
            title="Composición del costo anual (C\$28,000)",
            color_discrete_sequence=["#22c55e", "#06b6d4", "#3b82f6", "#f59e0b"],
            hole=0.45,
        )
        st.plotly_chart(_dark(fig2, 340), use_container_width=True)

    st.write("") # Espaciador
    callout(
        "**El 70% del costo anual es tiempo de analista** (C\$20,400 de C\$28,000). "
        "Por eso la decisión de si el analista ya está en nómina cambia radicalmente el cálculo: "
        "**C\$28,000 vs C\$5,000 anuales.**",
        "warn",
    )


# ============================================================
# 5. AHORROS POTENCIALES
# ============================================================
def _render_ahorros():
    section(5, "Ahorros Potenciales", "Cinco palancas, tres escenarios")

    _explain(
        "estas cinco fórmulas convierten cada palanca del Gemelo Digital en un monto anual. "
        "Cada ahorro multiplica una **magnitud operativa** por un **supuesto de mejora** y por "
        "el **valor unitario** (costo o margen). Son estimaciones de orden de magnitud, no "
        "mediciones."
    )

    formula_display = r"""
    \begin{aligned}
    \text{Ahorro}_{\text{merma}} &= \text{Volumen} \times \text{TasaMerma} \times \text{Reducción} \times \text{CostoPromedio} \\
    \text{Ahorro}_{\text{quiebre}} &= \text{CajillasPerdidas} \times \text{MargenPromedio} \\
    \text{Ahorro}_{\text{CrossSell}} &= \text{FacturasAnuales} \times \text{Uplift} \times \text{MargenPromedio} \\
    \text{Ahorro}_{\text{retención}} &= \text{ClientesRecuperados} \times \text{VentaAnual} \times \text{Margen} \\
    \text{Ahorro}_{\text{auditoría}} &= \text{HorasAhorradas} \times \text{CostoHora}
    \end{aligned}
    """
    st.latex(formula_display)

    st.write("") # Espaciador
    _explain(
        "esta matriz cruza cada palanca con tres escenarios (conservador, base, optimista). "
        "Cada escenario cambia el **supuesto de mejora**: por ejemplo, la merma se reduce 5%, "
        "10% o 15% según el caso. El total anual varía entre C\$31,000 y C\$105,000."
    )

    ahorros = pd.DataFrame({
        "Palanca": [
            "Reducción de merma",
            "Reducción de quiebres",
            "Ventas cruzadas",
            "Retención de clientes",
            "Auditoría más eficiente",
            "Total anual",
        ],
        "Conservador": ["C\$12,000", "C\$1,000", "C\$5,000", "C\$8,000", "C\$5,000", "C\$31,000"],
        "Base": ["C\$24,000", "C\$3,000", "C\$12,000", "C\$15,000", "C\$8,000", "C\$70,000"],
        "Optimista": ["C\$36,000", "C\$5,000", "C\$20,000", "C\$25,000", "C\$12,000", "C\$105,000"],
        "Supuesto principal": [
            "Merma base C\$238,000/año; reducción 5%, 10% y 15%",
            "2 caídas fuertes/año; 50 cajillas; margen C\$47",
            "2,004 facturas/año; uplift 0.05–0.21 cajilla/factura",
            "Recuperar 8%–24% de la venta anual de Activos Estándar",
            "Menos horas de revisión manual",
            "—",
        ],
    })
    st.dataframe(ahorros, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    # Gráfico de barras agrupadas
    palancas = ["Merma", "Quiebres", "Cross-sell", "Retención", "Auditoría"]
    cons = [12000, 1000, 5000, 8000, 5000]
    base = [24000, 3000, 12000, 15000, 8000]
    opti = [36000, 5000, 20000, 25000, 12000]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="Conservador", x=palancas, y=cons, marker_color="#94a3b8"))
    fig.add_trace(go.Bar(name="Base", x=palancas, y=base, marker_color="#3b82f6"))
    fig.add_trace(go.Bar(name="Optimista", x=palancas, y=opti, marker_color="#22c55e"))
    fig.update_layout(
        barmode="group",
        title="Ahorros anuales por palanca y escenario (C\$)",
        yaxis_title="Ahorro anual (C\$)",
    )
    st.plotly_chart(_dark(fig, 420), use_container_width=True)


# ============================================================
# 6. EVALUACIÓN FINANCIERA
# ============================================================
def _render_financiera():
    section(6, "Evaluación Financiera", "Tres vistas del mismo proyecto")

    _explain(
        "esta matriz compara las **tres formas de mirar el proyecto**: costo completo (imputa "
        "al analista), costo completo optimista y costo incremental (analista ya en nómina). "
        "El payback se calcula como Costo inicial ÷ flujo neto anual (ahorro − costo anual)."
    )

    fin = pd.DataFrame({
        "Vista": ["Costo completo (base)", "Costo completo (optimista)", "Costo incremental"],
        "Costo anual": ["C\$28,000", "C\$28,000", "C\$5,000"],
        "Ahorro base": ["C\$70,000", "C\$105,000", "C\$70,000"],
        "Resultado base": ["+C\$42,000/año", "+C\$77,000/año", "+C\$65,000/año"],
        "Payback inicial": ["0.8 años", "0.4 años", "0.5 años"],
    })
    st.dataframe(fin, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    # Tarjetas de payback
    c1, c2, c3 = st.columns(3)
    metric_col(c1, "Costo completo base", "0.8 años", "C\$42,000/año de flujo neto", "ok")
    metric_col(c2, "Costo completo optimista", "0.4 años", "C\$77,000/año de flujo neto", "ok")
    metric_col(c3, "Incremental", "0.5 años", "C\$65,000/año de flujo neto", "ok")

    st.write("") # Espaciador
    # Gráfico de flujo neto anual
    escenarios = ["Conservador", "Base", "Optimista"]
    completo = [31000 - 28000, 70000 - 28000, 105000 - 28000]
    incremental = [31000 - 5000, 70000 - 5000, 105000 - 5000]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Costo completo (C\$28k/año)",
        x=escenarios, y=completo,
        marker_color=["#94a3b8", "#3b82f6", "#22c55e"],
        text=[f"C\${v:,.0f}" for v in completo], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="Incremental (C\$5k/año)",
        x=escenarios, y=incremental,
        marker_color=["#64748b", "#06b6d4", "#10b981"],
        text=[f"C\${v:,.0f}" for v in incremental], textposition="outside",
    ))
    fig.update_layout(
        barmode="group",
        title="Flujo neto anual (ahorro − costo) en C\$",
        yaxis_title="Flujo neto anual (C\$)",
        yaxis=dict(range=[-10000, 110000]),
    )
    st.plotly_chart(_dark(fig, 420), use_container_width=True)


# ============================================================
# 7. RIESGOS (ACTUALIZADO SIN EL RIESGO DE PROPHET)
# ============================================================
def _render_riesgos():
    section(7, "Riesgos y Exposición Aproximada", "El riesgo real no es financiero, sino de decisión")

    _explain(
        "esta matriz enumera los **riesgos identificados** en el proyecto, su exposición "
        "aproximada en córdobas (cuando es cuantificable) y una nota de contexto. Los riesgos "
        "marcados como **'Cualitativo'** no se pueden monetizar con los datos actuales, pero "
        "son igual de importantes: contaminan análisis y decisiones."
    )

    riesgos = pd.DataFrame({
        "Riesgo": [
            "Apriori con facturas sintéticas",
            "K-Means: 'En Riesgo' no asignado",
            "Isolation Forest con contaminación fija",
            "Datos sintéticos no reproducibles",
            "Mezcla real/sintético sin bandera",
            "Código o documentación con errores",
            "Etiquetas de crédito no validadas",
        ],
        "Exposición aproximada": [
            "C\$40,000–50,000/año",
            "≈ C\$18,000/año de margen en riesgo",
            "≈ C\$3,000/año en auditoría",
            "≈ C\$3,400 por reproceso",
            "Cualitativo",
            "≈ C\$1,800 por reproceso",
            "Cualitativo alto",
        ],
        "Comentario": [
            "Descuentos del 5–20% sin margen incremental",
            "12 clientes; C\$102,604/año en ventas; margen 18%",
            "7.5 días/año × 8 h × C\$50/h",
            "68 h × C\$50/h",
            "Contamina análisis y decisiones",
            "36 h × C\$50/h",
            "Riesgo ético y comercial si se aplican a clientes reales",
        ],
    })
    st.dataframe(riesgos, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    _explain(
        "este gráfico **solo muestra los riesgos monetizables**, para comparar su magnitud "
        "relativa. Los riesgos cualitativos no aparecen en el gráfico pero están en la tabla."
    )

    riesgos_num = pd.DataFrame({
        "Riesgo": [
            "Apriori sintético (punto medio)",
            "K-Means 'En Riesgo' no asignado",
            "Datos sintéticos no reproducibles",
            "Isolation Forest contaminación fija",
            "Código con errores",
        ],
        "Exposición (C\$)": [45000, 18000, 3400, 3000, 1800],
    }).sort_values("Exposición (C\$)")

    fig = px.bar(
        riesgos_num, x="Exposición (C\$)", y="Riesgo", orientation="h",
        color="Exposición (C\$)", color_continuous_scale="Reds",
        text="Exposición (C\$)",
        title="Riesgos cuantificados por exposición anual (C\$)",
    )
    fig.update_traces(texttemplate="C\$%{text:,.0f}", textposition="outside")
    fig.update_layout(xaxis_title="Exposición anual (C\$)", yaxis_title="")
    st.plotly_chart(_dark(fig, 380), use_container_width=True)

    st.write("") # Espaciador
    callout(
        "**El mayor riesgo monetizable es Apriori**, con C\$45,000/año en descuentos sin margen. "
        "Esto supera ampliamente el costo anual del proyecto (C\$28,000), lo que confirma que "
        "**validar los modelos con facturas reales es la prioridad más alta**.",
        "danger",
    )

    callout(
        "**Riesgos cualitativos (no monetizados):** la mezcla de facturas reales y sintéticas sin "
        "bandera de origen contamina cualquier análisis posterior; y usar etiquetas de crédito no "
        "validadas en clientes reales es un riesgo **ético y comercial** que puede erosionar la "
        "confianza de la cartera. No se pueden poner en un gráfico, pero deben estar en la "
        "bitácora de riesgos de la gerencia.",
        "warn",
    )


# ============================================================
# 8. RECOMENDACIONES
# ============================================================
def _render_recomendaciones():
    section(8, "Recomendaciones", "Siete acciones priorizadas")

    st.markdown(
        "1. **No lanzar combos con Apriori sintético.** Repetir solo con facturas reales, "
        "fijar semilla y validar margen.\n"
        "2. **Corregir K-Means.** Aplicar 'En Riesgo' a nivel cliente y contactar a los 12 clientes "
        "con más de 300 días de inactividad.\n"
        "3. **Validar Prophet.** Truncar bandas en cero (ya realizado), incorporar feriados y calcular MAE/RMSE/MAPE.\n"
        "4. **Usar Isolation Forest sobre residuos del pronóstico.** Mantener bitácora de causas.\n"
        "5. **Pilotos con grupo de control.** Medir ticket, unidades, margen y rotación antes de escalar.\n"
        "6. **Cuantificar costos reales.** Levantar costo de merma, margen, quiebre y horas para "
        "reemplazar las cifras estimadas.\n"
        "7. **Asegurar disponibilidad del analista.** Con 34 h/mes asignadas el proyecto es viable; "
        "si la disponibilidad baja, el cronograma se extiende."
    )

    st.write("") # Espaciador
    callout(
        "Las recomendaciones 1, 2 y 4 **mitigan los tres riesgos monetizables más grandes** "
        "(Apriori, K-Means e Isolation Forest). Si solo se pudieran ejecutar tres acciones, serían esas.",
        "ok",
    )


# ============================================================
# 9. CONCLUSIÓN
# ============================================================
def _render_conclusion():
    section(9, "Conclusión", "Capacidad analítica instalada, decisiones basadas en datos")

    st.markdown(
        "Con un analista a **C\$400/día (C\$50/hora)**, el Gemelo Digital de DHM tiene un costo "
        "inicial aproximado de **C\$35,000** y un costo recurrente completo de **C\$28,000 anuales** "
        "(o **C\$5,000 incrementales** si el analista ya está en nómina). Los ahorros potenciales "
        "van de **C\$31,000 a C\$105,000 anuales**, con un escenario base de **C\$70,000**.\n\n"
        "El proyecto se paga en **menos de un año** en la mayoría de los escenarios. Su mayor "
        "restricción no es el dinero, sino la **calidad de los datos**, la **validación de los "
        "modelos** y la **disponibilidad real del analista**. Su valor principal es instalar "
        "capacidad analítica y reducir la dependencia de la intuición, preparando a DHM para "
        "decidir con datos reales cuando estos estén disponibles."
    )

    st.write("") # Espaciador
    callout(
        "**Lectura final:** el proyecto es financieramente atractivo, pero el verdadero retorno "
        "no está en los C\$70,000 de ahorro base, sino en instalar la **capacidad de decidir con "
        "datos** dentro de DHM. El riesgo a gestionar es el de usar modelos no validados como "
        "evidencia real.",
        "ok",
    )