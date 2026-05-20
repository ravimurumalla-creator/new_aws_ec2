import streamlit as st


from bedrock_client import ask_bedrock

st.set_page_config(page_title="Bedrock Chatbot", page_icon="💬", layout="centered")
st.title("Bedrock Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"][0]["text"])

prompt = st.chat_input("Type your message")

if prompt:
    user_msg = {"role": "user", "content": [{"text": prompt}]}
    st.session_state.messages.append(user_msg)

    with st.chat_message("user"):
        st.markdown(prompt)

    history_for_model = st.session_state.messages[:-1]
    reply_text, assistant_msg = ask_bedrock(prompt, history_for_model)

    with st.chat_message("assistant"):
        st.markdown(reply_text)

    if assistant_msg:
        st.session_state.messages.append(assistant_msg)
    else:
        st.session_state.messages.append(
            {"role": "assistant", "content": [{"text": reply_text}]}
        )