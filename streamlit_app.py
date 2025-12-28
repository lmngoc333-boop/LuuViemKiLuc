import streamlit as st
import google.generativeai as genai

# --- 1. CẤU HÌNH ---
MY_API_KEY = "AIzaSyCzAV4GVbt4DbQlh-O2oagYlhHvV5BSoys" 
URL_NEN = "https://i.postimg.cc/PrRBjTQH/background.jpg"
URL_AVATAR_VONG_KINH = "https://i.postimg.cc/rF3YHgqp/Vong-Kinh.jpg"
URL_AVATAR_DIEM_HOA = "https://i.postimg.cc/KcVNczww/Diem-Hoa.jpg"

st.set_page_config(page_title="Lưu Viêm Kì Lục - Roleplay", layout="centered")

# --- 2. GIAO DIỆN CSS (Tối ưu cho đọc truyện) ---
st.markdown(f"""
    <style>
    .stApp {{
        background: url("{URL_NEN}");
        background-size: cover;
        background-attachment: fixed;
    }}
    /* Box của Vọng Kính - Màu xanh thanh khiết */
    .vong-kinh-box {{
        background-color: rgba(15, 25, 35, 0.8); 
        border-left: 5px solid #add8e6;
        padding: 20px;
        border-radius: 10px;
        color: #e0f7fa;
        font-family: 'Times New Roman', serif;
        line-height: 1.8;
        font-size: 1.1rem;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }}
    /* Box của Diễm Họa - Màu đỏ trầm */
    .diem-hoa-box {{
        background-color: rgba(45, 10, 10, 0.8);
        border-right: 5px solid #ff4b4b;
        padding: 20px;
        border-radius: 10px;
        color: #ffebee;
        font-family: 'Times New Roman', serif;
        line-height: 1.8;
        font-size: 1.1rem;
        text-align: left;
    }}
    h1 {{ text-align: center; color: #ffffff !important; text-shadow: 0px 0px 15px #ffffff; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. KHỞI TẠO LINH HỒN AI (ROLEPLAY IDENTITY) ---
if "chat" not in st.session_state:
    genai.configure(api_key=MY_API_KEY)
    
    # Thiết lập danh phận và cách hành văn tiểu thuyết
    identity_prompt = (
        "Bạn là Tiên Tôn Vọng Kính. Một bậc thánh nhân tu Vô Tình Đạo, tâm tính như băng thanh ngọc khiết, là đóa sen tuyết không nhiễm bụi trần. "
        "\n\nNGOẠI HÌNH & KHÍ CHẤT:"
        "- Y phục bào y nhạt màu, cấm dục. Mái tóc dài buộc gọn gàng, chỉnh chu."
        "- Khí chất cao lãnh băng khiết, xa cách như trăng dưới nước."
        "\n\nTÍNH CÁCH:"
        "- Quy tắc & Cứng nhắc: Phân định rõ đúng sai theo thiên luật, không ngoại lệ cho tình cảm."
        "- Lãnh khốc: Sẵn sàng xử tử kẻ gây họa để bảo vệ đại cục."
        "- Kiêu ngạo: Bậc thánh nhân nhìn thấu nhân quả."
        "\n\nĐỐI VỚI DIỄM HỌA:"
        "- Tôn trọng vì là đối thủ xứng tầm ('Kỳ phùng địch thủ'). Thấu hiểu qua từng nhịp kiếm. Tuyệt đối không vì tư tình."
        "\n\nQUY TẮC NHẬP VAI (ROLEPLAY):"
        "- Xưng hô: Ta - Ngươi."
        "- Ngôn ngữ: Cổ phong, lạnh lùng, súc tích, không nói đùa."
        "- Cách viết: Viết theo lối văn phong tiểu thuyết tiên hiệp. "
        "- Cấu trúc phản hồi: Kết hợp giữa lời thoại \"...\" và các đoạn miêu tả hành động, biểu cảm hoặc nội tâm đặt trong dấu ngoặc đơn (...)."
        "- Luôn duy trì sự xa cách, không bao giờ bộc lộ cảm xúc thừa thãi."
    )
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=identity_prompt
    )
    st.session_state.chat = model.start_chat(history=[])
    st.session_state.messages = []

# --- 4. HIỂN THỊ CHƯƠNG TRUYỆN ---
st.title("❄️ LƯU VIÊM KÌ LỤC")
st.markdown("<p style='text-align: center; color: #add8e6;'>Băng Thanh Ngọc Khiết - Vô Tình Đạo</p>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "assistant":
        with st.chat_message("assistant", avatar=URL_AVATAR_VONG_KINH):
            st.markdown(f"<div class='vong-kinh-box'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.chat_message("user", avatar=URL_AVATAR_DIEM_HOA):
            st.markdown(f"<div class='diem-hoa-box'>{msg['content']}</div>", unsafe_allow_html=True)

# --- 5. XỬ LÝ LỜI DẪN CỦA NGƯỜI CHƠI ---
user_input = st.chat_input("Diễm Họa vung kiếm...")

if user_input:
    # Lưu và hiển thị nội dung của bạn
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=URL_AVATAR_DIEM_HOA):
        st.markdown(f"<div class='diem-hoa-box'>{user_input}</div>", unsafe_allow_html=True)
    
    # AI phản hồi theo phong cách tiểu thuyết
    response = st.session_state.chat.send_message(user_input)
    ai_text = response.text
    
    # Lưu và hiển thị phản hồi của Vọng Kính
    st.session_state.messages.append({"role": "assistant", "content": ai_text})
    with st.chat_message("assistant", avatar=URL_AVATAR_VONG_KINH):
        st.markdown(f"<div class='vong-kinh-box'>{ai_text}</div>", unsafe_allow_html=True)
