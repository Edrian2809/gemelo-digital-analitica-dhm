# views/isolation_forest.py
import streamlit as st
import pandas as pd
import numpy as np
from config import PRECIO_CAJILLA, COSTO_AUDITORIA, COSTO_ANOMALIA_NO_DETECTADA
from utils.ui_components import hero, section, metric_col, callout, formula
from utils.helpers import monto
from utils.data_loader import load_res

def show():
    _a = load_res("4_anomalias_detectadas.csv")
    _p = load_res("2_prediccion_demanda_prophet.csv")

    hero("Instacart Modeling the Unseen - Fases 3-4",
         "Isolation Forest - Deteccion de anomalias",
         "Instacart detecta quiebres invisibles. DHM detecta dias atipicos: fraudes, errores o mermas extraordinarias.",
         "Liu, Ting & Zhou (2008)")

    section("01", "Mini caso didactico - detectar el dia anomalo",
            "7 dias de ventas. Cual es el anomalo? El ojo humano lo ve, pero el algoritmo lo cuantifica y prioriza.")

    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
    valores = [120, 130, 125, 118, 500, 122, 128]

    filas_iso = []
    for dia, v in zip(dias, valores):
        if v == 500:
            score = 0.95
            clas = "ANOMALO (casi seguro)"
        else:
            score = 0.45 + (v - 118) / 200.0
            clas = "Normal"
        filas_iso.append({
            "Dia": dia,
            "Ventas (cajillas)": v,
            "Score aprox.": f"{score:.2f}",
            "Clasificacion": clas
        })

    df_iso = pd.DataFrame(filas_iso)

    with st.container(border=True):
        st.markdown("**Mini caso didactico (scores ilustrativos)**")
        st.markdown("7 dias de ventas. Cual es el anomalo?")
        st.dataframe(df_iso, use_container_width=True, hide_index=True)

    # Texto limpio usando Markdown (sin HTML)
    callout(
        f"**Leccion:** el viernes tiene 500 cajillas cuando el rango normal es 118-130. "
        f"El score es 0.95 = anomalia casi segura. Los demas dias tienen score 0.45-0.55 = normales.\n\n"
        f"Costo de auditar este dia: **{monto(COSTO_AUDITORIA)}**.\n\n"
        f"Si resulta ser un error de facturacion o un fraude, el valor en riesgo es "
        f"**{monto(COSTO_ANOMALIA_NO_DETECTADA)}**. Ratio beneficio/costo: "
        f"**{COSTO_ANOMALIA_NO_DETECTADA/COSTO_AUDITORIA:.1f}x**.",
        "ok",
    )

    section("02", "El score de anomalia")
    formula("Ec. 1 - Score de anomalia", r"s(x,n) = 2^{-\frac{E(h(x))}{c(n)}}", "`s -> 1` = anomalia. `s -> 0.5` = normalidad. `s -> 0` = claramente normal.")
    formula("Ec. 2 - Profundidad esperada", r"c(n) = 2\,H(n-1) - \frac{2(n-1)}{n}", "`H(i)` = numero armonico, aproximado por `ln(i) + 0.577`.")

    if _a.empty:
        callout("No existe `resultados_ml/4_anomalias_detectadas.csv`.", "danger")
    else:
        section("03", "Simulacion con datos reales")
        cont = st.slider("Proporcion esperada de anomalias", 0.005, 0.10, 0.02, 0.005)

        n_total = 721
        n_anom = int(n_total * cont)

        c1, c2, c3, c4 = st.columns(4)
        metric_col(c1, "Anomalias esperadas", n_anom, f"de {n_total} dias")
        metric_col(c2, "Costo de auditar todo", monto(n_anom * COSTO_AUDITORIA), "si todo es FP")
        metric_col(c3, "Valor en riesgo", monto(n_anom * COSTO_ANOMALIA_NO_DETECTADA), "si todo es real")
        metric_col(c4, "Ratio beneficio/costo", f"{COSTO_ANOMALIA_NO_DETECTADA / COSTO_AUDITORIA:.1f}x", "justifica auditar", "pos")

        cajillas_riesgo = COSTO_ANOMALIA_NO_DETECTADA / PRECIO_CAJILLA
        callout(
            f"Cada anomalia real no detectada cuesta **{monto(COSTO_ANOMALIA_NO_DETECTADA)}** = "
            f"**{cajillas_riesgo:.0f} cajillas** no vendidas. "
            f"Auditar un dia cuesta {monto(COSTO_AUDITORIA)}. "
            f"Por cada anomalia real atrapada, el ahorro es "
            f"{COSTO_ANOMALIA_NO_DETECTADA/COSTO_AUDITORIA:.1f}x el costo de auditarla.",
            "info",
        )

        section("04", "Resultados reales y contraste con Prophet")
        if {"ds", "Cantidad"}.issubset(_a.columns):
            anom = _a.copy()
            anom["ds"] = pd.to_datetime(anom["ds"])

            if not _p.empty:
                prop = _p.copy()
                prop["ds"] = pd.to_datetime(prop["ds"])
                merge = anom.merge(prop[["ds", "yhat", "yhat_lower", "yhat_upper"]], on="ds", how="left")
                merge["desv_pct"] = np.where(
                    merge["yhat"] > 0,
                    (merge["Cantidad"] - merge["yhat"]) / merge["yhat"] * 100,
                    0.0
                ).round(1)
                merge["ingreso_afectado"] = ((merge["Cantidad"] - merge["yhat"]).abs() * PRECIO_CAJILLA).round(0)

                st.dataframe(
                    merge[["ds", "Cantidad", "yhat", "desv_pct", "ingreso_afectado"]].round(1),
                    use_container_width=True, hide_index=True,
                )

        callout(
            "**Limitacion.** Isolation Forest no conoce el dia de la semana. "
            "Un sabado con 60 cajillas es normal; un miercoles con 60 seria una caida grave. "
            "Solo marca extremos globales, no desviaciones respecto del patron esperado.",
            "warn",
        )