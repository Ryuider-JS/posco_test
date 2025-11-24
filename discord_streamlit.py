import streamlit as st
import requests
import time
from datetime import datetime

# n8n Webhook URL
N8N_URL = "https://choyechoyechoye.app.n8n.cloud/webhook/3ea1fdf8-51f3-43ae-b6aa-03f8334dc81b"

# Discord 스타일 CSS
st.markdown("""
<style>
    /* 전체 배경 */
    .stApp {
        background-color: #36393f;
    }
    
    /* 사이드바 스타일 */
    [data-testid="stSidebar"] {
        background-color: #2f3136;
    }
    
    /* 메인 영역 */
    .main .block-container {
        background-color: #36393f;
        padding: 0;
        max-width: 100%;
    }
    
    /* 컬럼 스타일 */
    [data-testid="column"] {
        background-color: #2f3136;
        padding: 0;
    }
    
    /* 컬럼 내부 스타일 */
    .element-container {
        padding: 0;
    }
    
    /* 채팅 영역 스타일 */
    .chat-container {
        background-color: #36393f;
        min-height: calc(100vh - 200px);
        max-height: calc(100vh - 200px);
        overflow-y: auto;
        padding: 20px;
    }
    
    /* 메시지 스타일 */
    .message-wrapper {
        display: flex;
        padding: 8px 16px;
        margin: 4px 0;
        color: #dcddde;
    }
    
    .message-wrapper:hover {
        background-color: #32353b;
    }
    
    .message-avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: linear-gradient(135deg, #5865f2, #7289da);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 16px;
        flex-shrink: 0;
    }
    
    .message-content {
        flex: 1;
    }
    
    .message-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }
    
    .message-author {
        font-weight: 500;
        color: #ffffff;
        font-size: 16px;
    }
    
    .message-timestamp {
        color: #72767d;
        font-size: 12px;
    }
    
    .message-text {
        color: #dcddde;
        font-size: 16px;
        line-height: 1.375;
        word-wrap: break-word;
    }
    
    /* 채널 목록 스타일 */
    .channel-item {
        padding: 6px 8px;
        margin: 2px 0;
        border-radius: 4px;
        color: #96989d;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 16px;
    }
    
    .channel-item:hover {
        background-color: #3c3f44;
        color: #dcddde;
    }
    
    .channel-item.active {
        background-color: #3c3f44;
        color: #ffffff;
    }
    
    .channel-category {
        color: #8e9297;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        padding: 8px 8px 4px;
        margin-top: 16px;
    }
    
    /* 사용자 목록 스타일 */
    .user-item {
        padding: 6px 8px;
        margin: 2px 0;
        border-radius: 4px;
        color: #96989d;
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 14px;
    }
    
    .user-status {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #43b581;
    }
    
    /* 입력 영역 */
    .stChatInput {
        background-color: #40444b !important;
        border-radius: 8px;
    }
    
    .stChatInput > div > div {
        background-color: #40444b !important;
    }
    
    .stChatInput input {
        background-color: #40444b !important;
        color: #dcddde !important;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        background-color: #3c3f44;
        color: #96989d;
        border: none;
        border-radius: 4px;
        padding: 6px 8px;
        text-align: left;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3c3f44;
        color: #dcddde;
    }
    
    /* 스크롤바 스타일 */
    .chat-container::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-container::-webkit-scrollbar-track {
        background: #2f3136;
    }
    
    .chat-container::-webkit-scrollbar-thumb {
        background: #202225;
        border-radius: 4px;
    }
    
    /* 헤더 스타일 */
    .channel-header {
        background-color: #36393f;
        border-bottom: 1px solid #202225;
        padding: 16px 20px;
        display: flex;
        align-items: center;
        gap: 8px;
        color: #ffffff;
        font-size: 16px;
        font-weight: 600;
    }
    
    /* 활동 영역 */
    .activity-section {
        padding: 16px;
        border-bottom: 1px solid #202225;
    }
    
    .activity-title {
        color: #8e9297;
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    
    .activity-item {
        padding: 8px;
        color: #dcddde;
        font-size: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="n8n 챗봇",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 저장
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "selected_channel" not in st.session_state:
    st.session_state.selected_channel = "전체_운영문의"
if "message_timestamps" not in st.session_state:
    st.session_state.message_timestamps = []

# 3단 레이아웃: 왼쪽 사이드바, 중앙 채팅, 오른쪽 사이드바
col1, col2, col3 = st.columns([3, 7, 3])

# 왼쪽 사이드바 - 채널 목록
with col1:
    st.markdown("""
    <div style="background-color: #2f3136; min-height: 100vh; padding: 12px; display: flex; flex-direction: column;">
        <div style="padding: 12px; border-bottom: 1px solid #202225; margin-bottom: 12px;">
            <h3 style="color: #ffffff; margin: 0; font-size: 16px;">25-2차 포스코그룹 AI활용전문가 과정</h3>
        </div>
        <div class="channel-category">채팅 채널</div>
    </div>
    """, unsafe_allow_html=True)
    
    channels = ["전체_공지", "전체_운영문의", "전체_학습문의", "전체_자유"]
    for channel in channels:
        active_class = "active" if channel == st.session_state.selected_channel else ""
        icon = "🔊" if channel == st.session_state.selected_channel else "#"
        if st.button(f"{icon} {channel}", key=f"channel_{channel}", use_container_width=True):
            st.session_state.selected_channel = channel
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
    <div style="padding: 8px; color: #dcddde; font-size: 14px; background-color: #292b2f; border-radius: 4px; margin-top: auto;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 32px; height: 32px; border-radius: 50%; background: linear-gradient(135deg, #5865f2, #7289da); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold;">사</div>
            <div>
                <div style="color: #ffffff; font-weight: 500;">사무계 강사 조예찬</div>
                <div style="color: #43b581; font-size: 12px;">온라인</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 중앙 채팅 영역
with col2:
    st.markdown(f'<div class="channel-header"># {st.session_state.selected_channel}</div>', unsafe_allow_html=True)
    
    # 채팅 컨테이너
    chat_display = st.container()
    with chat_display:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # 채팅 히스토리 표시
        if st.session_state.chat_history:
            for idx, (role, msg) in enumerate(st.session_state.chat_history):
                if role == "user":
                    author = "사용자"
                    avatar_text = "사"
                else:
                    author = "봇"
                    avatar_text = "봇"
                
                # 저장된 타임스탬프 사용
                if idx < len(st.session_state.message_timestamps):
                    timestamp = st.session_state.message_timestamps[idx].strftime("%Y년 %m월 %d일 %H:%M")
                else:
                    timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
                
                # 마지막 봇 메시지인 경우 스트리밍 효과 적용
                if role == "bot" and idx == len(st.session_state.chat_history) - 1:
                    message_placeholder = st.empty()
                    streamed_text = ""
                    for ch in msg:
                        streamed_text += ch
                        message_placeholder.markdown(f"""
                        <div class="message-wrapper">
                            <div class="message-avatar">{avatar_text}</div>
                            <div class="message-content">
                                <div class="message-header">
                                    <span class="message-author">{author}</span>
                                    <span class="message-timestamp">{timestamp}</span>
                                </div>
                                <div class="message-text">{streamed_text}</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        time.sleep(0.015)
                else:
                    st.markdown(f"""
                    <div class="message-wrapper">
                        <div class="message-avatar">{avatar_text}</div>
                        <div class="message-content">
                            <div class="message-header">
                                <span class="message-author">{author}</span>
                                <span class="message-timestamp">{timestamp}</span>
                            </div>
                            <div class="message-text">{msg}</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; color: #72767d; padding: 40px;">
                <p>아직 메시지가 없습니다. 첫 메시지를 보내보세요!</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# 오른쪽 사이드바 - 활동 및 사용자 목록
with col3:
    st.markdown("""
    <div style="background-color: #2f3136; height: 100vh; padding: 0; overflow-y: auto;">
        <div class="activity-section">
            <div class="activity-title">활동 - 3</div>
            <div class="activity-item">🎮 Wordle - 2일 전</div>
            <div class="activity-item">💻 Comet - 43:08:02 연속 57일</div>
            <div class="activity-item">💻 Comet - 2일 전 (인기)</div>
        </div>
        <div class="activity-section">
            <div class="activity-title">온라인 - 5</div>
            <div class="user-item"><span class="user-status"></span>강수혁(기술계 코치)</div>
            <div class="user-item"><span class="user-status"></span>사무계 강사 조예찬</div>
            <div class="user-item"><span class="user-status"></span>이승호(기술계)</div>
            <div class="user-item"><span class="user-status"></span>임대건(기술계 코치)</div>
            <div class="user-item"><span class="user-status"></span>콥스랩-류태선</div>
        </div>
        <div class="activity-section">
            <div class="activity-title">오프라인 - 65</div>
            <div style="max-height: 300px; overflow-y: auto;">
                <div class="user-item">RyanPo</div>
                <div class="user-item">강민우(기술계)</div>
                <div class="user-item">강요섭(사무계)</div>
                <div class="user-item">강형근(사무계)</div>
                <div class="user-item">고미송(사무계코치)</div>
                <div class="user-item">권민지</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 메시지 입력 (전체 너비)
user_input = st.chat_input(f"# {st.session_state.selected_channel}에 메시지 보내기")

if user_input:
    current_time = datetime.now()
    st.session_state.chat_history.append(("user", user_input))
    st.session_state.message_timestamps.append(current_time)

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

    bot_time = datetime.now()
    st.session_state.chat_history.append(("bot", bot_reply))
    st.session_state.message_timestamps.append(bot_time)
    st.rerun()
