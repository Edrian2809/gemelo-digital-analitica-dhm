# views/what_if.py
import streamlit as st
import pandas as pd
import numpy as np
from config import PRECIO_CAJILLA, MARGEN_BRUTO_DEF
from utils.ui_components import hero, section, metric_col, callout
from utils.helpers import monto, caj, margen_ajustado
from utils.data_loader import load_res

def show():
    _p = load_res("2_prediccion_demanda_prophet.csv")

    hero("Instacart Prescriptive - Fase 6",
         "Simulador What-If",
         "Convierte resultados del gemelo digital en decisiones cuantificadas. Precio de referencia: " + monto(PRECIO_CAJILLA) + "/cajilla.",
         "Ciclo de Vida Fase 6")

    section("01", "Mini caso didactico - subir precio vs bajar precio",
            "Dos estrategias opuestas sobre el mismo cliente. Una gana, la otra destruye utilidad.")

    costo_unit = PRECIO_CAJILLA * (1 - MARGEN_BRUTO_DEF/100)
    util_base = 100 * (PRECIO_CAJILLA - costo_unit)

    precio_A = PRECIO_CAJILLA * 1.05
    dem_A = int(round(100 * (1 - 0.8*0.05)))
    util_A = dem_A * (precio_A - costo_unit)

    precio_B = PRECIO_CAJILLA * 0.90
    dem_B = int(round(100 * 1.15))
    util_B = dem_B * (precio_B - costo_unit)

    # Reemplazo de la tabla HTML por un DataFrame nativo
    df_mini = pd.DataFrame({
        "Estrategia": ["Base", "Subir precio 5%", "Combo -10% +15% vol"],
        "Demanda": [100, dem_A, dem_B],
        "Precio": [monto(PRECIO_CAJILLA), monto(precio_A), monto(precio_B)],
        "Ingreso": [monto(100*PRECIO_CAJILLA), monto(dem_A*precio_A), monto(dem_B*precio_B)],
        "Margen unit.": [monto(PRECIO_CAJILLA-costo_unit), monto(precio_A-costo_unit), monto(precio_B-costo_unit)],
        "Utilidad": [monto(util_base), monto(util_A), monto(util_B)],
        "Veredicto": ["-", f"RENTABLE (+{monto(util_A-util_base)})", f"DESTRUYE (-{monto(util_base-util_B)})"]
    })

    with st.container(border=True):
        st.markdown("### Mini caso didactico")
        st.markdown(f"**Cliente compra 100 cajillas. Precio {monto(PRECIO_CAJILLA)}, margen {MARGEN_BRUTO_DEF}%**")
        st.dataframe(df_mini, use_container_width=True, hide_index=True)

    st.write("") # Espaciador
    callout(
        f"**Leccion clave:** ambas opciones suben ingreso, pero solo la primera sube UTILIDAD. "
        f"Con margen del {MARGEN_BRUTO_DEF}%, un descuento del 10% deja solo "
        f"{monto(PRECIO_CAJILLA*0.90 - costo_unit)} de margen por cajilla ("
        f"{(PRECIO_CAJILLA*0.90 - costo_unit)/(PRECIO_CAJILLA*0.90)*100:.2f}%). "
        f"Aunque vendas 15% mas, la utilidad cae {monto(util_base-util_B)}. "
        f"**El ingreso engana, la utilidad decide.**",
        "warn",
    )

    if _p.empty:
        callout("Se necesita el pronostico de Prophet para simular.", "danger")
    else:
        section("02", "Simulacion con datos reales")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            delta_p = st.slider("Ajuste de precio (%)", -25, 25, 0) / 100
        with c2:
            eps = st.slider("Elasticidad precio-demanda", -2.0, -0.2, -0.8, 0.1,
                            help="Huevo (commodity) suele tener elasticidad entre -0.6 y -1.0.")
        with c3:
            precio = st.number_input("Precio por cajilla (C\$)", 1.0, 1000.0, PRECIO_CAJILLA, 1.0)
        with c4:
            margen = st.slider("Margen bruto (%)", 5, 40, MARGEN_BRUTO_DEF) / 100

        c5, c6, c7 = st.columns(3)
        with c5:
            stock_act = st.number_input("Stock actual (cajillas)", 0.0, 100000.0, 800.0, 10.0)
        with c6:
            lead = st.slider("Lead time (dias)", 1, 15, 3)
        with c7:
            nivel_serv = st.select_slider("Nivel de servicio", [0.80, 0.85, 0.90, 0.95, 0.99], value=0.95)

        z_map = {0.80: 0.84, 0.85: 1.04, 0.90: 1.28, 0.95: 1.65, 0.99: 2.33}
        z = z_map[nivel_serv]

        p = _p.copy()
        p["ds"] = pd.to_datetime(p["ds"])
        futuro = p.tail(90)
        D = float(futuro["yhat"].sum())
        band_mean = float((futuro["yhat_upper"] - futuro["yhat_lower"]).mean())
        d_diario = D / 90.0
        sigma_d = band_mean / 2.5632

        safety = z * sigma_d * np.sqrt(lead)
        rop = d_diario * lead + safety

        D_new = max(0.0, D * (1 + eps * delta_p))
        R_base = D * precio
        R_new = D_new * (1 + delta_p) * precio
        delta_R = R_new - R_base

        margen_nuevo = margen_ajustado(margen, delta_p)
        U_base = R_base * margen
        U_new = R_new * margen_nuevo
        delta_U = U_new - U_base

        with st.expander("Trazabilidad de calculos paso a paso"):
            st.markdown("### Demanda")
            df_dem = pd.DataFrame({
                "Variable": ["Suma de yhat (90 dias)", "Demanda diaria (D/90)", "Ancho banda (80%)", "Sigma diaria"],
                "Valor": [f"{D:,.0f} cajillas", f"{d_diario:.2f} caj/dia", f"{band_mean:.2f} caj/dia", f"{sigma_d:.2f} caj/dia"]
            })
            st.dataframe(df_dem, hide_index=True, use_container_width=True)

            st.markdown("### Punto de reorden")
            df_rop = pd.DataFrame({
                "Variable": [f"z para nivel {nivel_serv*100:.0f}%", "Lead time", "Safety stock", "Demanda en lead time", "ROP Final"],
                "Valor": [f"{z:.2f}", f"{lead} dias", f"{safety:.0f} cajillas", f"{d_diario*lead:.0f} cajillas", f"{rop:.0f} cajillas"]
            })
            st.dataframe(df_rop, hide_index=True, use_container_width=True)

            st.markdown("### Escenario comercial")
            df_com = pd.DataFrame({
                "Variable": ["D nueva = D * (1 + eps * dP)", "Ingreso base = D * P", "Ingreso nuevo", "Margen nuevo %", "Utilidad base", "Utilidad nueva"],
                "Valor": [f"{D_new:,.0f} cajillas", monto(R_base), monto(R_new), f"{margen_nuevo*100:.2f}%", monto(U_base), monto(U_new)]
            })
            st.dataframe(df_com, hide_index=True, use_container_width=True)

        section("03", "Resultado comercial")
        c1, c2, c3 = st.columns(3)
        metric_col(c1, "Demanda base 90d", caj(D), "cajillas")
        delta_cls = "pos" if delta_R >= 0 else "neg"
        metric_col(c2, "Ingreso simulado", monto(R_new),
                   "{:+,.0f} C\$ vs base".format(delta_R), delta_cls)
        u_cls = "pos" if delta_U >= 0 else "neg"
        metric_col(c3, "Utilidad simulada", monto(U_new),
                   "{:+,.0f} C\$ vs base".format(delta_U), u_cls)

        st.write("") # Espaciador
        if delta_U > 0:
            callout(
                f"**DECISION: EJECUTAR.** Ajuste del {delta_p*100:+.0f}% "
                f"aumenta utilidad en **{monto(delta_U)}** en 90 dias. "
                f"La demanda cae {caj(abs(D_new - D))} pero el mayor margen compensa.",
                "ok",
            )
        else:
            callout(
                f"**DECISION: NO EJECUTAR.** Ajuste del {delta_p*100:+.0f}% "
                f"reduce utilidad en **{monto(abs(delta_U))}**. "
                f"La caida de volumen supera el beneficio del mayor precio.",
                "danger",
            )

        section("04", "Resultado operativo - punto de reorden")
        c1, c2, c3 = st.columns(3)
        metric_col(c1, "Demanda diaria", "{:.1f} caj/dia".format(d_diario), "cajillas")
        metric_col(c2, "Safety stock", "{:.0f} caj".format(safety), "z=" + str(z))
        metric_col(c3, "Punto de reorden", "{:.0f} caj".format(rop), "lead " + str(lead) + "d")

        st.write("") # Espaciador
        if stock_act < rop:
            gap = rop - stock_act
            dias_rest = stock_act / d_diario if d_diario > 0 else 0
            venta_perdida = max(0, lead - dias_rest) * d_diario * precio
            callout(
                f"**ALERTA.** Stock ({stock_act:.0f} caj) esta {gap:.0f} cajillas por debajo del ROP. "
                f"Quiebre estimado en {dias_rest:.1f} dias. "
                f"Ventas perdidas por lead time: **{monto(venta_perdida)}**. Emitir orden hoy.",
                "danger",
            )
        else:
            exc = stock_act - rop
            dias_cub = stock_act / d_diario if d_diario > 0 else 0
            callout(
                f"**OK.** Stock supera el ROP por {exc:.0f} cajillas, "
                f"cubriendo {dias_cub:.1f} dias. Sin reposicion inmediata.",
                "ok",
            )

        section("05", "Comparacion de tres escenarios")
        costo_cajilla = precio * (1 - margen)
        escenarios_data = [
            ("Base", D, precio, margen),
            ("Subir precio 5%", D*(1+eps*0.05), precio*1.05, margen_ajustado(margen, 0.05)),
            ("Combo -10% +15% vol", D*(1+eps*(-0.10))*(1+0.15), precio*0.90, margen_ajustado(margen, -0.10)),
        ]
        filas = []
        for nombre, _D, _P, _m in escenarios_data:
            _I = _D * _P
            _U = _I * _m
            filas.append({
                "Escenario": nombre,
                "Demanda": "{:,.0f} caj".format(_D),
                "Precio": monto(_P),
                "Ingreso": monto(_I),
                "Margen": "{:.2f}%".format(_m*100),
                "Utilidad": monto(_U),
                "Delta utilidad": "{:+,.0f} C\$".format(_U - U_base),
            })
        st.dataframe(pd.DataFrame(filas), use_container_width=True, hide_index=True)

        util_combo = escenarios_data[2][1] * escenarios_data[2][2] * escenarios_data[2][3]
        if util_combo < U_base and margen > 0.10:
            pct_vol_requerido = (margen / (margen - 0.10) - 1) * 100
            callout(
                f"**Leccion del combo:** con margen {margen*100:.0f}%, "
                f"un descuento del 10% requiere que el volumen suba al menos "
                f"{pct_vol_requerido:.0f}% solo para empatar la utilidad. "
                f"Con +15% volumen la utilidad cae {monto(U_base - util_combo)}. "
                f"El combo solo es rentable si el volumen sube mas o si el descuento es menor.",
                "warn",
            )
        elif margen <= 0.10 and delta_p < 0:
            callout(
                f"**Leccion del combo:** con margen {margen*100:.1f}%, "
                f"un descuento del 10% es matematicamente imposible de recuperar. "
                f"El margen queda por debajo del descuento. No aplicar.",
                "danger",
            )