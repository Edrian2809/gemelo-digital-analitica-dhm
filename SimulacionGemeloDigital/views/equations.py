# views/equations.py
import streamlit as st
from utils.ui_components import hero, formula

def show():
    hero("Referencia matematica", "Ecuaciones completas",
         "Formulas con leyenda, interpretacion y fuente.",
         "Lloyd (1982) - Taylor & Letham (2018) - Agrawal & Srikant (1994) - Liu, Ting & Zhou (2008)")

    tabs = st.tabs(["K-Means (5)", "Prophet (6)", "Apriori (6)", "Isolation Forest (3)", "Negocio (5)"])

    with tabs[0]:
        formula("Ec. 1 - Estandarizacion", r"z_{ij} = \frac{x_{ij}-\bar{x}_j}{s_j}", "Transforma cada variable a media 0 y desviacion 1.")
        formula("Ec. 2 - Funcion objetivo", r"J = \sum_{i=1}^{n}\sum_{k=1}^{K} w_{ik}\,\left\|x_i - \mu_k\right\|^2", "Suma de distancias al cuadrado al centroide.")
        formula("Ec. 3 - Paso de asignacion", r"C_i = \underset{k}{\arg\min}\,\left\|z_i - \mu_k\right\|^2", "Cada cliente al centroide mas cercano.")
        formula("Ec. 4 - Paso de actualizacion", r"\mu_k = \frac{1}{|C_k|}\sum_{z_i \in C_k} z_i", "Centroide = media de sus miembros.")
        formula("Ec. 5 - Coeficiente de silueta", r"s(i) = \frac{b(i) - a(i)}{\max\left(a(i),b(i)\right)}", "Valida calidad del agrupamiento. En DHM: 0.335 con K=4.")

    with tabs[1]:
        formula("Ec. 6 - Descomposicion aditiva", r"y(t) = g(t) + s(t) + h(t) + \varepsilon_t", "Tendencia + estacionalidad + feriados + ruido.")
        formula("Ec. 7 - Tendencia lineal por tramos", r"g(t) = (k + a(t)^T\delta)\,t + (m + a(t)^T\gamma)", "Cambios de pendiente en puntos de cambio.")
        formula("Ec. 8 - Tendencia logistica", r"g(t) = \frac{C}{1+\exp(-k(t-m))}", "Saturacion con capacidad C.")
        formula("Ec. 9 - Estacionalidad Fourier", r"s(t) = \sum_{n=1}^{N}\left(a_n\cos\frac{2\pi n t}{P} + b_n\sin\frac{2\pi n t}{P}\right)", "P = 7 (semanal) o 365.25 (anual).")
        formula("Ec. 10 - Feriados", r"h(t) = Z(t)\,\kappa", "Matriz de indicadores por evento. El script no configura feriados.")
        formula("Ec. 11 - Error", r"\varepsilon_t \sim \mathcal{N}(0, \sigma^2)", "Causa de que la banda pueda ser negativa.")

    with tabs[2]:
        formula("Ec. 12 - Soporte A", r"\text{Soporte}(A) = \frac{\left|\{T \in D : A \subseteq T\}\right|}{|D|}", "Proporcion de facturas que contienen A.")
        formula("Ec. 13 - Soporte conjunto", r"\text{Soporte}(A \Rightarrow B) = P(A \cap B)", "Proporcion de facturas con A y B.")
        formula("Ec. 14 - Confianza", r"\text{Confianza}(A \Rightarrow B) = \frac{P(A \cap B)}{P(A)} = P(B \mid A)", "Probabilidad condicional. Asimetrica.")
        formula("Ec. 15 - Elevacion", r"\text{Elevacion}(A \Rightarrow B) = \frac{P(A \cap B)}{P(A)\,P(B)}", "Tambien llamada lift en la literatura. =1: independencia. mayor a 1: asociacion.")
        formula("Ec. 16 - Conviction", r"\text{Conviction}(A \Rightarrow B) = \frac{1-P(B)}{1-\text{Confianza}(A \Rightarrow B)}", "Cuantas veces falla la regla vs independencia.")
        formula("Ec. 17 - Antimonotona", r"X \subseteq Y \Rightarrow \text{Soporte}(X) \geq \text{Soporte}(Y)", "Base de la eficiencia del algoritmo.")

    with tabs[3]:
        formula("Ec. 18 - Score", r"s(x,n) = 2^{-\frac{E(h(x))}{c(n)}}", "s -> 1: anomalia. s -> 0.5: normal. s -> 0: claramente normal.")
        formula("Ec. 19 - Camino esperado", r"c(n) = 2\,H(n-1) - \frac{2(n-1)}{n}", "Normaliza por tamano de muestra.")
        formula("Ec. 20 - Armonico", r"H(i) \approx \ln(i) + 0.5772156649", "Constante de Euler-Mascheroni = 0.577.")

    with tabs[4]:
        formula("Ec. 21 - Elasticidad", r"\%\Delta Q = \varepsilon \cdot \%\Delta P", "Aproximacion lineal. Huevo: eps entre -0.6 y -1.0.")
        formula("Ec. 22 - Utilidad simulada", r"U_{sim} = I_{sim} \cdot m_{nuevo}", "La utilidad importa, no el ingreso. Combo -10% con margen 15% deja solo 5.56%.")
        formula("Ec. 23 - Margen nuevo con ajuste de precio", r"m_{nuevo} = \frac{m + \Delta P}{1 + \Delta P}", "Formula exacta del margen tras un cambio de precio. Si el descuento supera el margen, el resultado es negativo (perdida).")
        formula("Ec. 24 - ROP", r"\text{ROP} = \bar{d}\cdot L + z_{\alpha}\,\sigma_d\sqrt{L}", "Segundo termino = safety stock.")
        formula("Ec. 25 - EOQ", r"\text{EOQ} = \sqrt{\frac{2DS}{H}}", "Minimiza costos de orden y almacenamiento.")