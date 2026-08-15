import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- CSS (Dark Mode & Bright Text) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e10 !important; }
    h1, h2, h3, p, div, span, label, .stMarkdown { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #1e1e24 !important; }
    .stChatMessage { background-color: #1e1e24 !important; border-radius: 10px; }
    .stButton > button { background-color: #2b2b36 !important; color: #ffffff !important; border: 1px solid #444; }
    .st-expander { background-color: #161621 !important; border: 1px solid #333 !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 OmniLearn Assistant")

if "messages" not in st.session_state: st.session_state.messages = []

# --- AI RESPONSE (Multilingual & Date) ---
def get_ai_response(prompt):
    dt = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    full_prompt = f"Date: {dt}. User language: {prompt}. Respond in the user's language."
    try:
        chat = client.chat.completions.create(messages=[{"role": "user", "content": full_prompt}], model="llama-3.3-70b-versatile")
        return chat.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

# --- TEXT TO SPEECH (गाना गाकर सुनाने के लिए) ---
def play_audio(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- SIDEBAR SPECIAL FEATURES ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    
    # 1. Solvers & Notes
    for f in ["🧮 Math Solver", "🧪 Science Solver", "🌍 General Solver", "📝 Create Notes", "🎨 Image Generator"]:
        with st.expander(f):
            st.write(f"Inp: {f}")
            if st.button(f"ओपन {f}", key=f"btn_{f}"):
                res = get_ai_response(f"Do task for {f}")
                st.session_state.messages.append({"role": "assistant", "content": res})
                st.rerun()

    # 2. Song Writer (गाना लिखकर गाएगा)
    with st.expander("🎵 AI Song Writer"):
        mood = st.text_input("गाने का विषय लिखें:", key="song_in")
        if st.button("गाना तैयार करो"):
            lyrics = get_ai_response(f"Write a full emotional song with Sthayi and Antara for: {mood}")
            st.session_state.messages.append({"role": "assistant", "content": lyrics})
            st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 गाओ", key=f"audio_{idx}"):
                st.audio(play_audio(msg["content"]), format='audio/mp3')

# --- PLUS ICON ---
with st.popover("➕"):
    mode = st.radio("माध्यम:", ["🖼️ गैलरी", "📄 डॉक्यूमेंट", "📷 कैमरा"])
    if mode == "📷 कैमरा": st.camera_input("कैमरा")
    else: st.file_uploader("फाइल", type=["jpg", "pdf"])

if prompt := st.chat_input("कुछ पूछो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
    
