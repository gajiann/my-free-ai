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
        with st.spinner("Sedang berpikir..."):
            try:
                # Menghasilkan respon dari Qwen
                outputs = pipe(prompt, max_new_tokens=256, do_sample=True, temperature=0.7)
                response_text = outputs[0]["generated_text"]
                
                # Membersihkan output agar tidak menampilkan ulang teks prompt pengguna
                if response_text.startswith(prompt):
                    response_text = response_text[len(prompt):].strip()
                
                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Terjadi error: {e}")
