import streamlit as st
import ollama
import re

st.set_page_config(page_title="ChatGPT Clone", page_icon="🤖", layout="centered")

st.title("🤖 ChatGPT Clone (Ollama Streaming)")

# CSS styling bubble chat
st.markdown("""
<style>
.user-msg {
    background-color: #DCF8C6;
    color: #111;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.ai-msg {
    background-color: #F1F0F0;
    color: #111;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# tampilkan history chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>👤 **You:**<br>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-msg'>🤖 **AI:**<br>{msg['content']}</div>", unsafe_allow_html=True)

# input baru dari user
if prompt := st.chat_input("Tulis pesan..."):
    # simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.markdown(f"<div class='user-msg'>👤 **You:**<br>{prompt}</div>", unsafe_allow_html=True)

    # container kosong untuk menampilkan streaming
    with st.chat_message("assistant"):
        ai_placeholder = st.empty()
        full_response = ""

        # streaming respons dari ollama
        for chunk in ollama.chat(
            model="deepseek-r1",  # bisa ganti model lain
            messages=st.session_state.messages,
            stream=True
        ):
            content = chunk["message"]["content"]
            full_response += content

            # sembunyikan teks berpikir <think>...</think>
            clean_response = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL)

            # tampilkan teks bersih yang sudah terkumpul
            ai_placeholder.markdown(
                f"<div class='ai-msg'>🤖 **AI:**<br>{clean_response.strip()}</div>",
                unsafe_allow_html=True
            )

    # simpan jawaban ke history
    st.session_state.messages.append({"role": "assistant", "content": clean_response.strip()})
