# views/ai_agent.py
import streamlit as st
import pandas as pd
import os
import base64
import io
from freellmpool import Pool
from utils.ui_components import hero, callout
from utils.data_loader import load_res

# --- IMPORTACIONES PARA VOZ ---
from audio_recorder_streamlit import audio_recorder
import speech_recognition as sr
from gtts import gTTS


# ============================================================
# 1. CONSTRUCCIÓN DEL PROMPT MAESTRO (CONOCIMIENTO TOTAL)
# ============================================================
@st.cache_data(show_spinner=False)
def construir_prompt_maestro():
    """
    Construye el contexto definitivo del proyecto combinando:
    1. Conocimiento estático (el informe, reglas de negocio, arquitectura, costos).
    2. Datos dinámicos (lectura en vivo de los CSVs).
    """
    try:
        cli = load_res("1_clientes_segmentados.csv")
        pr = load_res("2_prediccion_demanda_prophet.csv")
        co = load_res("3_combos_apriori.csv")
        an = load_res("4_anomalias_detectadas.csv")

        seg = cli["Segmento_Instacart"].value_counts().to_dict()
        texto_seg = ", ".join([f"{k}: {v} clientes" for k, v in seg.items()])
        total_clientes = len(cli)
        futuro = pr.tail(90)
        demanda_total = futuro["yhat"].sum()
        demanda_diaria = futuro["yhat"].mean()
        total_reglas = len(co)
        lift_max = co["lift"].max()
        lift_med = co["lift"].median()
        total_anomalias = len(an)
    except Exception:
        # Fallback si los CSVs fallan
        texto_seg, total_clientes, demanda_total, demanda_diaria = "Datos no cargados.", 514, 10044, 111.6
        total_reglas, lift_max, lift_med, total_anomalias = 234, 12.47, 2.35, 15

    prompt = f"""
    Eres el **Asistente Analítico Senior y Arquitecto de Datos** del proyecto "DHM Digital Twin". 
    Tu objetivo es responder CUALQUIER pregunta sobre el proyecto con un nivel de precisión mayor al 85%, basándote exclusivamente en la información proporcionada a continuación.

    # 1. CONTEXTO DEL NEGOCIO (Huevos Méndez - DHM)
    - **Empresa:** Distribuidora de huevos en Nicaragua (PyME).
    - **Producto:** Huevos (perecederos de alta rotación). Catálogo de 6 referencias.
    - **Precios y Costos (Supuestos):** Costo promedio C$189/cajilla. Precio de venta promedio C$236/cajilla. Margen bruto promedio C$47/cajilla (aprox 25%).
    - **Problema:** Mermas, quiebres de stock, churn de clientes, tickets bajos y días con ventas anómalas.
    - **Costos del Proyecto (Fase 6):** Inversión inicial C$35,000. Costo recurrente C$28,000/año (o C$5,000 incrementales si el analista ya está en nómina). Ahorro base C$70,000/año. Payback 0.8 años.

    # 2. LA ARQUITECTURA (Inspirada en Instacart)
    - **Personalización (K-Means):** Reemplaza a los Bandidos Contextuales.
    - **Disponibilidad/Forecasting (Prophet):** Reemplaza a XGBoost.
    - **Cross-selling (Apriori):** Reemplaza a Embeddings/Búsqueda Semántica.
    - **Fraude/Anomalías (Isolation Forest):** Reemplaza al "Modeling the Unseen".
    - **Pipeline:** Dos ciclos ETL. 1) `seed_mock_data.py` (SQLite). 2) `01_preparar_datasets.py` (3 CSVs). Los modelos generan 4 CSVs de resultados.

    # 3. RESULTADOS ACTUALES (Datos dinámicos extraídos en vivo)
    - **K-Means:** {total_clientes} clientes. Segmentos: {texto_seg}. *Nota:* "Activos Estándar" es la cartera en riesgo real (recencia 150-536 días). K=4, StandardScaler, random_state=42.
    - **Prophet:** Proyección a 90 días: {demanda_total:,.0f} cajillas. Promedio diario: {demanda_diaria:.1f}. Fuerte estacionalidad semanal (fines de semana caen a la mitad). Bandas negativas truncadas a 0. No usa feriados.
    - **Apriori:** {total_reglas} reglas. Lift máximo: {lift_max:.2f}. Lift mediano: {lift_med:.2f}. Combos giran en torno al Huevo Blanco Grande. *Nota:* El script inyecta 1,000 facturas sintéticas; las reglas son ilustrativas.
    - **Isolation Forest:** {total_anomalias} días anómalos (contamination=0.02). 11 picos de venta (278-438 unidades) y 4 caídas severas (2-6 unidades). *Nota:* Es univariado (no distingue días de la semana).

    # 4. REGLAS ESTRICTAS DE RESPUESTA
    1. **Idioma:** Responde siempre en español, con tono profesional, técnico y ejecutivo.
    2. **Precisión:** Usa los datos dinámicos de arriba para preguntas de negocio.
    3. **Honestidad:** Si algo NO está en este prompt, responde: "Esa información no está documentada en el alcance actual del Gemelo Digital."
    4. **Formato:** Usa viñetas y negritas. Si haces cálculos, muestra el paso a paso.
    5. **Respuestas Cortas (Modo Voz):** Tus respuestas serán leídas en voz alta, así que sé conciso y evita textos excesivamente largos o tablas complejas a menos que se soliciten explícitamente.

    Historial de conversación:
    """
    return prompt


# ============================================================
# 2. FUNCIONES DE VOZ (SIN ERRORES DE WINDOWS)
# ============================================================
def transcribir_audio(audio_bytes):
    """Convierte bytes de audio (WAV) a texto usando Google Speech Recognition."""
    if not audio_bytes:
        return None
    try:
        recognizer = sr.Recognizer()
        # Usar BytesIO en lugar de archivo temporal para evitar WinError 32
        audio_file = io.BytesIO(audio_bytes)
        
        with sr.AudioFile(audio_file) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio_data = recognizer.record(source)
        
        # Idioma español
        texto = recognizer.recognize_google(audio_data, language="es-ES")
        return texto
    except sr.UnknownValueError:
        st.warning("No se pudo entender el audio. Intenta hablar más claro y sin ruido de fondo.")
        return None
    except sr.RequestError as e:
        st.error(f"Error con el servicio de reconocimiento de voz: {e}")
        return None
    except Exception as e:
        st.error(f"Error al procesar el audio: {e}")
        return None


def reproducir_audio(texto):
    """Convierte texto a audio (MP3) en memoria RAM y lo reproduce automáticamente."""
    if not texto:
        return
    try:
        # Limpiar el texto (quitar markdown)
        texto_limpio = texto.replace("*", "").replace("#", "").replace("`", "").replace("_", "")
        if len(texto_limpio) > 600:
            texto_limpio = texto_limpio[:600] + "..."
        
        tts = gTTS(text=texto_limpio, lang="es", slow=False)
        
        # SOLUCIÓN AL WINERROR 32: Usar BytesIO (memoria) en lugar de archivo temporal
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        audio_bytes = fp.getvalue()
        fp.close()

        # Codificar en base64 y usar un tag <audio> con autoplay
        b64 = base64.b64encode(audio_bytes).decode()
        audio_html = f"""
        <audio autoplay controls style="width: 100%; margin-top: 10px;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"No se pudo generar la voz: {e}")


# ============================================================
# 3. INTERFAZ PRINCIPAL DEL AGENTE
# ============================================================
def show():
    hero("Asistente Virtual - Voz y Texto", 
         "Agente Experto en DHM (Modo Alexa)",
         "Consulta por voz o texto. El agente conoce todos los resultados reales del proyecto.",
         "Powered by freellmpool + Google Speech + gTTS")

    # Construir el cerebro del agente
    master_prompt = construir_prompt_maestro()

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "system", "content": master_prompt}]

    # Botón para limpiar conversación
    if st.button("🗑️ Reiniciar Contexto del Agente", type="secondary"):
        st.session_state.messages = [{"role": "system", "content": master_prompt}]
        st.rerun()

    # --- MOSTRAR HISTORIAL ---
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # --- ENTRADA POR VOZ (ALEXA MODE) ---
    st.markdown("---")
    st.markdown("### 🎤 Habla con el Agente")
    audio_bytes = audio_recorder(
        text="Haz clic para hablar",
        recording_color="#e53935",
        neutral_color="#6aa84f",
        icon_name="microphone",
        icon_size="2x",
        key="voice_recorder"
    )

    prompt = None # Variable unificada para texto o voz

    # Si hay audio grabado, transcribir
    if audio_bytes:
        with st.spinner("Transcribiendo audio..."):
            prompt = transcribir_audio(audio_bytes)
            if prompt:
                st.success(f"**Tú dijiste:** {prompt}")

    # --- ENTRADA POR TEXTO (FALLBACK) ---
    if prompt_text := st.chat_input("O escribe tu pregunta aquí..."):
        prompt = prompt_text

    # --- PROCESAMIENTO DEL PROMPT (Voz o Texto) ---
    if prompt:
        # 1. Guardar y mostrar mensaje del usuario
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 2. Generar respuesta del agente
        with st.chat_message("assistant"):
            with st.spinner("Analizando el contexto del Gemelo Digital..."):
                try:
                    pool = Pool.from_default_config()
                    # Unir historial con el master prompt
                    prompt_text_full = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
                    
                    reply_obj = pool.ask(prompt_text_full)
                    reply = reply_obj.text
                    
                    # Mostrar texto
                    st.markdown(reply)
                    # Reproducir la respuesta en voz alta automáticamente
                    reproducir_audio(reply)
                    
                    # Guardar en historial
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error en el pool de APIs: {e}")
                    # Si falla, quitamos la última pregunta del usuario para no corromper el historial
                    st.session_state.messages.pop()