# views/kmeans.py
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from utils.ui_components import hero, section, metric_col, callout, formula, plot_dark, xref, fase_ciclo_vida
from utils.helpers import monto
from utils.data_loader import load_res

def show():
    _c = load_res("1_clientes_segmentados.csv")
    fase_ciclo_vida(4, "Construcción del Modelo", "Ejecución del algoritmo K-Means (Fase 3: Planificación, K=4). Aplicación de la función de inercia.")
    hero("Instacart Personalization - Fases 3-4",
         "K-Means - Segmentacion de clientes",
         "Instacart decide que mostrar a cada usuario. DHM decide a quien proteger, reactivar o descontar.",
         "Lloyd (1982) - Hartigan & Wong (1979) - Rousseeuw (1987)")

    section("01", "Mini caso didactico - clasificar un cliente nuevo",
            "Un cliente nuevo llega a DHM. Con 3 datos lo clasificamos en un segmento y definimos la accion comercial.")

    col_m1, col_m2, col_m3 = st.columns(3)
    with col_m1:
        rec_m = st.slider("Recencia (dias)", 0, 365, 60, key="km_rec")
    with col_m2:
        fre_m = st.slider("Frecuencia (compras)", 0, 20, 8, key="km_fre")
    with col_m3:
        mon_m = st.slider("Monto (C$)", 0, 80000, 25000, step=500, key="km_mon")

    centroides = {
        "Alto Valor":            (54.7, 7.9, 23725),
        "Alto Valor Premium":    (54.5, 11.6, 36777),
        "Sensible a Descuento":  (71.1, 4.1, 11331),
        "En Riesgo (funcional)": (250.1, 6.6, 20138),
    }
    escalas = (250.0, 20.0, 80000.0)
    distancias = {}
    for nombre, (r, f, m) in centroides.items():
        dr = (rec_m - r) / escalas[0]
        df_ = (fre_m - f) / escalas[1]
        dm = (mon_m - m) / escalas[2]
        distancias[nombre] = float(np.sqrt(dr*dr + df_*df_ + dm*dm))

    asignado = min(distancias, key=distancias.get)
    accion_map = {
        "Alto Valor": "Ejecutivo de cuenta. Mantener sin descuento agresivo.",
        "Alto Valor Premium": "Maxima prioridad. Frecuencia 11.6. Proteccion total.",
        "Sensible a Descuento": "Promocion por volumen o recompra. Vigilar margen.",
        "En Riesgo (funcional)": "Reactivacion inmediata. Investigar causa antes de descontar.",
    }

    # DISEÑO PREMIUM: Contenedor nativo con título en Markdown
    with st.container(border=True):
        st.markdown("### 🎯 Clasificacion en tiempo real")
        st.markdown(f"**Perfil evaluado:** Recencia **{rec_m}** dias | Frecuencia **{fre_m}** compras | Monto **C$ {mon_m:,.0f}**")
        
        df_distancias = pd.DataFrame(list(distancias.items()), columns=["Segmento", "Distancia Euclidiana"])
        df_distancias = df_distancias.sort_values("Distancia Euclidiana").reset_index(drop=True)
        df_distancias["Estado"] = df_distancias["Segmento"].apply(lambda x: "✅ MAS CERCANO" if x == asignado else "")
        
        st.dataframe(df_distancias, use_container_width=True, hide_index=True)

    callout(
        f"**Clasificacion Final:** {asignado}\n\n"
        f"**Accion recomendada:** {accion_map[asignado]}\n\n"
        "**Sin el algoritmo:** DHM trataria a este cliente igual que a todos, "
        "perdiendo la oportunidad de actuar con la estrategia correcta.",
        "ok",
    )

    section("02", "La formula y su lectura de negocio")
    formula(
        "Ec. 1 - Funcion objetivo",
        r"J = \sum_{i=1}^{n}\sum_{k=1}^{K} w_{ik}\,\left\|x_i - \mu_k\right\|^2",
        "n = clientes | K = clusters | x_i = vector estandarizado | mu_k = centroide. Minimizar J significa agrupar clientes similares.",
    )

    if _c.empty:
        callout("No existe `resultados_ml/1_clientes_segmentados.csv`.", "danger")
    else:
        section("03", "Simulacion completa con datos reales")
        K = st.slider("Numero de clusters K", 2, 8, 4, key="km_k")
        sil_ref = {2: 0.343, 3: 0.351, 4: 0.335, 5: 0.348, 6: 0.294, 7: 0.298, 8: 0.280}
        inercia_ref = {2: 942.4, 3: 693.4, 4: 529.9, 5: 451.7, 6: 392.0, 7: 349.3, 8: 317.9}
        sil = sil_ref[K]
        inercia = inercia_ref[K]

        c1, c2, c3 = st.columns(3)
        metric_col(c1, "Inercia (SSE)", f"{inercia:.1f}", "menor = mas compacto")
        metric_col(c2, "Silueta media", f"{sil:.3f}", "mayor = mejor separacion")
        metric_col(c3, "Clusters", K, "vs 4 recomendado")

        if "Segmento_Instacart" in _c.columns:
            agg = _c.groupby("Segmento_Instacart").agg(
                Clientes=("Cluster", "count"),
                Recencia=("Recencia", "mean"),
                Frecuencia=("Frecuencia", "mean"),
                Monto=("Monto", "mean"),
            ).round(1).reset_index()
            agg["Pct"] = (100 * agg["Clientes"] / agg["Clientes"].sum()).round(1)
            st.dataframe(agg, use_container_width=True, hide_index=True)

        if {"Recencia", "Monto"}.issubset(_c.columns):
            fig = px.scatter(
                _c, x="Recencia", y="Monto",
                color="Segmento_Instacart" if "Segmento_Instacart" in _c.columns else None,
                size="Frecuencia",
                color_discrete_sequence=["#7c3aed", "#06b6d4", "#10b981", "#f59e0b"],
            )
            fig.update_layout(title="Distribucion real de clientes")
            st.plotly_chart(plot_dark(fig, 450), use_container_width=True)

        section("04", "Consecuencia cuantificada")
        if "Monto" in _c.columns and "Segmento_Instacart" in _c.columns:
            _c_clean = _c.dropna(subset=["Recencia", "Monto"])
            if "En Riesgo (Churn)" in _c_clean["Segmento_Instacart"].values:
                en_riesgo = _c_clean[_c_clean["Segmento_Instacart"] == "En Riesgo (Churn)"]
            else:
                en_riesgo = _c_clean.nlargest(max(1, int(len(_c_clean)*0.13)), "Recencia")
            monto_riesgo = float(en_riesgo["Monto"].sum())

            with st.container(border=True):
                st.markdown("### 📊 Analisis de Riesgo de Churn")
                df_escenarios = pd.DataFrame({
                    "Concepto": ["Clientes en riesgo", "Ingreso en juego", "Costo / Inversion", "Recuperacion esperada", "Resultado Neto"],
                    "Escenario A (No actuar)": [len(en_riesgo), monto(monto_riesgo), "$0", "$0", f"-{monto(monto_riesgo*0.4)}"],
                    "Escenario B (Reactivar)": [len(en_riesgo), monto(monto_riesgo), monto(monto_riesgo*0.08), monto(monto_riesgo*0.25), monto(monto_riesgo*0.25 - monto_riesgo*0.08)]
                })
                st.dataframe(df_escenarios, use_container_width=True, hide_index=True)
                st.caption("Nota: El Escenario A asume una tasa de perdida del 40% a 12 meses. El Escenario B aplica una campana con 25% de recuperacion.")

        xref("El segmento Alto Valor alimenta al **What-If** para decidir a quien ofrecer descuentos sin erosionar margen.")