import streamlit as st
from gtts import gTTS
import PyPDF2
import uuid
import os

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
    for pagina in lector_pdf.pages:
        texto += pagina.extract_text()

    if texto:
        if st.button("🔊 Convertir a Audio"):
            # Generar nombre único para el archivo
            nombre_unico = f"{nombre_audio}_{uuid.uuid4().hex[:8]}.mp3"
            tts = gTTS(text=texto, lang=idioma)
            tts.save(nombre_unico)

            # Reproducir audio
            with open(nombre_unico, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(label="⬇️ Descargar Audio", data=audio_bytes, file_name=nombre_unico, mime="audio/mp3")

            # Limpieza opcional del archivo generado
            os.remove(nombre_unico)
    else:
        st.warning("No se pudo extraer texto del PDF.")
