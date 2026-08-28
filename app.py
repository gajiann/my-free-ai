import streamlit as st
from transformers import pipeline

st.set_page_config(page_title="AI Chatbot Free", page_icon="🤖")
st.title("🤖 GhazyAI (ZyBot)")

@st.cache_resource
def load_model():
    return pipeline("text-generation", model="Qwen/Qwen2.5-0.5B-Instruct")

pipe = load_model()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tulis pesan di sini..."):
    # Instruksi sistem agar Qwen bertindak sebagai asisten yang cerdas dan akurat
    system_prompt = "System: Kamu adalah asisten AI yang cerdas, sangat pintar, akurat, dan menjawab dalam bahasa Indonesia yang baik, benar, dan informatif.\n\n"
    full_prompt = system_prompt + f"User: {prompt}\nAssistant:"
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Sedang berpikir..."):
            try:
                outputs = pipe(
                    full_prompt, 
                    max_new_tokens=256, 
                    do_sample=True, 
                    temperature=0.4, 
                    top_p=0.85,
                    return_full_text=False
                )
                response_text = outputs[0]["generated_text"].strip()
                
                # Membersihkan sisa tag jika ada
                if "User:" in response_text:
                    response_text = response_text.split("User:")[0].strip()

                st.markdown(response_text)
                st.session_state.messages.append({"role": "assistant", "content": response_text})
            except Exception as e:
                st.error(f"Terjadi error: {e}")
