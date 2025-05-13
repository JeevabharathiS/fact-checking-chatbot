import streamlit as st
import requests

st.set_page_config(page_title="Sindoor-Scout.Ai", page_icon="🤖")
st.title("Sindoor-Scout.Ai")
st.markdown("Ask anything related to the current war or conflict between India and Pakistan to verify facts.")

API_URL = "http://127.0.0.1:8000/ask"


if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


user_input = st.chat_input("Ask your question...")

if user_input:
    if user_input and isinstance(user_input, str):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
    else:
        st.error("Please enter a valid question.")
        st.stop()

    valid_messages = []
    for msg in st.session_state.messages:
        if (
            isinstance(msg, dict)
            and "role" in msg
            and "content" in msg
            and isinstance(msg["role"], str)
            and isinstance(msg["content"], str)
        ):
            valid_messages.append({"role": msg["role"], "content": msg["content"]})
        else:
            st.error("Invalid message format detected.")
            st.stop()

    try:
        payload = {"messages": valid_messages}
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            answer = response.json().get("answer", "No response received.")
        else:
            st.error(f"Error from backend: {response.status_code}")
            st.write(response.json())
            answer = "Failed to get a response."
    except Exception as e:
        answer = f"Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)