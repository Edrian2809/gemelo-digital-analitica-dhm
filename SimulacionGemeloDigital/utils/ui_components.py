# utils/ui_components.py
import streamlit as st

def hero(badge, title, subtitle, refs):
    st.markdown(
        f"<div class='hero'><div class='badge'>{badge}</div>"
        f"<h1>{title}</h1><p>{subtitle}</p>"
        f"<div class='refs'>{refs}</div></div>",
        unsafe_allow_html=True,
    )

def section(num, title, subtitle=""):
    st.markdown(
        f"<div class='sec-header'><div class='sec-num'>{num}</div>"
        f"<div class='sec-title'>{title}</div></div>",
        unsafe_allow_html=True,
    )
    if subtitle:
        st.markdown(f"<div class='sec-sub'>{subtitle}</div>", unsafe_allow_html=True)

def metric(label, value, delta=None, delta_class="neu"):
    # st.metric nativo es a prueba de errores React
    st.metric(label=label, value=str(value), delta=str(delta) if delta else None)

def metric_col(col, label, value, delta=None, delta_class="neu"):
    with col:
        metric(label, value, delta, delta_class)

def formula(title, latex, legend):
    st.markdown(f"<div class='formula-title'>{title}</div>", unsafe_allow_html=True)
    st.latex(latex)
    # Usamos blockquote de Markdown para la leyenda, es muy elegante
    st.markdown(f"> *{legend}*")

def callout(text, kind="info"):
    # Limpieza profunda para evitar que Google Translate rompa el HTML
    text = text.replace("<strong>", "**").replace("</strong>", "**")
    text = text.replace("<b>", "**").replace("</b>", "**")
    text = text.replace("<code>", "`").replace("</code>", "`")
    text = text.replace("<br>", "\n\n").replace("<br/>", "\n\n")
    
    if kind == "ok":
        st.success(text, icon="✅")
    elif kind == "warn":
        st.warning(text, icon="⚠️")
    elif kind == "danger":
        st.error(text, icon="🚨")
    else:
        st.info(text, icon="ℹ️")

def xref(text):
    with st.container(border=True):
        st.markdown(f"**🔗 Conexion con otros modelos:** {text}")

def plot_dark(fig, height=400):
    fig.update_layout(
        template="plotly_dark", height=height,
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(19,24,32,0.4)",
        font=dict(color="#e6edf3", size=12),
    )
    return fig
# utils/ui_components.py

def fase_ciclo_vida(numero: int, nombre: str, descripcion: str):
    """
    Muestra un banner indicando la fase del Ciclo de Vida de Data Analytics (Smith, 2021).
    """
    colores = {
        1: "#3b82f6", 2: "#06b6d4", 3: "#8b5cf6", 
        4: "#a855f7", 5: "#10b981", 6: "#f59e0b"
    }
    color = colores.get(numero, "#06b6d4")
    
    html = f"""
    <div style="
        background: linear-gradient(90deg, rgba(13,17,23,0.9) 0%, rgba(13,17,23,0.5) 100%);
        border-left: 4px solid {color};
        border-radius: 4px;
        padding: 12px 20px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        gap: 15px;
        font-family: 'Share Tech Mono', monospace;
    ">
        <div style="
            background-color: {color}20; 
            border: 1px solid {color};
            color: {color}; 
            padding: 5px 10px; 
            border-radius: 4px; 
            font-size: 14px; 
            font-weight: bold;
            white-space: nowrap;
        ">
            FASE {numero}
        </div>
        <div>
            <div style="color: #e6edf3; font-size: 14px; font-weight: bold; letter-spacing: 1px;">
                {nombre.upper()}
            </div>
            <div style="color: #8b949e; font-size: 11px;">
                {descripcion}
            </div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)