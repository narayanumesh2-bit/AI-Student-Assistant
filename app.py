import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime
import platform
import music_gen # म्यूजिक जनरेशन के लिए

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- CSS FOR DARK MODE & BRIGHT TEXT ---
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
    full_prompt = f"Current Date: {current_date}. Respond in user's language: {prompt}"
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

# --- SIDEBAR SPECIAL FEATURES ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    
    # Math Solver
    with st.expander("🧮 Math Solver"):
        math_mode = st.radio("इनपुट:", ["फाइल अपलोड", "कैमरा"], key="math_m")
        if math_mode == "फाइल अपलोड": st.file_uploader("Upload", type=["jpg", "png", "pdf"], key="math_up")
        else: st.camera_input("कैमरा", key="math_cam")
        math_query = st.text_input("सवाल:", key="math_q")
        if st.button("Solve Math"):
            res = get_ai_response(math_query or "Solve math")
            st.session_state.messages.extend([{"role": "user", "content": math_query}, {"role": "assistant", "content": res}])
            st.rerun()

    # Science Solver
    with st.expander("🧪 Science Solver"):
        sci_mode = st.radio("इनपुट:", ["फाइल अपलोड", "कैमरा"], key="sci_m")
        if sci_mode == "फाइल अपलोड": st.file_uploader("Upload", type=["jpg", "png", "pdf"], key="sci_up")
        else: st.camera_input("कैमरा", key="sci_cam")
        sci_query = st.text_input("प्रश्न:", key="sci_q")
        if st.button("Solve Science"):
            res = get_ai_response(sci_query or "Explain science")
            st.session_state.messages.extend([{"role": "user", "content": sci_query}, {"role": "assistant", "content": res}])
            st.rerun()

    # General Solver
    with st.expander("🌍 General Solver"):
        gen_query = st.text_input("सवाल:", key="gen_q")
        if st.button("Get Answer"):
            res = get_ai_response(gen_query)
            st.session_state.messages.extend([{"role": "user", "content": gen_query}, {"role": "assistant", "content": res}])
            st.rerun()

    # Create Notes
    with st.expander("📝 Create Notes"):
        note_mode = st.radio("इनपुट:", ["फाइल अपलोड", "कैमरा"], key="note_m")
        if note_mode == "फाइल अपलोड": st.file_uploader("Upload", type=["jpg", "png", "pdf"], key="note_up")
        else: st.camera_input("कैमरा", key="note_cam")
        note_topic = st.text_input("टॉपिक:", key="note_t")
        if st.button("Generate Notes"):
            res = get_ai_response(f"Write natural, handwritten-style notes for: {note_topic}")
            st.session_state.messages.extend([{"role": "user", "content": note_topic}, {"role": "assistant", "content": res}])
            st.rerun()

    # Image Generator
    with st.expander("🎨 Image Generator"):
        img_prompt = st.text_input("तस्वीर का वर्णन:", key="img_q")
        if st.button("Generate Concept"):
            res = get_ai_response(f"Provide image prompt for: {img_prompt}")
            st.session_state.messages.extend([{"role": "user", "content": img_prompt}, {"role": "assistant", "content": res}])
            st.rerun()

    # AI Song Writer (Singing Feature)
    with st.expander("🎵 AI Song Writer"):
        song_prompt = st.text_input("गाने का मूड या विषय:", key="song_q")
        if st.button("गाना गाओ (Generate Song)"):
            st.write("🎤 गाना तैयार हो रहा है...")
            # गाना जनरेट करने के लिए Lyria 3 मॉडल कॉल करें
            music_data = music_gen.generate_music()
            st.session_state.messages.append({"role": "assistant", "content": f"यहाँ है आपके मूड '{song_prompt}' पर आधारित गाना:"})
            # यदि जनरेट हुआ तो दिखाएं
            if music_data:
                st.audio(music_data)
            st.rerun()

    if st.button("🗑️ Clear All"): 
        st.session_state.messages = []
        st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and "content" in msg:
            if st.button(f"🔊 सुनो", key=f"audio_{idx}"):
                st.audio(text_to_speech(msg["content"]), format='audio/mp3')

# --- PLUS ICON (Multimodal) ---
with st.popover("➕"):
    mode = st.radio("माध्यम:", ["🖼️ गैलरी", "📄 डॉक्यूमेंट", "📷 कैमरा"])
    if mode == "🖼️ गैलरी": st.file_uploader("फोटो", type=["jpg", "png"], key="gal")
    elif mode == "📄 डॉक्यूमेंट": st.file_uploader("दस्तावेज़", type=["pdf", "txt", "docx"], key="doc")
    else: st.camera_input("कैमरा", key="main_cam")

if prompt := st.chat_input("कुछ पूछो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
