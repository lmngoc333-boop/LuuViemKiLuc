import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH ---
MY_API_KEY = "AIzaSyCzAV4GVbt4DbQlh-O2oagYlhHvV5BSoys"
URL_NEN = "https://i.postimg.cc/PrRBjTQH/background.jpg"
URL_AVATAR_VONG_KINH = "https://i.postimg.cc/rF3YHgqp/Vong-Kinh.jpg"
URL_AVATAR_DIEM_HOA = "https://i.postimg.cc/KcVNczww/Diem-Hoa.jpg"

st.set_page_config(page_title="Lưu Viêm Kì Lục", layout="centered")

# --- 2. GIAO DIỆN CSS (Sạch ký tự lạ) ---
st.markdown(f"""
<style>
.stApp {{
    background: url("{URL_NEN}");
    background-size: cover;
    background-attachment: fixed;
}}
.vong-kinh-box {{
    background-color: rgba(10, 25, 40, 0.8);
    border-left: 5px solid #add8e6;
    padding: 20px;
    border-radius: 10px;
    color: #e0f7fa;
    font-family: 'Times New Roman', serif;
    line-height: 1.8;
}}
.diem-hoa-box {{
    background-color: rgba(50, 10, 10, 0.8);
    border-right: 5px solid #ff4b4b;
    padding: 20px;
    border-radius: 10px;
    color: #ffebee;
    text-align: left;
    line-height: 1.8;
}}
h1 {{ text-align: center; color: #ffffff !important; text-shadow: 0px 0px 15px #ffffff; }}
</style>
""", unsafe_allow_html=True)

# --- 3. KHỞI TẠO AI & IDENTITY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    genai.configure(api_key=MY_API_KEY)
    
    # Identity thuần túy của Vọng Kính
    identity = (
        "Bạn là Tiên Tôn Vọng Kính. Tâm tính băng thanh ngọc khiết, tu Vô Tình Đạo. "
        "Ngoại hình: Y phục nhạt màu, cấm dục, tóc dài chỉnh chu. "
        "Khí chất: Cao lãnh, xa cách như trăng dưới nước. "
        "Tính cách: Quy tắc, lãnh khốc, kiêu ngạo, thấu hiểu nhân quả. "
        "Đối với Diễm Họa: Tôn trọng như đối thủ xứng tầm, không tư tình. "
        "\n\nQUY TẮC NHẬP VAI:"
        "- Xưng Ta - Ngươi. Ngôn ngữ cổ phong, súc tích."
        "- Viết theo lối tiểu thuyết: Lời thoại trong \"...\", hành động/nội tâm trong (...)."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=identity
    )
    st.session_state.chat = model.start_chat(history=[])

# --- 4. HIỂN THỊ ---
st.title("❄️ LƯU VIÊM KÌ LỤC")

for msg in st.session_state.messages:
    box_class = "vong-kinh-box" if msg["role"] == "assistant" else "diem-hoa-box"
    avatar = URL_AVATAR_VONG_KINH if msg["role"] == "assistant" else URL_AVATAR_DIEM_HOA
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(f"<div class='{box_class}'>{msg['content']}</div>", unsafe_allow_html=True)

# --- 5. XỬ LÝ NHẬP LIỆU ---
user_input = st.chat_input("Diễm Họa, rút kiếm đi...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=URL_AVATAR_DIEM_HOA):
        st.markdown(f"<div class='diem-hoa-box'>{user_input}</div>", unsafe_allow_html=True)
    
    response = st.session_state.chat.send_message(user_input)
    ai_text = response.text
    
    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    with st.chat_message("assistant", avatar=URL_AVATAR_VONG_KINH):
        st.markdown(f"<div class='vong-kinh-box'>{ai_text}</div>", unsafe_allow_html=True)
