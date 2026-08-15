import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime
import platform

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")
st.markdown("<style>.stApp { background-color: #0e0e10; color: #ffffff; }</style>", unsafe_allow_html=True)

st.title("🤖 OmniLearn Assistant")

if "messages" not in st.session_state: st.session_state.messages = []

# --- AI RESPONSE (Multilingual & Date Support) ---
def get_ai_response(prompt):
    current_date = datetime.date.today().strftime("%d %B %Y")
    full_prompt = (
        f"Today is {current_date}. "
        f"You are a helpful AI assistant. Always respond in the exact same language "
        f"that the user uses (supports Hindi, English, and all Indian languages). "
        f"User query: {prompt}"
    )
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
        st.markdown("📁 **गैलरी / डॉक्यूमेंट / पीडीएफ अपलोड करें:**")
        math_file = st.file_uploader("Math File", type=["jpg", "png", "pdf", "txt", "docx"], key="math_up")
        math_query = st.text_input("या गणित का सवाल यहाँ लिखें:", key="math_q")
        if st.button("Solve Math"):
            q_text = math_query if math_query else "Solve the math problem from the uploaded file."
            res = get_ai_response(q_text)
            st.session_state.messages.append({"role": "user", "content": f"Math: {q_text}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
            
    # 2. Science Solver
    with st.expander("🧪 Science Solver"):
        st.markdown("📁 **गैलरी / डॉक्यूमेंट / पीडीएफ अपलोड करें:**")
        sci_file = st.file_uploader("Science File", type=["jpg", "png", "pdf", "txt", "docx"], key="sci_up")
        sci_query = st.text_input("या विज्ञान का प्रश्न यहाँ लिखें:", key="sci_q")
        if st.button("Solve Science"):
            q_text = sci_query if sci_query else "Explain the science concept from the uploaded file."
            res = get_ai_response(q_text)
            st.session_state.messages.append({"role": "user", "content": f"Science: {q_text}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 3. General Solver
    with st.expander("🌍 General Solver"):
        gen_query = st.text_input("कोई भी सामान्य सवाल पूछें:", key="gen_q")
        if st.button("Get Answer"):
            res = get_ai_response(gen_query)
            st.session_state.messages.append({"role": "user", "content": gen_query})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 4. Create Notes
    with st.expander("📝 Create Notes"):
        st.markdown("📁 **डॉक्यूमेंट या नोट्स फाइल अपलोड करें:**")
        note_file = st.file_uploader("Notes File", type=["jpg", "png", "pdf", "txt", "docx"], key="note_up")
        note_topic = st.text_input("नोट्स का टॉपिक लिखें:", key="note_t")
        if st.button("Generate Notes"):
            q_text = f"Create structured summary notes for: {note_topic}" if note_topic else "Create summary notes from the uploaded file."
            res = get_ai_response(q_text)
            st.session_state.messages.append({"role": "user", "content": f"Notes Topic: {note_topic}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 5. Image Generator
    with st.expander("🎨 Image Generator"):
        img_prompt = st.text_input("तस्वीर का वर्णन करें (Image Description):", key="img_q")
        if st.button("Generate Image Concept"):
            res = get_ai_response(f"Provide a detailed visual prompt description for an image generator based on: {img_prompt}")
            st.session_state.messages.append({"role": "user", "content": f"Image Idea: {img_prompt}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    if st.button("🗑️ Clear All Chat"): 
        st.session_state.messages = []
        st.rerun()

# --- CHAT UI ---
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if st.button(f"🔊 सुनो", key=f"audio_{idx}"):
                st.audio(text_to_speech(msg["content"]), format='audio/mp3')

# --- PLUS ICON (GALLERY, FILES & CAMERA POPOVER) ---
with st.popover("➕"):
    st.markdown("### 📂 फाइल या कैमरा चुनें")
    upload_type = st.radio("माध्यम चुनें:", ["गैलरी और डॉक्यूमेंट फाइल्स", "लाइव कैमरा (तस्वीर खींचें)"])
    
    if upload_type == "गैलरी और डॉक्यूमेंट फाइल्स":
        main_upload = st.file_uploader("यहाँ से चुनें (JPG, PNG, PDF, TXT, DOCX)", type=["jpg", "png", "pdf", "txt", "docx"])
        if main_upload:
            st.success(f"'{main_upload.name}' सफलतापूर्वक अपलोड हो गई!")
    else:
        cam_photo = st.camera_input("कैमरे से फोटो लें")
        if cam_photo:
            st.success("कैमरे की फोटो ले ली गई है!")

# --- CHAT INPUT ---
prompt = st.chat_input("कुछ पूछो (हिंदी, इंग्लिश या किसी भी भाषा में)...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
