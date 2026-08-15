import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime
import requests

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- CSS (Clean Dark Mode & Input Visibility Fix) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e10 !important; }
    h1, h2, h3, p, div, span, label, .stMarkdown { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #161621 !important; }
    .stChatMessage { background-color: #1e1e24 !important; border-radius: 10px; }
    .stButton > button { background-color: #2b2b36 !important; color: #ffffff !important; border: 1px solid #444; width: 100%; }
    .st-expander { background-color: #1e1e24 !important; border-radius: 8px; border: 1px solid #333 !important; }
    
    /* प्लस पॉपओवर स्टाइल */
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

# --- AI RESPONSE (With Groq/Ollama Switch & Notes + Diagrams) ---
def get_ai_response(prompt, task_type="general"):
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %d %B %Y")
    
    if task_type == "notes":
        system_instruction = (
            "You are an expert student and tutor making clean, high-yield, handwritten-style study notes "
            "based on NCERT textbooks. Format the notes like a human topper's notebook: "
            "Use clear headings, concise bullet points, important keywords in bold, and simple explanations. "
            "CRITICAL: Wherever a diagram, flow-chart, or scientific sketch would help explain the concept, "
            "insert contextually relevant diagram tags like  right where it belongs (e.g., [attachment_0](attachment))."
        )
    elif task_type == "math":
        system_instruction = "You are an expert Math tutor. Solve the mathematical problem step by step clearly."
    elif task_type == "science":
        system_instruction = "You are an expert Science tutor. Explain the scientific concept clearly in simple points with diagrams where necessary."
    elif task_type == "song":
        system_instruction = "You are a professional lyricist. Write full, beautiful, emotional song lyrics with Sthayi and Antara."
    elif task_type == "image":
        system_instruction = "You are a professional AI prompt engineer. Create a detailed, high-quality prompt for image generation."
    else:
        system_instruction = f"Today is {current_date}. You are a helpful AI assistant. Respond clearly in the user's language."

    full_prompt = f"{system_instruction}\n\nTask/Query: {prompt}"
    
    selected_model = st.session_state.get("ai_model", "Groq (Cloud - Fast)")
    
    try:
        if "Groq" in selected_model:
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}], 
                model="llama-3.3-70b-versatile"
            )
            return chat.choices[0].message.content
        else:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": full_prompt, "stream": False},
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get("response", "Ollama response error.")
            else:
                return "Error: Ollama server not running locally. Please make sure Ollama is active."
    except Exception as e: 
        return f"Error: {str(e)} (Note: Ollama requires local server running if selected)."

# --- TEXT TO SPEECH ---
def play_audio(text):
    tts = gTTS(text=text, lang='hi')
    fp = io.BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp

# --- SIDEBAR: MODEL SWITCHER & ALL SPECIAL FEATURES ---
with st.sidebar:
    st.markdown("### ⚙️ Model Switcher")
    st.session_state["ai_model"] = st.radio(
        "AI मॉडल चुनें:", 
        ["Groq (Cloud - Fast)", "Ollama (Local - Offline)"], 
        key="model_switch"
    )
    
    st.markdown("---")
    st.markdown("### ✨ Special Features")
    
    # 1. Math Solver
    with st.expander("🧮 Math Solver"):
        m_type = st.radio("इनपुट माध्यम:", ["📁 फाइल अपलोड", "📷 लाइव कैमरा"], key="math_m")
        if m_type == "📁 फाइल अपलोड": st.file_uploader("मैथ फाइल चुनें", type=["jpg", "png", "pdf"], key="math_file")
        else: st.camera_input("मैथ फोटो लें", key="math_cam")
        q = st.text_input("गणित का सवाल लिखें:", key="math_txt")
        if st.button("Solve Math", key="btn_math"):
            res = get_ai_response(q or "Solve this math problem step by step cleanly", task_type="math")
            st.session_state.messages.extend([{"role": "user", "content": q or "Solve Math"}, {"role": "assistant", "content": res}])
            st.rerun()

    # 2. Science Solver
    with st.expander("🧪 Science Solver"):
        s_type = st.radio("इनपुट माध्यम:", ["📁 फाइल अपलोड", "📷 लाइव कैमरा"], key="sci_m")
        if s_type == "📁 फाइल अपलोड": st.file_uploader("साइंस फाइल चुनें", type=["jpg", "png", "pdf"], key="sci_file")
        else: st.camera_input("साइंस फोटो लें", key="sci_cam")
        q = st.text_input("विज्ञान का प्रश्न लिखें:", key="sci_txt")
        if st.button("Solve Science", key="btn_sci"):
            res = get_ai_response(q or "Explain this science concept clearly in simple points", task_type="science")
            st.session_state.messages.extend([{"role": "user", "content": q or "Solve Science"}, {"role": "assistant", "content": res}])
            st.rerun()

    # 3. Create Notes (हैंडरिटन + डायग्राम्स के साथ)
    with st.expander("📝 Create Notes"):
        n_type = st.radio("इनपुट माध्यम:", ["📁 फाइल अपलोड", "📷 लाइव कैमरा"], key="note_m")
        if n_type == "📁 फाइल अपलोड": st.file_uploader("डॉक्यूमेंट चुनें", type=["jpg", "pdf", "txt"], key="note_file")
        else: st.camera_input("फोटो लें", key="note_cam")
        q = st.text_input("नोट्स का टॉपिक लिखें:", key="note_txt")
        if st.button("Generate Notes", key="btn_note"):
            res = get_ai_response(q or "Study Notes", task_type="notes")
            st.session_state.messages.extend([{"role": "user", "content": f"Create Notes for: {q}"}, {"role": "assistant", "content": res}])
            st.rerun()

    # 4. General Solver
    with st.expander("🌍 General Solver"):
        q = st.text_input("कुछ भी पूछें:", key="gen_txt")
        if st.button("Get Answer", key="btn_gen"):
            res = get_ai_response(q, task_type="general")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 5. Image Generator
    with st.expander("🎨 Image Generator"):
        q = st.text_input("इमेज का आइडिया दें:", key="img_txt")
        if st.button("Generate Prompt", key="btn_img"):
            res = get_ai_response(q, task_type="image")
            st.session_state.messages.extend([{"role": "user", "content": q}, {"role": "assistant", "content": res}])
            st.rerun()

    # 6. AI Song Writer
    with st.expander("🎵 AI Song Writer"):
        q = st.text_input("गाने का मूड या विषय:", key="song_txt")
        if st.button("Write Full Song", key="btn_song"):
            res = get_ai_response(q, task_type="song")
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

# --- PLUS ICON (Popover) ---
with st.popover("➕"):
    st.markdown("### 📂 फाइल या कैमरा चुनें")
    upload_type = st.radio("विकल्प चुनें:", ["🖼️ गैलरी से फोटो", "📄 डॉक्यूमेंट फाइल", "📷 लाइव कैमरा"])
    if upload_type == "🖼️ गैलरी से फोटो":
        st.file_uploader("तस्वीर अपलोड करें", type=["jpg", "png", "jpeg"], key="pop_gal")
    elif upload_type == "📄 डॉक्यूमेंट फाइल":
        st.file_uploader("डॉक्यूमेंट अपलोड करें", type=["pdf", "txt", "docx"], key="pop_doc")
    else:
        st.camera_input("तस्वीर खींचें", key="pop_cam")

# --- CHAT INPUT (Fixed and Clean) ---
if prompt := st.chat_input("कुछ पूछो..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt, task_type="general")
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
