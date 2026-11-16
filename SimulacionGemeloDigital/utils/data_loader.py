# utils/data_loader.py
from pathlib import Path
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent.parent
RES = BASE / "resultados_ml"

@st.cache_data(ttl=30)
def load_res(nombre):
    p = RES / nombre
    return pd.read_csv(p) if p.exists() else pd.DataFrame()