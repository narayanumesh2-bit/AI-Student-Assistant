import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime
import music_gen # यह टूल गाना गाकर सुनाएगा

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- CSS - साफ़ और चमकदार लुक ---
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

# --- AI RESPONSE (Date/Time & Multilingual) ---
def get_ai_response(prompt):
    dt = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    full_prompt = f"Date: {dt}. User language: {prompt}. Respond in the same language."
    try:
        chat = client.chat.completions.create(messages=[{"role": "user", "content": full_prompt}], model="llama-3.3-70b-versatile")
        return chat.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

# --- SIDEBAR SPECIAL FEATURES ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    
    features = ["🧮 Math Solver", "🧪 Science Solver", "🌍 General Solver", "📝 Create Notes", "🎨 Image Generator", "🎵 AI Song Writer"]
    
    for f in features:
        with st.expander(f):
            if "Song" in f:
                mood = st.text_input("गाना बनाने के लिए मूड/विषय लिखें:", key=f"inp_{f}")
                if st.button("गाना बनाओ", key=f"btn_{f}"):
                    # गाना गाकर सुनाने वाला टूल
                    music_data = music_gen.generate_music()
                    st.audio(music_data)
            else:
                st.write(f"{f} के लिए इनपुट:")
                if st.button(f"ओपन {f}", key=f"btn_{f}"):
                    res = get_ai_response(f"Explain or solve for {f}")
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- PLUS ICON (3 Column options) ---
with st.popover("➕"):
    st.write("📂 माध्यम चुनें:")
    mode = st.radio("चुनें:", ["🖼️ गैलरी", "📄 डॉक्यूमेंट", "📷 कैमरा"])
    if mode == "📷 कैमरा": st.camera_input("तस्वीर खींचें")
    else: st.file_uploader("फाइल चुनें", type=["jpg", "png", "pdf", "docx"])

if prompt := st.chat_input("कुछ पूछो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
