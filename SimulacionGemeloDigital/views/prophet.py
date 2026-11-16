# views/prophet.py
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from config import PRECIO_CAJILLA, MARGEN_BRUTO_DEF
from utils.ui_components import hero, section, metric_col, callout, formula, plot_dark, xref
from utils.helpers import caj, monto
from utils.data_loader import load_res

def show():
    _p = load_res("2_prediccion_demanda_prophet.csv")
    
    hero("Instacart Forecasting - Fases 3-4",
         "Prophet - Pronostico de demanda",
         "Instacart predice disponibilidad por articulo. DHM predice demanda diaria en cajillas con banda de confianza.",
         "Taylor & Letham (2018)")

    section("01", "Mini caso didactico - promedio vs por dia de semana",
            "Comprar por promedio semanal destruye margen. Este mini caso lo demuestra con 7 dias.")

    demanda_dias = [
        ("Lunes", 133), ("Martes", 133), ("Miercoles", 136), ("Jueves", 142),
        ("Viernes", 123), ("Sabado", 55), ("Domingo", 62),
    ]
    promedio = sum(d for _, d in demanda_dias) / 7.0

    error_ventas = 0
    error_mermas = 0
    filas_dias = []
    
    for dia, dem in demanda_dias:
        error = int(promedio) - dem
        if error > 0:
            consecuencia = f"Sobran {error} caj (merma)"
            error_mermas += error
        elif error < 0:
            consecuencia = f"Faltan {abs(error)} caj (venta perdida)"
            error_ventas += abs(error)
        else:
            consecuencia = "OK"
            
        filas_dias.append({
            "Dia": dia,
            "Demanda real": dem,
            "Compra por promedio": int(promedio),
            "Error": f"{error:+d}",
            "Consecuencia": consecuencia
        })
    
    df_dias = pd.DataFrame(filas_dias)
    costo_venta_perdida = error_ventas * PRECIO_CAJILLA * (MARGEN_BRUTO_DEF / 100)
    costo_merma = error_mermas * PRECIO_CAJILLA * (1 - MARGEN_BRUTO_DEF / 100)
    costo_total = costo_venta_perdida + costo_merma

    with st.container(border=True):
        st.markdown("**Mini caso didactico**")
        st.markdown(f"DHM debe comprar para los proximos 7 dias. Promedio simple = {int(promedio)} caj/dia.")
        st.dataframe(df_dias, use_container_width=True, hide_index=True)

    c1, c2, c3 = st.columns(3)
    metric_col(c1, "Margen perdido por ventas", monto(costo_venta_perdida), f"{error_ventas} caj faltantes", "neg")
    metric_col(c2, "Costo de merma", monto(costo_merma), f"{error_mermas} caj sobrando", "neg")
    metric_col(c3, "Costo semanal del promedio", monto(costo_total), "por no usar Prophet", "neg")

    st.write("") # Espaciador

    section("02", "La descomposicion aditiva")
    formula(
        "Ec. 1 - Descomposicion aditiva",
        r"y(t) = g(t) + s(t) + h(t) + \varepsilon_t",
        "`g(t)` = tendencia - `s(t)` = estacionalidad semanal y anual - "
        "`h(t)` = feriados (no configurados, h=0) - `epsilon` = ruido.",
    )

    if _p.empty:
        callout("No existe `resultados_ml/2_prediccion_demanda_prophet.csv`.", "danger")
    else:
        section("03", "Simulacion con datos reales")
        df = _p.copy()
        df["ds"] = pd.to_datetime(df["ds"])
        horizonte = st.slider("Horizonte de planificacion (dias)", 7, 90, 30)

        fut = df.tail(horizonte)
        dem_central = float(fut["yhat"].sum())
        dem_opt = float(fut["yhat_upper"].sum())
        dem_pes = float(fut["yhat_lower"].clip(lower=0).sum())
        band_mean = float((fut["yhat_upper"] - fut["yhat_lower"]).mean())

        c1, c2, c3, c4 = st.columns(4)
        metric_col(c1, "Prediccion central", caj(dem_central), f"{horizonte} dias")
        metric_col(c2, "Escenario optimista", caj(dem_opt), "80% superior", "pos")
        metric_col(c3, "Escenario pesimista", caj(dem_pes), "truncado en 0")
        metric_col(c4, "Ancho banda diaria", caj(band_mean), "+/- cajillas/dia")

        ingreso_central = dem_central * PRECIO_CAJILLA
        ingreso_opt = dem_opt * PRECIO_CAJILLA
        ingreso_pes = dem_pes * PRECIO_CAJILLA

        with st.container(border=True):
            st.markdown(f"**Comparacion economica a {monto(PRECIO_CAJILLA)}/cajilla**")
            df_econ = pd.DataFrame({
                "Escenario": ["Pesimista", "Central", "Optimista"],
                "Demanda": [caj(dem_pes), caj(dem_central), caj(dem_opt)],
                "Ingreso proyectado": [monto(ingreso_pes), monto(ingreso_central), monto(ingreso_opt)]
            })
            st.dataframe(df_econ, use_container_width=True, hide_index=True)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["ds"], y=df["yhat_upper"], line=dict(width=0), showlegend=False, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=df["ds"], y=df["yhat_lower"].clip(lower=0), fill="tonexty", fillcolor="rgba(124,58,237,0.20)", line=dict(width=0), name="Banda 80%"))
        fig.add_trace(go.Scatter(x=df["ds"], y=df["yhat"], line=dict(color="#7c3aed", width=2.5), name="Prediccion"))
        fig.update_layout(title="Pronostico con banda de incertidumbre", yaxis_title="Cajillas/dia")
        st.plotly_chart(plot_dark(fig, 450), use_container_width=True)

        neg = int((df["yhat_lower"] < 0).sum())
        if neg > 0:
            callout(
                f"**Banda Negativa:** En **{neg} de {len(df)}** dias el limite inferior es negativo, "
                "fisicamente imposible de vender. Esto ocurre cuando el modelo no esta seguro y la varianza es alta. "
                "Para la planificacion, el sistema ya **trunca automaticamente a 0** los limites negativos, "
                "por lo que no hay riesgo de sobrestock por este motivo. Se recomienda usar el valor central (yhat) para la compra diaria.",
                "warn",
            )

        xref("El pronostico alimenta a **Isolation Forest** (dias fuera de banda = anomalia) y al **What-If** (ROP).")