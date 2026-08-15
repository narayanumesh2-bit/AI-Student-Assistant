import streamlit as st
from groq import Groq
import ollama
from PIL import Image
import pytesseract
import speech_recognition as sr
import io
from streamlit_mic_recorder import mic_recorder

# --- CONFIGURATION ---
client = Groq(api_key="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")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- UI SETUP ---
st.set_page_config(page_title="AI Student Smart Assistant", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #131314; }
    div[data-testid="stChatMessage"] p, div[data-testid="stChatMessage"] div { color: #FFFFFF !important; font-size: 16px !important; }
    section[data-testid="stSidebar"] { background-color: #f0f2f6 !important; }
    section[data-testid="stSidebar"] div, section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label { 
        color: #000000 !important; font-weight: 600 !important; 
    }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI Student Smart Assistant")

if "messages" not in st.session_state: st.session_state.messages = []
if "extracted_text" not in st.session_state: st.session_state.extracted_text = ""

# --- AI RESPONSE ---
def get_ai_response(prompt, use_ollama):
    lang_instruction = " (Answer in the same language as user input. Support all Indian languages.)"
    full_prompt = prompt + lang_instruction
    try:
        if not use_ollama:
            chat = client.chat.completions.create(messages=[{"role": "user", "content": full_prompt}], model="llama-3.3-70b-versatile")
            return chat.choices[0].message.content
        else:
            res = ollama.chat(model='llama3', messages=[{'role': 'user', 'content': full_prompt}])
            return res['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    use_ollama = st.toggle("Switch to Ollama (Local)", value=False)
    st.write(f"Engine: **{'💻 Ollama' if use_ollama else '🚀 Groq'}**")
    st.markdown("---")
    st.markdown("### ✨ Special Features")
    
    with st.expander("🎨 AI Image Prompt"):
        img_q = st.text_input("Describe image:")
        if st.button("Generate"): st.write(get_ai_response(f"Create prompt for: {img_q}", use_ollama))
            
    with st.expander("🧮 Math/Science Solver"):
        if st.button("Solve/Explain"):
            if st.session_state.extracted_text: st.markdown(get_ai_response(f"Explain:\n{st.session_state.extracted_text}", use_ollama))
            else: st.warning("Upload image first!")

    with st.expander("📚 Notes & MCQ"):
        if st.button("Create Notes"):
            if st.session_state.extracted_text: st.markdown(get_ai_response(f"Notes:\n{st.session_state.extracted_text}", use_ollama))
        if st.button("Generate MCQ"):
            if st.session_state.extracted_text: st.markdown(get_ai_response(f"5 MCQs for:\n{st.session_state.extracted_text}", use_ollama))
    
    with st.expander("🎵 AI Song Writer"):
        song_topic = st.text_input("Topic for song:")
        if st.button("Write Song"):
            st.markdown(get_ai_response(f"Write a song about: {song_topic}", use_ollama))

    if st.button("🗑️ Clear All"): st.session_state.messages = []; st.session_state.extracted_text = ""; st.rerun()

# --- MAIN CHAT & VOICE ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

c1, c2 = st.columns([1, 6])
with c1:
    audio_data = mic_recorder(start_prompt="🎤", stop_prompt="⏹️", key="mic")
    with st.popover("➕"):
        choice = st.radio("Source:", ["Gallery", "Camera"])
        if choice == "Gallery":
            file = st.file_uploader("Upload", type=["jpg", "png"])
            if file: st.session_state.extracted_text = pytesseract.image_to_string(Image.open(file))
        else:
            cam = st.camera_input("Take Photo")
            if cam: st.session_state.extracted_text = pytesseract.image_to_string(Image.open(cam))

with c2:
    prompt = st.chat_input("Ask me anything...")

# सुधरा हुआ माइक लॉजिक
final_input = prompt
if audio_data:
    try:
        r = sr.Recognizer()
        # बाइट्स से सीधे ऑडियो बनाना
        audio_file = io.BytesIO(audio_data['bytes'])
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
            # गूगल स्पीच रिकग्निशन
            final_input = r.recognize_google(audio, language="hi-IN")
    except Exception:
        st.error("माइक में समस्या: या तो बहुत शोर है या इंटरनेट धीमा है। फिर से प्रयास करें।")

if final_input:
    st.session_state.messages.append({"role": "user", "content": final_input})
    with st.chat_message("user"): st.markdown(final_input)
    with st.chat_message("assistant"):
        response = get_ai_response(f"{final_input}\n\nContext: {st.session_state.extracted_text}", use_ollama)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()