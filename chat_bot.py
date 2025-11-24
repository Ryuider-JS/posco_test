from openai import OpenAI
import streamlit as st

st.title("💬 챗봇과 대화를 해보세요")

# 1) secrets → 2) input 순으로 key 설정
if "OPENAI_API_KEY" in st.secrets:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
else:
    openai_api_key = st.text_input("Enter your OpenAI API key", type="password")

if not openai_api_key:
    st.warning("⚠️ OpenAI API 키를 입력해야 챗봇을 사용할 수 있습니다.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# 모델 & 메시지 초기화
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o-mini"

if "messages" not in st.session_state:
    st.session_state.messages = []

# 기존 대화 기록 출력
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 유저 입력
if prompt := st.chat_input("질문을 입력해보세요"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)

    st.session_state.messages.append({"role": "assistant", "content": response})