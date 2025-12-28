import streamlit as st
import google.generativeai as genai 

# --- 1. CẤU HÌNH HÌNH ẢNH (BẠN TỰ CHÈN LINK VÀO ĐÂY) ---
URL_NEN = "https://i.postimg.cc/PrRBjTQH/background.jpg"
URL_AVATAR_VONG_KINH = "https://i.postimg.cc/rF3YHgqp/Vong-Kinh.jpg"
URL_AVATAR_DIEM_HOA = "https://i.postimg.cc/KcVNczww/Diem-Hoa.jpg"
MY_API_KEY = "AIzaSyCzAV4GVbt4DbQlh-O2oagYlhHvV5BSoys" 

# --- 2. CẤU HÌNH GIAO DIỆN (UI) ---
st.set_page_config(page_title="Lưu Viêm Kì Lục", layout="centered") 

st.markdown(f"""
    <style>
    /* Nền toàn trang */
    .stApp {{
        background: url("{URL_NEN}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    /* Khung chat của Vọng Kính (Assistant) */
    .vong-kinh-box {{
        background-color: rgba(255, 255, 255, 0.1); 
        border-left: 4px solid #add8e6;
        padding: 15px;
        border-radius: 5px;
        color: #ffffff;
        font-family: 'Times New Roman', serif;
        text-shadow: 1px 1px 2px black;
    }}
    /* Khung chat của Diễm Họa (User) */
    .diem-hoa-box {{
        background-color: rgba(60, 0, 0, 0.4);
        border-right: 4px solid #ff4b4b;
        padding: 15px;
        border-radius: 5px;
        color: #ffffff;
        text-align: right;
    }}
    h1 {{
        color: #ffffff !important;
        text-shadow: 0px 0px 15px #ffffff;
        text-align: center;
        font-family: 'Georgia', serif;
    }}
    </style>
    """, unsafe_allow_html=True) 

st.title("❄️ LƯU VIÊM KÌ LỤC")
st.markdown("<p style='text-align: center; color: #add8e6;'>Băng Thanh Ngọc Khiết - Vô Tình Đạo</p>", unsafe_allow_html=True) 

# --- 3. CẤU HÌNH LINH HỒN AI (IDENTITY) ---
genai.configure(api_key=MY_API_KEY) 

if "chat" not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.session_state.chat = model.start_chat(history=[])
    # Identity chuẩn theo yêu cầu của bạn
    st.session_state.identity = (
        "Bạn là Tiên Tôn Vọng Kính. Tâm tính như băng thanh ngọc khiết, là đóa sen tuyết không nhiễm bụi trần. "
        "Bạn tu Vô Tình Đạo, lấy việc thực thi chính đạo làm lẽ sống. "
        "Ngoại hình: Y phục bào y nhạt màu, cấm dục. Mái tóc dài buộc gọn gàng, chỉnh chu. "
        "Khí chất: Cao lãnh băng khiết, xa cách như trăng dưới nước. "
        "Tính cách: Quy tắc, cứng nhắc, phân định rõ đúng sai theo thiên luật. Lãnh khốc, sẵn sàng xử tử kẻ gây họa. "
        "Kiêu ngạo bậc thánh nhân nhìn thấu nhân quả. "
        "Đối với Diễm Họa: Tôn trọng vì là đối thủ xứng tầm (Kỳ phùng địch thủ). Thấu hiểu qua từng nhịp kiếm. Tuyệt đối không vì tư tình. "
        "Quy tắc phản hồi: Xưng Ta - Ngươi. Ngôn ngữ cổ phong, lạnh lùng, súc tích, không nói đùa."
    ) 

# --- 4. XỬ LÝ TIN NHẮN ---
if "messages" not in st.session_state:
    st.session_state.messages = [] 

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar=URL_AVATAR_VONG_KINH):
            st.markdown(f"<div class='vong-kinh-box'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("user", avatar=URL_AVATAR_DIEM_HOA):
            st.markdown(f"<div class='diem-hoa-box'>{msg['content']}</div>", unsafe_allow_html=True) 

# Nhập liệu
user_input = st.chat_input("Rút kiếm đi, Diễm Họa...") 

if user_input:
    # Hiển thị tin nhắn người dùng
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Gửi tới AI
    full_prompt = f"{st.session_state.identity}\n\nDiễm Họa: {user_input}"
    response = st.session_state.chat.send_message(full_prompt)
    
    # Lưu tin nhắn AI
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()
