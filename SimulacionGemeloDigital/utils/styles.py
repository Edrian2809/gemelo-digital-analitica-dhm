# utils/styles.py
CSS = '''
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&display=swap');

:root { --bg:#0a0f18; --card:#111827; --border:#1f2937; --text:#e6edf3; --dim:#8b949e;
        --neon-cyan:#06b6d4; --neon-purple:#a78bfa; --ok:#10b981; --warn:#f59e0b; --bad:#ef4444; }

.stApp { background: #0a0f18; background-image: radial-gradient(circle at 50% 0%, rgba(6, 182, 212, 0.05) 0%, transparent 50%); }
.block-container { padding-top:1.2rem; max-width:1400px; }

/* TIPOGRAFÍA TECNOLÓGICA */
h1, h2, h3, h4, .sec-title { font-family: 'Rajdhani', sans-serif !important; letter-spacing: 1px; }
.mono, .metric-value, .price-value { font-family: 'Share Tech Mono', monospace !important; }

/* HERO */
.hero { background:linear-gradient(135deg,rgba(6,182,212,0.1),rgba(167,139,250,0.05));
        border:1px solid rgba(6,182,212,0.3); border-radius:8px; padding:26px 30px; margin-bottom:22px;
        box-shadow: 0 0 20px rgba(6,182,212,0.05); }
.hero h1 { color:var(--text); font-size:28px; margin:0 0 8px 0; text-transform: uppercase; }
.hero p { color:var(--dim); font-size:14px; margin:0; line-height:1.6; }
.hero .badge { display:inline-block; background:rgba(6,182,212,0.15); border:1px solid var(--neon-cyan);
               color:var(--neon-cyan); font-size:10px; font-weight:700; padding:3px 10px; border-radius:4px;
               letter-spacing:0.1em; text-transform:uppercase; margin-bottom:10px; box-shadow: 0 0 10px rgba(6,182,212,0.3); }

/* SECCIONES */
.sec-header { display:flex; align-items:center; gap:12px; margin:28px 0 6px 0;
              padding-bottom:10px; border-bottom:1px solid var(--border); }
.sec-num { width:30px; height:30px; background:rgba(6,182,212,0.1); border: 1px solid var(--neon-cyan);
           border-radius:4px; display:flex; align-items:center; justify-content:center;
           font-family:'Share Tech Mono', monospace; font-weight:700; font-size:12px; color:var(--neon-cyan); }
.sec-title { font-size:22px; font-weight:700; color:var(--text); text-transform: uppercase; }

/* =========================================
   DISEÑO TECNOLÓGICO DEL SIDEBAR (HUD)
   ========================================= */

/* Fondo del sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #06090f 100%) !important;
    border-right: 1px solid rgba(6, 182, 212, 0.2) !important;
}

/* Ocultar los círculos de radio */
div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* Estilo de los botones del menú (HUD) */
div[data-testid="stRadio"] > div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-left: 3px solid transparent;
    border-radius: 4px;
    padding: 12px 15px !important;
    margin-bottom: 6px;
    transition: all 0.2s ease-in-out;
    cursor: pointer;
}

/* Efecto Hover (Neón Cyan) */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
    background: rgba(6, 182, 212, 0.05);
    border-left: 3px solid var(--neon-cyan);
    box-shadow: inset 0 0 10px rgba(6, 182, 212, 0.1);
}

/* Texto del menú */
div[data-testid="stRadio"] > div[role="radiogroup"] > label p {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #8b949e !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Estado Seleccionado (Neón Cyan Brillante) */
div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, rgba(6,182,212,0.15) 0%, transparent 100%);
    border-left: 3px solid var(--neon-cyan);
    box-shadow: inset 0 0 15px rgba(6, 182, 212, 0.1);
}

div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) p {
    color: var(--neon-cyan) !important;
    text-shadow: 0 0 8px rgba(6, 182, 212, 0.5);
}

/* Separador de secciones */
.sidebar-divider {
    margin: 20px 0;
    border-top: 1px dashed rgba(6, 182, 212, 0.2);
}

/* Tarjeta de estado del pipeline (Consola) */
.pipeline-status-card {
    background: rgba(13, 17, 23, 0.8);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 6px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    position: relative;
}

.pipeline-status-card::before {
    content: 'SYS.STATUS';
    position: absolute;
    top: -8px; left: 10px;
    background: #0d1117;
    padding: 0 5px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: var(--neon-cyan);
    letter-spacing: 1px;
}

.status-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    margin-top: 10px;
}

.status-item {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--dim);
    font-family: 'Share Tech Mono', monospace;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    animation: pulse 2s infinite;
}

.status-dot.ok { background: var(--ok); box-shadow: 0 0 8px var(--ok); }
.status-dot.bad { background: var(--bad); box-shadow: 0 0 8px var(--bad); }

@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
}

/* Tarjeta de precio (Terminal Financiera) */
.price-card {
    background: linear-gradient(180deg, rgba(6,182,212,0.05), rgba(13,17,23,0));
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 6px;
    padding: 15px;
    text-align: center;
    position: relative;
}

.price-card::before {
    content: 'PRICE.FEED';
    position: absolute;
    top: -8px; left: 10px;
    background: #0d1117;
    padding: 0 5px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 9px;
    color: var(--neon-cyan);
    letter-spacing: 1px;
}

.price-value {
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    margin: 5px 0;
    text-shadow: 0 0 10px rgba(255,255,255,0.2);
}
</style>
'''