import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- FIXED CSS FOR DARK MODE ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e10 !important; }
    h1, h2, h3, p, div, span, label, .stMarkdown { color: #ffffff !important; }
    .stChatMessage { background-color: #1e1e24 !important; border-radius: 10px; }
    .stButton > button { background-color: #2b2b36 !important; color: #ffffff !important; border: 1px solid #444; }
    .st-expander { background-color: #161621 !important; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 OmniLearn Assistant")

if "messages" not in st.session_state: st.session_state.messages = []

# --- AI RESPONSE ---
def get_ai_response(prompt):
    current_date = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    full_prompt = (f"Current Date: {current_date}. Respond in the user's language: {prompt}")
    try:
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": full_prompt}], 
            model="llama-3.3-70b-versatile"
        )
        return chat.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- TEXT TO SPEECH ---
def text_to_speech(text):
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
        if st.radio("इनपुट:", ["फाइल", "कैमरा"], key="m_m") == "फाइल": st.file_uploader("Upload", key="m_up")
        else: st.camera_input("कैमरा", key="m_cam")
        q = st.text_input("सवाल:", key="m_q")
        if st.button("Solve Math"):
            res = get_ai_response(q or "Solve math")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 2. Science Solver
    with st.expander("🧪 Science Solver"):
        if st.radio("इनपुट:", ["फाइल", "कैमरा"], key="s_m") == "फाइल": st.file_uploader("Upload", key="s_up")
        else: st.camera_input("कैमरा", key="s_cam")
        q = st.text_input("प्रश्न:", key="s_q")
        if st.button("Solve Science"):
            res = get_ai_response(q or "Explain science")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 3. Create Notes
    with st.expander("📝 Create Notes"):
        if st.radio("इनपुट:", ["फाइल", "कैमरा"], key="n_m") == "फाइल": st.file_uploader("Upload", key="n_up")
        else: st.camera_input("कैमरा", key="n_cam")
        q = st.text_input("टॉपिक:", key="n_q")
        if st.button("Generate Notes"):
            res = get_ai_response(f"Write natural, human-like handwritten style notes for: {q}")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 4. Song Writer
    with st.expander("🎵 AI Song Writer"):
        q = st.text_input("मूड/विषय:", key="so_q")
        if st.button("Write Song"):
            res = get_ai_response(f"Write a full, rhythmic song lyrics with Sthayi and Antara for: {q}")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    if st.button("🗑️ Clear All"): st.session_state.messages = []; st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 सुनो", key=f"audio_{idx}"):
                st.audio(text_to_speech(msg["content"]), format='audio/mp3')

# --- PLUS ICON ---
with st.popover("➕"):
    m = st.radio("माध्यम:", ["🖼️ गैलरी", "📄 डॉक्यूमेंट", "📷 कैमरा"])
    if m == "🖼️ गैलरी": st.file_uploader("फोटो", type=["jpg", "png"], key="p1")
    elif m == "📄 डॉक्यूमेंट": st.file_uploader("दस्तावेज़", type=["pdf", "txt"], key="p2")
    else: st.camera_input("कैमरा", key="p3")

if prompt := st.chat_input("कुछ पूछो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
