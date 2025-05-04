import streamlit as st
from gtts import gTTS
import PyPDF2
import uuid
import os
import time

st.set_page_config(page_title="PDF a Audio", layout="centered")
st.title("📄➡️🔊 Convertir PDF a Audio")

# Entrada para nombre del archivo
nombre_audio = st.text_input("📝 Nombre del archivo de audio (sin extensión):", "mi_audio")

# Carga de archivo PDF
archivo_pdf = st.file_uploader("Sube tu archivo PDF", type=["pdf"])

# Selección de idioma
idioma = st.selectbox("🌐 Selecciona el idioma del texto", ["es", "en", "fr", "de", "it"])

if archivo_pdf is not None:
    lector_pdf = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    num_paginas = len(lector_pdf.pages)

    with st.spinner("📄 Extrayendo texto del PDF..."):
        for i, pagina in enumerate(lector_pdf.pages):
            texto += pagina.extract_text()
            time.sleep(0.05)  # Simula tiempo de extracción

    if texto:
        if st.button("🔊 Convertir a Audio"):
            progreso = st.progress(0, text="🎙️ Convirtiendo texto a audio...")
            nombre_unico = f"{nombre_audio}_{uuid.uuid4().hex[:8]}.mp3"

            # Simula carga con barra de progreso
            for i in range(1, 101):
                progreso.progress(i, text=f"🎙️ Convirtiendo... {i}%")
                time.sleep(0.01)  # Simula carga

            tts = gTTS(text=texto, lang=idioma)
            tts.save(nombre_unico)

            st.success("✅ Conversión completada")

            with open(nombre_unico, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(label="⬇️ Descargar Audio", data=audio_bytes, file_name=nombre_unico, mime="audio/mp3")

            os.remove(nombre_unico)
    else:
        st.warning("⚠️ No se pudo extraer texto del PDF.")
