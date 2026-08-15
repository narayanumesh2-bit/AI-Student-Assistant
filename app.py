import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- CSS (UI & Popover Fixes) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e10 !important; }
    h1, h2, h3, p, div, span, label, .stMarkdown { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #161621 !important; }
    .stChatMessage { background-color: #1e1e24 !important; border-radius: 10px; }
    .stButton > button { background-color: #2b2b36 !important; color: #ffffff !important; border: 1px solid #444; width: 100%; }
    .st-expander { background-color: #1e1e24 !important; border: 1px solid #333 !important; }
    
    /* चैट इनपुट बॉक्स फिक्स */
    [data-testid="stChatInput"] input { background-color: #1e1e24 !important; color: #ffffff !important; }
    
    /* प्लस पॉपओवर को बड़ा और साफ़ करने के लिए */
    [data-testid="stPopoverBody"] {
        background-color: #161621 !important;
        border: 1px solid #444 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        width: 300px !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 OmniLearn Assistant")

if "messages" not in st.session_state: st.session_state.messages = []

# --- AI RESPONSE (Correct Date & Day) ---
def get_ai_response(prompt):
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %d %B %Y, %I:%M %p")
    full_prompt = f"Today is {current_date}. Respond in the user's language: {prompt}"
    try:
        chat = client.chat.completions.create(messages=[{"role": "user", "content": full_prompt}], model="llama-3.3-70b-versatile")
        return chat.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

# --- TEXT TO SPEECH ---
def play_audio(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- SIDEBAR SPECIAL FEATURES ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    
    # 1. Math Solver
    with st.expander("🧮 Math Solver"):
        m_type = st.radio("इनपुट माध्यम:", ["📁 फाइल अपलोड", "📷 लाइव कैमरा"], key="math_m")
        if m_type == "📁 फाइल अपलोड": st.file_uploader("मैथ फाइल चुनें", type=["jpg", "png", "pdf"], key="math_file")
        else: st.camera_input("मैथ फोटो लें", key="math_cam")
        q = st.text_input("गणित का सवाल लिखें:", key="math_txt")
        if st.button("Solve Math", key="btn_math"):
            res = get_ai_response(q or "Solve this math problem step by step")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 2. Science Solver
    with st.expander("🧪 Science Solver"):
        s_type = st.radio("इनपुट माध्यम:", ["📁 फाइल अपलोड", "📷 लाइव कैमरा"], key="sci_m")
        if s_type == "📁 फाइल अपलोड": st.file_uploader("साइंस फाइल चुनें", type=["jpg", "png", "pdf"], key="sci_file")
        else: st.camera_input("साइंस फोटो लें", key="sci_cam")
        q = st.text_input("विज्ञान का प्रश्न लिखें:", key="sci_txt")
        if st.button("Solve Science", key="btn_sci"):
            res = get_ai_response(q or "Explain this science concept clearly")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 3. Create Notes
    with st.expander("📝 Create Notes"):
        n_type = st.radio("इनपुट माध्यम:", ["📁 फाइल अपलोड", "📷 लाइव कैमरा"], key="note_m")
        if n_type == "📁 फाइल अपलोड": st.file_uploader("डॉक्यूमेंट चुनें", type=["jpg", "pdf", "txt"], key="note_file")
        else: st.camera_input("फोटो लें", key="note_cam")
        q = st.text_input("नोट्स का टॉपिक लिखें:", key="note_txt")
        if st.button("Generate Notes", key="btn_note"):
            res = get_ai_response(f"Write clean, natural, handwritten-style study notes for: {q}")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 4. General Solver
    with st.expander("🌍 General Solver"):
        q = st.text_input("कुछ भी पूछें:", key="gen_txt")
        if st.button("Get Answer", key="btn_gen"):
            res = get_ai_response(q)
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 5. Image Generator
    with st.expander("🎨 Image Generator"):
        q = st.text_input("इमेज का आइडिया दें:", key="img_txt")
        if st.button("Generate Prompt", key="btn_img"):
            res = get_ai_response(f"Create a professional AI image prompt for: {q}")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 6. AI Song Writer
    with st.expander("🎵 AI Song Writer"):
        q = st.text_input("गाने का मूड या विषय:", key="song_txt")
        if st.button("Write Full Song", key="btn_song"):
            res = get_ai_response(f"Write a full emotional song with Sthayi and Antara for: {q}")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    if st.button("🗑️ Clear All Chat", key="btn_clear"): 
        st.session_state.messages = []
        st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 सुनो", key=f"audio_{idx}"):
                st.audio(play_audio(msg["content"]), format='audio/mp3')

# --- IMPROVED PLUS ICON (Popover) ---
with st.popover("➕"):
    st.markdown("### 📂 फाइल या कैमरा चुनें")
    upload_type = st.radio("विकल्प चुनें:", ["🖼️ गैलरी से फोटो", "📄 डॉक्यूमेंट फाइल", "📷 लाइव कैमरा"])
    if upload_type == "🖼️ गैलरी से फोटो":
        st.file_uploader("तस्वीर अपलोड करें", type=["jpg", "png", "jpeg"], key="pop_gal")
    elif upload_type == "📄 डॉक्यूमेंट फाइल":
        st.file_uploader("डॉक्यूमेंट अपलोड करें", type=["pdf", "txt", "docx"], key="pop_doc")
    else:
        st.camera_input("तस्वीर खींचें", key="pop_cam")

# --- CHAT INPUT ---
if prompt := st.chat_input("कुछ पूछो (हिंदी, इंग्लिश या किसी भी भाषा में)..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
