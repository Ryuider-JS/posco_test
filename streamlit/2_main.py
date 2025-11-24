import streamlit as st
import requests
import time

# n8n Webhook URL
N8N_URL = "https://choyechoyechoye.app.n8n.cloud/webhook/3ea1fdf8-51f3-43ae-b6aa-03f8334dc81b"

st.set_page_config(page_title="n8n 챗봇", page_icon="🤖")
st.title("🤖 n8n Webhook 기반 챗봇 (스트리밍 + Markdown)")

# 세션 저장
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.chat_input("메시지를 입력하세요")

if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # Webhook 호출
    try:
        params = {"chatInput": user_input, "sessionId": "abc"}
        r = requests.get(N8N_URL, params=params, timeout=60)
        data = r.json()

        if "output" in data:
            bot_reply = data["output"]
        else:
            bot_reply = f"⚠️ 응답에 'output' 키가 없습니다.\n\n받은 데이터: {data}"

    except Exception as e:
        bot_reply = f"❌ 오류 발생: {e}"

    st.session_state.chat_history.append(("bot", bot_reply))

# UI
for role, msg in st.session_state.chat_history:
    if role == "user":
        with st.chat_message("user"):
            st.write(msg)
    else:
        with st.chat_message("assistant"):
            # ===== 스트리밍 + Markdown =====
            container = st.empty()
            streamed_text = ""

            for ch in msg:
                streamed_text += ch
                container.markdown(streamed_text)  # Markdown 렌더링
                time.sleep(0.015)  # 속도 조절
