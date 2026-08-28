import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="AI Assistant + Vision", page_icon="🤖")
st.title("🤖 AI Assistant (Text & Vision)")

# Masukkan API Key
api_key = st.sidebar.text_input("Masukkan Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Fitur Upload Gambar
    uploaded_file = st.sidebar.file_uploader("Unggah Foto (Opsional):", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Foto yang diunggah", use_column_width=True)

    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input Prompt
    if prompt := st.chat_input("Tulis pesan di sini..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Mikir sebentar..."):
                try:
                    if uploaded_file:
                        response = model.generate_content([prompt, image])
                    else:
                        response = model.generate_content(prompt)
                    
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")
else:
    st.info("👈 Silakan masukkan Gemini API Key kamu di sidebar sebelah kiri untuk mulai!")
