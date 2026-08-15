import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime
import platform

# --- ENVIRONMENT CHECK ---
IS_WINDOWS = platform.system() == "Windows"

# --- CONFIGURATION ---
client = Groq(api_key="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")

# --- UI SETUP ---
st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="centered")
st.markdown("<style>.stApp { background-color: #0e0e10; color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🤖 OmniLearn Assistant")

if "messages" not in st.session_state: st.session_state.messages = []

# --- AI RESPONSE ---
def get_ai_response(prompt):
    current_date = datetime.date.today().strftime("%d %B %Y")
    full_prompt = f"Today is {current_date}. Respond in the same language as the user. {prompt}"
    try:
        chat = client.chat.completions.create(messages=[{"role": "user", "content": full_prompt}], model="llama-3.3-70b-versatile")
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

# --- SIDEBAR (SPECIAL FEATURES) ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    if st.button("📝 Create Notes"): 
        st.session_state.messages.append({"role": "assistant", "content": get_ai_response("Create summary notes.")})
    if st.button("🧮 Math Solver"): 
        st.session_state.messages.append({"role": "assistant", "content": get_ai_response("Explain this math problem.")})
    if st.button("🎵 AI Song Writer"): 
        st.session_state.messages.append({"role": "assistant", "content": get_ai_response("Write a creative song.")})
    if st.button("🗑️ Clear All"): 
        st.session_state.messages = []; st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 सुनो", key=f"audio_{idx}"):
                st.audio(text_to_speech(msg["content"]), format='audio/mp3')

# --- IMAGE / CAMERA UPLOAD ---
with st.popover("➕ फोटो/डॉक्यूमेंट"):
    choice = st.radio("माध्यम:", ["Gallery", "Camera"])
    file = st.file_uploader("Upload", type=["jpg", "png"]) if choice == "Gallery" else st.camera_input("Camera")
    if file:
        st.success("फोटो अपलोड हो गई!")

prompt = st.chat_input("कुछ पूछो...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
