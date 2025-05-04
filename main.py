import streamlit as st
import PyPDF2
import uuid
import os
import time
import pyttsx3

st.set_page_config(page_title="PDF a Audio", layout="centered")
st.title("📄➡️🔊 Convertir PDF a Audio (Offline)")

nombre_audio = st.text_input("📝 Nombre del archivo de audio (sin extensión):", "mi_audio")
archivo_pdf = st.file_uploader("Sube tu archivo PDF", type=["pdf"])

if archivo_pdf is not None:
    lector_pdf = PyPDF2.PdfReader(archivo_pdf)
    texto = ""
    with st.spinner("📄 Extrayendo texto del PDF..."):
        for pagina in lector_pdf.pages:
            texto += pagina.extract_text()
            time.sleep(0.05)

    if texto:
        if st.button("🔊 Convertir a Audio"):
            progreso = st.progress(0, text="🎙️ Convirtiendo texto a audio...")
            for i in range(1, 101):
                progreso.progress(i, text=f"🎙️ Convirtiendo... {i}%")
                time.sleep(0.01)

            nombre_unico = f"{nombre_audio}_{uuid.uuid4().hex[:8]}.mp3"
            engine = pyttsx3.init()
            engine.save_to_file(texto, nombre_unico)
            engine.runAndWait()

            st.success("✅ Conversión completada")
            with open(nombre_unico, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(label="⬇️ Descargar Audio", data=audio_bytes, file_name=nombre_unico, mime="audio/mp3")

            os.remove(nombre_unico)
    else:
        st.warning("⚠️ No se pudo extraer texto del PDF.")

