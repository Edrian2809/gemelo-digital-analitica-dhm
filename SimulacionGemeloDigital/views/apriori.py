# views/apriori.py
import streamlit as st
import pandas as pd
from config import PRECIO_CAJILLA, MARGEN_BRUTO_DEF
from utils.ui_components import hero, section, metric_col, callout, formula
from utils.helpers import monto
from utils.data_loader import load_res

def show():
    _k = load_res("3_combos_apriori.csv")
    
    hero("Instacart Frequently Bought Together - Fases 3-4",
         "Apriori - Reglas de asociacion",
         "Instacart sugiere productos complementarios. DHM descubre que combinaciones de huevo aparecen juntas.",
         "Agrawal & Srikant (1994)")

    section("01", "Mini caso didactico - que ofrecer a un cliente",
            "Un cliente pide 10 cajillas de Huevo Blanco Grande. Que otro producto le ofrecemos?")

    reglas_ejemplo = [
        ("Rojo Grande", 99.6, 2.34, "Ofrecer SIEMPRE"),
        ("Blanco Mediano", 87.3, 2.14, "Ofrecer"),
        ("Rojo Mediano", 81.7, 2.14, "Ofrecer"),
        ("Extra Grande", 35.5, 1.04, "NO ofrecer (elevacion ~1)"),
    ]

    filas_ap = []
    for prod, conf, elev, decision in reglas_ejemplo:
        aceptacion = int(round(10 * conf / 100))
        filas_ap.append({
            "Producto": prod,
            "Confianza": f"{conf:.1f}%",
            "Elevacion": f"{elev:.2f}",
            "Aceptacion esperada": f"~{aceptacion} de 10",
            "Decision": decision
        })

    df_ap = pd.DataFrame(filas_ap)

    with st.container(border=True):
        st.markdown("**Mini caso didactico**")
        st.markdown("Cliente pide 10 cajillas de Huevo Blanco Grande")
        st.dataframe(df_ap, use_container_width=True, hide_index=True)

    ganancia_rojo = int(round(10 * 0.996)) * PRECIO_CAJILLA * (MARGEN_BRUTO_DEF/100)
    ganancia_extra = int(round(10 * 0.355)) * PRECIO_CAJILLA * (MARGEN_BRUTO_DEF/100)

    st.write("") # Espaciador
    callout(
        f"**Leccion:** ofrecer Rojo Grande tiene aceptacion esperada de "
        f"{int(round(10 * 0.996))} de 10 clientes -> ganancia esperada **{monto(ganancia_rojo)}**. "
        f"Ofrecer Extra Grande tiene aceptacion de solo {int(round(10 * 0.355))} de 10 -> **{monto(ganancia_extra)}**. "
        f"La diferencia es {ganancia_rojo/max(ganancia_extra,1):.1f}x. "
        f"Sin Apriori, el vendedor podria ofrecer Extra Grande por intuicion y perder la mayor parte de la ganancia.",
        "ok",
    )

    section("02", "Las tres metricas")
    formula("Ec. 1 - Soporte", r"\text{Soporte}(A \Rightarrow B) = \frac{|A \cup B|}{|D|}", "Proporcion de facturas con A y B juntos.")
    formula("Ec. 2 - Confianza", r"\text{Confianza}(A \Rightarrow B) = \frac{\text{Soporte}(A \cup B)}{\text{Soporte}(A)} = P(B \mid A)", "Probabilidad de B dado A.")
    formula("Ec. 3 - Elevacion", r"\text{Elevacion}(A \Rightarrow B) = \frac{P(A \cap B)}{P(A)\,P(B)}", "Elevacion > 1: asociacion positiva. = 1: independencia. < 1: sustitucion. (lift)")

    if _k.empty:
        callout("No existe `resultados_ml/3_combos_apriori.csv`.", "danger")
    else:
        section("03", "Simulacion con datos reales")
        kk = _k.copy()
        if "lift" in kk.columns and "elevacion" not in kk.columns:
            kk = kk.rename(columns={"lift": "elevacion"})

        umbral = st.slider("Umbral de elevacion minimo", 1.0, 5.0, 1.5, 0.1)

        if "elevacion" in kk.columns:
            reglas_altas = kk[kk["elevacion"] >= umbral].sort_values("elevacion", ascending=False)
            reglas_bajas = kk[(kk["elevacion"] >= 1.0) & (kk["elevacion"] < 1.5)]

            c1, c2, c3 = st.columns(3)
            metric_col(c1, "Reglas sobre umbral", len(reglas_altas))
            metric_col(c2, "Reglas con elevacion baja", len(reglas_bajas), "zona de ruido", "neg")
            metric_col(c3, "Elevacion maxima", f"{float(kk['elevacion'].max()):.2f}")

            st.write("") # Espaciador
            if len(reglas_bajas) > 0:
                callout(
                    f"**El costo de promocionar mal:** si ofreces un descuento del 10% sobre "
                    f"{len(reglas_bajas)} combos con elevacion baja, pierdes ~10% de margen "
                    f"en compras que ya ocurririan por azar. Ejemplo: 100 combos de 25 cajillas a "
                    f"{monto(PRECIO_CAJILLA)} = {monto(100*25*PRECIO_CAJILLA)} de ingreso. El 10% de descuento son "
                    f"**{monto(100*25*PRECIO_CAJILLA*0.10)} de margen perdido sin venta incremental**.",
                    "warn",
                )

            cols_show = [c for c in ["Antecedente", "Consecuente", "support", "confidence", "elevacion"] if c in reglas_altas.columns]
            if len(reglas_altas) > 0:
                st.dataframe(reglas_altas[cols_show], use_container_width=True, hide_index=True)
            else:
                callout("Con este umbral no hay reglas. Baja el slider para ver mas.", "warn")

        if "elevacion" in kk.columns and len(kk) > 0:
            top = kk.sort_values("elevacion", ascending=False).iloc[0]
            ant = str(top.get("Antecedente", "?"))
            con = str(top.get("Consecuente", "?"))
            conf = float(top.get("confidence", 0))
            elev = float(top.get("elevacion", 1))
            sup_b = conf / elev if elev > 1e-6 else 0.0

            with st.container(border=True):
                st.markdown("**Regla mas fuerte - calculo paso a paso**")
                df_top = pd.DataFrame({
                    "Metrica": ["Regla", "Confianza", "Elevacion", "Base esperada (Soporte B)", "Efecto incremental"],
                    "Valor": [
                        f"{ant} -> {con}",
                        f"{conf*100:.2f}%",
                        f"{elev:.2f}x",
                        f"{sup_b*100:.2f}%",
                        f"{(conf - sup_b)*100:.1f} puntos porcentuales"
                    ]
                })
                st.dataframe(df_top, use_container_width=True, hide_index=True)

        st.write("") # Espaciador
        callout(
            "**Advertencia.** El script inyecta facturas con patrones artificiales antes de Apriori. "
            "Las reglas son demostracion metodologica, no comportamiento real.",
            "danger",
        )