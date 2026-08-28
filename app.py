import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Chatbot Free", page_icon="🤖")
st.title("🤖 AI Assistant (Free & No Captcha)")

# Memuat model AI secara memori-efisien
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")

pipe = load_model()

# Simpan riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tampilkan riwayat chat di layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input dari pengguna
if prompt := st.chat_input("Tulis pesan di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        messages = [{"role": "user", "content": prompt}]
        outputs = pipe(messages, max_new_tokens=200, temperature=0.7)
        response = outputs[0]["generated_text"][-1]["content"]
        st.markdown(response)
        
    st.session_state.messages.append({"role": "assistant", "content": response})
