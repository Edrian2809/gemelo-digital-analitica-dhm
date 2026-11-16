"""
Vista: Informe de Resultados
Sintetiza los hallazgos del informe de investigación del caso Instacart
aplicado al Gemelo Digital de Huevos Méndez (DHM).
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.ui_components import hero, section, metric_col, callout, formula, plot_dark, fase_ciclo_vida


# ============================================================
# HELPER: aplica tema oscuro soportando ambos patrones de plot_dark
# ============================================================
def _dark(fig, height=400):
    out = plot_dark(fig, height)
    return out if out is not None else fig


# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data(show_spinner=False)
def _csv(nombre):
    return pd.read_csv(f"resultados_ml/{nombre}")


@st.cache_data(show_spinner=False)
def cargar_resultados():
    cli = _csv("1_clientes_segmentados.csv")
    pr = _csv("2_prediccion_demanda_prophet.csv")
    co = _csv("3_combos_apriori.csv")
    an = _csv("4_anomalias_detectadas.csv")
    pr["ds"] = pd.to_datetime(pr["ds"])
    an["ds"] = pd.to_datetime(an["ds"])
    return cli, pr, co, an


# ============================================================
# ENTRYPOINT
# ============================================================
def show():
    cli, pr, co, an = cargar_resultados()
 # AQUÍ AGREGAS LA FASE
    fase_ciclo_vida(5, "Comunicación", "Traducción de los hallazgos técnicos en decisiones de negocio interpretables.")
    hero(
        badge="📊 INFORME DE RESULTADOS · GEMELO DIGITAL DHM",
        title="De la Intuición a la Ciencia de Datos",
        subtitle="Síntesis ejecutiva de los cuatro algoritmos Instacart aplicados a Huevos Méndez (DHM)",
        refs="K-Means · Prophet · Apriori · Isolation Forest · UNI · 2026",
    )

    # ---------- 1. RESUMEN EJECUTIVO ----------
    section(1, "Resumen Ejecutivo", "Los cuatro hallazgos que cambian la operación")

    total_seg = cli["Segmento_Instacart"].nunique()
    dias_total = len(pr)
    dias_anom = len(an)
    reglas = len(co)

    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Clientes", f"{len(cli):,}", f"{total_seg} segmentos de negocio", "ok")
    metric_col(c2, "Días proyectados", "90", "10,044 unidades esperadas", "info")
    metric_col(c3, "Reglas Apriori", f"{reglas}", "Lift máx = 12.47", "warn")
    metric_col(c4, "Días anómalos", f"{dias_anom}", f"{dias_anom/dias_total*100:.1f}% del historial", "danger")

    st.write("") # Espaciador
    callout(
        "**Hallazgo central:** el segmento Alto Valor concentra el **66.5%** de los clientes "
        "y el **79.1%** del monto acumulado. El segmento 'Activos Estándar' es, en la práctica, "
        "la cartera en riesgo de fuga (recencia media de 250 días).",
        "info",
    )

    # ---------- 2. TAXONOMÍA ----------
    section(2, "Taxonomía de los Cuatro Análisis", "Cada algoritmo responde una pregunta distinta")

    tax = pd.DataFrame({
        "Tipo": ["Descriptivo", "Diagnóstico", "Predictivo", "Prescriptivo"],
        "Pregunta": ["¿Qué sucedió?", "¿Por qué sucedió?", "¿Qué puede suceder?", "¿Qué se debe hacer?"],
        "Algoritmo": ["K-Means", "Isolation Forest", "Prophet", "Apriori"],
        "Pregunta en DHM": [
            "¿Qué tipos de cliente tenemos?",
            "¿En qué fechas las ventas son anómalas?",
            "¿Cuánto se venderá en 90 días?",
            "¿Qué productos conviene ofrecer juntos?",
        ],
        "Archivo de salida": [
            "1_clientes_segmentados.csv",
            "4_anomalias_detectadas.csv",
            "2_prediccion_demanda_prophet.csv",
            "3_combos_apriori.csv",
        ],
    })
    st.dataframe(tax, use_container_width=True, hide_index=True)

    # ---------- 3. ALGORITMOS EN TABS ----------
    section(3, "Resultados por Algoritmo", "Análisis descriptivo, diagnóstico, predictivo y prescriptivo")

    tab_km, tab_if, tab_pr, tab_ap = st.tabs([
        "🔵 K-Means · Descriptivo",
        "🟠 Isolation Forest · Diagnóstico",
        "🟢 Prophet · Predictivo",
        "🟣 Apriori · Prescriptivo",
    ])

    with tab_km:
        _render_kmeans(cli)
    with tab_if:
        _render_isolation(an, pr)
    with tab_pr:
        _render_prophet(pr)
    with tab_ap:
        _render_apriori(co)

    # ---------------------------------------------------------
    # Separador visual para que las siguientes secciones no se
    # sientan "pegadas" a los tabs al hacer scroll
    # ---------------------------------------------------------
    st.divider()

    # ---------- 4. INTEGRACIÓN ----------
    section(4, "Integración del Gemelo Digital", "Cómo se conectan los cuatro algoritmos")
    _render_integracion()

    st.divider()

    # ---------- 5. CONCLUSIONES ----------
    section(5, "Conclusiones y Limitaciones", "Lo que se puede afirmar y lo que falta")
    _render_conclusiones()


# ============================================================
# SUB-VISTAS (TABS)
# ============================================================
def _render_kmeans(cli):
    st.markdown("#### Segmentación de Clientes (RFM)")
    st.caption("Variables: Recencia · Frecuencia · Monto · K=4 · StandardScaler · random_state=42")

    total = len(cli)
    seg = (
        cli.groupby("Segmento_Instacart")
        .agg(
            Clientes=("Cluster", "count"),
            Monto=("Monto", "sum"),
            Recencia=("Recencia", "mean"),
            Frecuencia=("Frecuencia", "mean"),
        )
        .reset_index()
    )
    seg["% Cartera"] = (seg["Clientes"] / total * 100).round(1)
    seg["% Monto"] = (seg["Monto"] / seg["Monto"].sum() * 100).round(1)

    cols = st.columns(len(seg))
    for col, (_, row) in zip(cols, seg.iterrows()):
        nombre = str(row["Segmento_Instacart"])
        kind = "ok" if "Alto" in nombre else ("danger" if "Riesgo" in nombre else "info")
        metric_col(
            col, nombre,
            f"{int(row['Clientes'])} clientes",
            f"{row['% Cartera']}% cartera · {row['% Monto']}% monto",
            kind,
        )

    st.write("") 
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="% Cartera", x=seg["Segmento_Instacart"], y=seg["% Cartera"],
        marker_color="#3b82f6", text=seg["% Cartera"], textposition="outside",
    ))
    fig.add_trace(go.Bar(
        name="% Monto", x=seg["Segmento_Instacart"], y=seg["% Monto"],
        marker_color="#f59e0b", text=seg["% Monto"], textposition="outside",
    ))
    fig.update_layout(barmode="group", title="Participación por segmento", yaxis_title="Porcentaje (%)")
    st.plotly_chart(_dark(fig, 380), use_container_width=True)

    st.write("") 
    fig2 = px.scatter(
        cli, x="Recencia", y="Monto", color="Segmento_Instacart", size="Frecuencia",
        hover_data=["Cluster"], title="Clientes: Recencia vs Monto (tamaño = Frecuencia)",
    )
    st.plotly_chart(_dark(fig2, 420), use_container_width=True)

    st.write("") 
    st.markdown("**Perfil de los segmentos**")
    tabla = seg[["Segmento_Instacart", "Clientes", "% Cartera", "% Monto", "Recencia", "Frecuencia"]].copy()
    tabla.columns = ["Segmento", "Clientes", "% Cartera", "% Monto", "Recencia (días)", "Frecuencia"]
    tabla["Recencia (días)"] = tabla["Recencia (días)"].round(1)
    tabla["Frecuencia"] = tabla["Frecuencia"].round(2)
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.write("") 
    callout(
        "**Advertencia de calidad 1:** el segmento 'En Riesgo (Churn)' no se asignó a ningún clúster. "
        "El umbral de 300 días se aplica al centroide (promedio) y el clúster más rezagado tiene "
        "una recencia media de 250 días. En la práctica, 'Activos Estándar' es la cartera en riesgo: "
        "sus 67 clientes tienen recencias de 150 a 536 días.",
        "warn",
    )


def _render_prophet(pr):
    st.markdown("#### Pronóstico de Demanda a 90 Días")
    st.caption("Estacionalidad anual + semanal · horizonte de 90 días · sin calendario de feriados")

    corte = pd.Timestamp("2026-10-20")
    hist = pr[pr["ds"] <= corte]
    futuro = pr[pr["ds"] > corte].copy()

    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Días histórico", f"{len(hist)}", "20/10/2024 → 20/10/2026", "info")
    metric_col(c2, "Días proyectados", f"{len(futuro)}", "21/10/2026 → 18/01/2027", "ok")
    metric_col(c3, "Demanda diaria", f"{futuro['yhat'].mean():.1f}", "unidades/día", "warn")
    metric_col(c4, "Total proyectado", f"{futuro['yhat'].sum():,.0f}", "unidades en 90 días", "ok")

    st.write("") 
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=hist["ds"], y=hist["yhat"], name="Histórico",
                             line=dict(color="#3b82f6", width=1)))
    fig.add_trace(go.Scatter(x=futuro["ds"], y=futuro["yhat"], name="Proyección",
                             line=dict(color="#22c55e", width=2)))
    fig.add_trace(go.Scatter(x=futuro["ds"], y=futuro["yhat_upper"], name="Optimista",
                             line=dict(color="#22c55e", dash="dot"), fill=None))
    fig.add_trace(go.Scatter(x=futuro["ds"], y=futuro["yhat_lower"], name="Pesimista",
                             line=dict(color="#ef4444", dash="dot"),
                             fill="tonexty", fillcolor="rgba(34,197,94,0.10)"))
    fig.update_layout(title="Pronóstico con banda de incertidumbre (80%)")
    st.plotly_chart(_dark(fig, 440), use_container_width=True)

    st.write("") 
    futuro["dia"] = futuro["ds"].dt.dayofweek
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    semanal = futuro.groupby("dia")["yhat"].mean().reset_index()
    semanal["Día"] = semanal["dia"].map(lambda d: dias[d])

    fig2 = px.bar(semanal, x="Día", y="yhat", color="yhat",
                  color_continuous_scale="Teal",
                  title="Patrón semanal de la proyección a 90 días")
    fig2.update_yaxes(title="Unidades/día")
    st.plotly_chart(_dark(fig2, 340), use_container_width=True)

    st.write("") 
    callout(
        "**Hallazgo:** la demanda de lunes a viernes es de 123-142 unidades, mientras que "
        "sábados (~55) y domingos (~62) caen a menos de la mitad. Planificar con un promedio "
        "plano sobreabastece los fines de semana y subabastece los jueves.",
        "info",
    )

    st.write("") 
    futuro["mes"] = futuro["ds"].dt.to_period("M").astype(str)
    mensual = futuro.groupby("mes").agg(
        Días=("ds", "count"),
        Demanda=("yhat", "sum"),
        Promedio=("yhat", "mean"),
    ).reset_index()
    mensual.columns = ["Mes", "Días en horizonte", "Demanda total", "Promedio diario"]
    mensual["Demanda total"] = mensual["Demanda total"].round(0).astype(int)
    mensual["Promedio diario"] = mensual["Promedio diario"].round(1)
    
    st.markdown("**Proyección por mes**")
    st.dataframe(mensual, use_container_width=True, hide_index=True)

    st.write("") 
    callout(
        "**Advertencia de calidad 2:** el límite inferior es negativo en 188 de 811 días "
        "(artefacto del supuesto de errores normales). Para planificación, truncar en cero "
        "con max(yhat_lower, 0) y considerar estacionalidad multiplicativa.",
        "warn",
    )


def _render_apriori(co):
    st.markdown("#### Reglas de Asociación y Combos")
    st.caption("6 referencias de huevo · min_support=0.01 · lift mínimo 1.0")

    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Reglas totales", f"{len(co)}", "sobre 6 productos", "info")
    metric_col(c2, "Lift máximo", f"{co['lift'].max():.2f}", "asociación fuerte", "ok")
    metric_col(c3, "Lift mediano", f"{co['lift'].median():.2f}", "asociación genuina", "warn")
    metric_col(c4, "Soporte mediano", f"{co['support'].median()*100:.1f}%", "de facturas", "info")

    st.write("") 
    st.markdown("**Top 10 reglas por Lift**")
    top = co.nlargest(10, "lift")[["Antecedente", "Consecuente", "support", "confidence", "lift"]].copy()
    top["support"] = (top["support"] * 100).round(2).astype(str) + "%"
    top["confidence"] = (top["confidence"] * 100).round(1).astype(str) + "%"
    top["lift"] = top["lift"].round(2)
    st.dataframe(top, use_container_width=True, hide_index=True)

    st.write("") 
    fig = px.scatter(
        co, x="confidence", y="lift", size="support", color="lift",
        color_continuous_scale="Purples",
        title="Confianza vs Lift (tamaño = soporte)",
    )
    st.plotly_chart(_dark(fig, 420), use_container_width=True)

    st.write("") 
    formula(
        "Lift (Elevación)",
        r"\text{Lift}(A \Rightarrow B) = \frac{\text{Confianza}(A \Rightarrow B)}{\text{Soporte}(B)} = \frac{P(A \cap B)}{P(A)\,P(B)}",
        "Lift > 1: asociación positiva · Lift = 1: independencia · Lift < 1: sustitución",
    )

    st.write("") 
    callout(
        "**Combos propuestos** (sujetos a validación con facturas reales): "
        "**Dúo Grande** (Blanco Grande + Rojo Grande, conf. 99.6%, lift 2.34) · "
        "**Blanco Familiar** (Blanco Grande + Blanco Mediano, conf. 87.3%, lift 2.14) · "
        "**Surtido Pulpería** (4 referencias, lift 9.13).",
        "ok",
    )

    st.write("") 
    callout(
        "**Advertencia de calidad 3:** el script inyecta 1,000 facturas sintéticas con un patrón "
        "fijo y sin semilla aleatoria. Las reglas son ilustrativas del método y no deben usarse "
        "para lanzar promociones hasta repetir el análisis solo con facturas reales.",
        "danger",
    )


def _render_isolation(an, pr):
    st.markdown("#### Detección de Días Anómalos")
    st.caption("Isolation Forest · contamination=0.02 · random_state=42 · variable única: Cantidad")

    an = an.copy()
    an["tipo"] = np.where(an["Cantidad"] > 200, "Pico", "Caída")
    picos = an[an["tipo"] == "Pico"]
    caidas = an[an["tipo"] == "Caída"]

    c1, c2, c3, c4 = st.columns(4)
    metric_col(c1, "Días anómalos", f"{len(an)}", "2.1% del historial", "warn")
    metric_col(c2, "Picos", f"{len(picos)}", "278 – 438 unidades", "danger")
    metric_col(c3, "Caídas", f"{len(caidas)}", "2 – 6 unidades", "warn")
    metric_col(c4, "Concentración", f"{len(picos)/len(an)*100:.0f}%", "picos sobre total", "info")

    st.write("") 
    fig = px.scatter(
        an, x="ds", y="Cantidad", color="tipo",
        color_discrete_map={"Pico": "#ef4444", "Caída": "#f59e0b"},
        size="Cantidad", title="Días anómalos detectados por Isolation Forest",
    )
    st.plotly_chart(_dark(fig, 420), use_container_width=True)

    st.write("") 
    st.markdown("**Detalle de fechas anómalas**")
    tabla = an[["ds", "Cantidad", "tipo"]].sort_values("ds").copy()
    tabla.columns = ["Fecha", "Cantidad", "Tipo"]
    tabla["Fecha"] = tabla["Fecha"].dt.strftime("%d/%m/%Y")
    st.dataframe(tabla, use_container_width=True, hide_index=True)

    st.write("") 
    callout(
        "**Hallazgo:** los 11 picos (278–438 unidades) superan la banda de Prophet; "
        "las 4 caídas (2–6 unidades) no salen de la banda porque el límite inferior es negativo. "
        "Ambos métodos son complementarios: Isolation Forest detecta extremos globales; "
        "Prophet contextualiza respecto al día de la semana.",
        "info",
    )

    st.write("") 
    callout(
        "**Advertencia de calidad 4:** Isolation Forest es univariado; no conoce el día de la semana. "
        "Un domingo con 60 unidades es normal, pero un miércoles con 60 sería una caída grave. "
        "Las causas deben auditarse caso por caso (facturas, inventario, rutas, feriados).",
        "warn",
    )


# ============================================================
# SECCIONES FINALES (RESTAURADAS)
# ============================================================
def _render_integracion():
    st.markdown(
        "Los cuatro algoritmos corren en **paralelo e independiente**. El Gemelo Digital cobra sentido "
        "cuando las cuatro respuestas se leen en conjunto:\n\n"
        "- **K-Means → Apriori:** calcular reglas por segmento → combos personalizados.\n"
        "- **Prophet ↔ Isolation Forest:** alertas como desviación del pronóstico (residuos).\n"
        "- **K-Means → Prophet:** pronóstico por segmento de cliente.\n"
        "- **K-Means → Isolation Forest:** atribuir picos a clientes y segmentos.\n"
    )

    inter = pd.DataFrame({
        "Interacción": [
            "K-Means → Apriori",
            "Prophet ↔ Isolation Forest",
            "K-Means → Prophet",
            "K-Means → Isolation Forest",
            "Todos → Power BI / Streamlit",
        ],
        "Mecanismo": [
            "Reglas por segmento de cliente",
            "Alertas como residuos del pronóstico",
            "Pronóstico por segmento",
            "Atribuir picos a clientes y segmentos",
            "Visualización conjunta en tablero",
        ],
        "Estado": ["Propuesta", "Propuesta", "Propuesta", "Propuesta", "Implementado"],
        "Requisito": [
            "Agregar cliente a 3_canasta.csv",
            "Calcular residuos y excluir anomalías del entrenamiento",
            "Mantener el cliente en el archivo de demanda",
            "Vincular facturas diarias con clientes",
            "CSV de salida (ya generados)",
        ],
    })
    st.dataframe(inter, use_container_width=True, hide_index=True)

    st.write("") 
    callout(
        "Hoy los cuatro algoritmos corren en paralelo. El siguiente paso es integrarlos: que Apriori "
        "reciba la segmentación, que Isolation Forest use los residuos de Prophet, y que todo se "
        "retroalimente en un simulador de decisiones.",
        "info",
    )


def _render_conclusiones():
    st.markdown(
        "**Lo que el Gemelo Digital ya permite hacer:**\n"
        "- Planificar compras por día de la semana (no con promedio plano).\n"
        "- Identificar a quién proteger (Alto Valor), reactivar (Activos Estándar) y activar (Sensible a Descuento).\n"
        "- Diseñar combos con base en reglas de asociación genuinas (Lift > 2).\n"
        "- Auditar 15 fechas en lugar de revisar miles de registros.\n\n"
        "**Prioridades para la siguiente iteración:**\n"
        "1. Corregir la regla de segmentación para reportar clientes en riesgo (recencia > 300 días a nivel cliente).\n"
        "2. Repetir Apriori solo con facturas reales y semilla fija.\n"
        "3. Truncar bandas de Prophet en cero, agregar feriados y validar exactitud con cross-validation.\n"
        "4. Detectar anomalías sobre residuos del pronóstico (no sobre la serie cruda).\n"
        "5. Integrar los modelos según la matriz de la sección anterior.\n"
    )

    st.write("") 
    callout(
        "El valor del Gemelo Digital no reside en los algoritmos sino en las decisiones que habilitan: "
        "comprar mejor, segmentar mejor, ofrecer mejor y vigilar mejor.",
        "ok",
    )