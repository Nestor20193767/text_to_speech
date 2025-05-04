import streamlit as st
from PyPDF2 import PdfReader
from gtts import gTTS
from pydub import AudioSegment
import uuid
import os
import io
import tempfile
import math

st.title("📄➡️🔊 Convertir PDF a Audio (Gratis con gTTS)")
st.info("Funciona en fragmentos para evitar errores de gTTS.")

nombre_audio = st.text_input("Nombre del archivo de audio:", "mi_audio")
archivo_pdf = st.file_uploader("Sube tu archivo PDF", type="pdf")

def dividir_texto(texto, max_chars=1000):
    partes = []
    while len(texto) > max_chars:
        corte = texto[:max_chars].rfind(".") + 1
        if corte == 0:
            corte = max_chars
        partes.append(texto[:corte])
        texto = texto[corte:]
    partes.append(texto)
    return partes

if archivo_pdf is not None:
    lector = PdfReader(archivo_pdf)
    texto = ""
    for pagina in lector.pages:
        texto += pagina.extract_text() or ""

    if st.button("🔊 Convertir a audio"):
        partes = dividir_texto(texto)
        st.info(f"Texto dividido en {len(partes)} fragmentos...")

        audio_final = AudioSegment.empty()
        progress = st.progress(0)
        status = st.empty()

        for i, parte in enumerate(partes):
            status.text(f"Procesando fragmento {i + 1} de {len(partes)}...")
            tts = gTTS(text=parte, lang="es")
            temp_fp = io.BytesIO()
            tts.write_to_fp(temp_fp)
            temp_fp.seek(0)
            audio_segment = AudioSegment.from_file(temp_fp, format="mp3")
            audio_final += audio_segment
            progress.progress((i + 1) / len(partes))

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            audio_final.export(f.name, format="mp3")
            with open(f.name, "rb") as a:
                st.audio(a.read(), format="audio/mp3")
                st.download_button("⬇️ Descargar Audio", a, f"{nombre_audio}.mp3", mime="audio/mp3")

        progress.empty()
        status.text("✅ Conversión completa")
