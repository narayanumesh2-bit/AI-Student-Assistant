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

# --- AI RESPONSE (Multilingual, Date & Time Support) ---
def get_ai_response(prompt):
    current_date = datetime.datetime.now().strftime("%d %B %Y, %I:%M %p")
    full_prompt = (
        f"Current Date and Time: {current_date}. "
        f"You are an expert, friendly AI assistant. Always respond in the exact same language "
        f"that the user uses (supports Hindi, English, and all Indian languages). "
        f"Task/Query: {prompt}"
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

# --- SIDEBAR SPECIAL FEATURES (With Upload & Camera Options) ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    
    # 1. Math Solver
    with st.expander("🧮 Math Solver"):
        math_mode = st.radio("मैथ इनपुट चुनें:", ["फाइल/फोटो अपलोड", "लाइव कैमरा"], key="math_m")
        if math_mode == "फाइल/फोटो अपलोड":
            math_file = st.file_uploader("Math File/Doc", type=["jpg", "png", "pdf", "txt", "docx"], key="math_up")
        else:
            math_cam = st.camera_input("मैथ प्रश्न की फोटो लें", key="math_cam")
            
        math_query = st.text_input("या गणित का सवाल यहाँ लिखें:", key="math_q")
        if st.button("Solve Math"):
            q_text = math_query if math_query else "Solve the math problem step by step."
            res = get_ai_response(q_text)
            st.session_state.messages.append({"role": "user", "content": f"Math: {q_text}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
            
    # 2. Science Solver
    with st.expander("🧪 Science Solver"):
        sci_mode = st.radio("साइंस इनपुट चुनें:", ["फाइल/फोटो अपलोड", "लाइव कैमरा"], key="sci_m")
        if sci_mode == "फाइल/फोटो अपलोड":
            sci_file = st.file_uploader("Science File/Doc", type=["jpg", "png", "pdf", "txt", "docx"], key="sci_up")
        else:
            sci_cam = st.camera_input("साइंस प्रश्न की फोटो लें", key="sci_cam")
            
        sci_query = st.text_input("या विज्ञान का प्रश्न यहाँ लिखें:", key="sci_q")
        if st.button("Solve Science"):
            q_text = sci_query if sci_query else "Explain this science concept clearly."
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

    # 4. Create Notes (Human-Like Handwritten Style with Upload & Camera)
    with st.expander("📝 Create Notes"):
        note_mode = st.radio("नोट्स इनपुट चुनें:", ["फाइल/फोटो अपलोड", "लाइव कैमरा"], key="note_m")
        if note_mode == "फाइल/फोटो अपलोड":
            note_file = st.file_uploader("Notes File/Doc", type=["jpg", "png", "pdf", "txt", "docx"], key="note_up")
        else:
            note_cam = st.camera_input("नोट्स के लिए फोटो लें", key="note_cam")
            
        note_topic = st.text_input("नोट्स का टॉपिक लिखें:", key="note_t")
        if st.button("Generate Notes"):
            topic_desc = note_topic if note_topic else "the provided document"
            q_text = (
                f"Act as an expert human student. Write clean, natural, handwritten-style study notes for '{topic_desc}'. "
                f"Make it look like it was written manually by a person in a notebook—use simple headings, bullet points, "
                f"and easy explanations. Avoid any robotic AI jargon."
            )
            res = get_ai_response(q_text)
            st.session_state.messages.append({"role": "user", "content": f"Handwritten Notes for: {topic_desc}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 5. Image Generator Prompt
    with st.expander("🎨 Image Generator"):
        img_prompt = st.text_input("तस्वीर/आइडिया का वर्णन करें:", key="img_q")
        if st.button("Generate Image Concept"):
            res = get_ai_response(f"Create a professional, detailed AI image generation prompt and description based on: {img_prompt}")
            st.session_state.messages.append({"role": "user", "content": f"Image Concept: {img_prompt}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 6. AI Song Writer (Full Lyrics Generator)
    with st.expander("🎵 AI Song Writer"):
        song_prompt = st.text_input("गाने का विषय, मूड या बोल का आइडिया लिखें:", key="song_q")
        if st.button("Write Full Song"):
            q_text = (
                f"Write complete, full song lyrics (with Sthayi/Mukhdah and Antara) based on this topic/mood: '{song_prompt}'. "
                f"Make it emotional, rhythmic, and ready to sing in the user's language."
            )
            res = get_ai_response(q_text)
            st.session_state.messages.append({"role": "user", "content": f"Song Request: {song_prompt}"})
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

# --- PLUS ICON (SEPARATE OPTIONS FOR GALLERY, DOCUMENTS & CAMERA) ---
with st.popover("➕"):
    st.markdown("### 📂 अपलोड या कैमरा चुनें")
    main_choice = st.radio("माध्यम चुनें:", ["🖼️ गैलरी (तस्वीरें)", "📄 डॉक्यूमेंट फाइल्स (PDF, TXT, DOCX)", "📷 लाइव कैमरा (फोटो खींचें)"])
    
    if main_choice == "🖼️ गैलरी (तस्वीरें)":
        gal_file = st.file_uploader("तस्वीर चुनें", type=["jpg", "png", "jpeg"], key="pop_gal")
        if gal_file:
            st.success(f"'{gal_file.name}' गैलरी से अपलोड हो गई!")
    elif main_choice == "📄 डॉक्यूमेंट फाइल्स (PDF, TXT, DOCX)":
        doc_file = st.file_uploader("डॉक्यूमेंट फाइल चुनें", type=["pdf", "txt", "docx", "csv"], key="pop_doc")
        if doc_file:
            st.success(f"'{doc_file.name}' डॉक्यूमेंट अपलोड हो गया!")
    else:
        cam_pic = st.camera_input("कैमरे से फोटो लें", key="pop_cam")
        if cam_pic:
            st.success("कैमरे से फोटो सफलतापर्वक ले ली गई है!")

# --- CHAT INPUT ---
prompt = st.chat_input("कुछ पूछो (हिंदी, इंग्लिश या किसी भी भाषा में)...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
