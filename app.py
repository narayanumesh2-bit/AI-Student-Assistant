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

# --- AI RESPONSE (With Current Date Support) ---
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

# --- SIDEBAR SPECIAL FEATURES ---
with st.sidebar:
    st.markdown("### ✨ Special Features")
    
    # 1. Math Solver
    with st.expander("🧮 Math Solver"):
        math_file = st.file_uploader("Upload Math File", type=["jpg", "png", "pdf", "txt"], key="math_up")
        math_query = st.text_input("Enter math question:", key="math_q")
        if st.button("Solve Math"):
            prompt = f"Solve this math problem: {math_query}"
            res = get_ai_response(prompt)
            st.session_state.messages.append({"role": "user", "content": f"Math Query: {math_query}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()
            
    # 2. Science Solver
    with st.expander("🧪 Science Solver"):
        sci_file = st.file_uploader("Upload Science File", type=["jpg", "png", "pdf", "txt"], key="sci_up")
        sci_query = st.text_input("Enter science question:", key="sci_q")
        if st.button("Solve Science"):
            prompt = f"Explain this science concept: {sci_query}"
            res = get_ai_response(prompt)
            st.session_state.messages.append({"role": "user", "content": f"Science Query: {sci_query}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 3. General Solver
    with st.expander("🌍 General Solver"):
        gen_query = st.text_input("Ask anything:", key="gen_q")
        if st.button("Get Answer"):
            res = get_ai_response(gen_query)
            st.session_state.messages.append({"role": "user", "content": gen_query})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 4. Create Notes
    with st.expander("📝 Create Notes"):
        note_file = st.file_uploader("Upload Document for Notes", type=["jpg", "png", "pdf", "txt"], key="note_up")
        note_topic = st.text_input("Enter topic for notes:", key="note_t")
        if st.button("Generate Notes"):
            prompt = f"Create structured summary notes for: {note_topic}"
            res = get_ai_response(prompt)
            st.session_state.messages.append({"role": "user", "content": f"Notes for: {note_topic}"})
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

    # 5. Image Generator
    with st.expander("🎨 Image Generator"):
        img_prompt = st.text_input("Describe the image you want:", key="img_q")
        if st.button("Generate Image Concept"):
            prompt = f"Provide a detailed visual prompt description for an image generator based on: {img_prompt}"
            res = get_ai_response(prompt)
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

# --- PLUS ICON (DOCUMENT & FILE UPLOADER POPOVER) ---
with st.popover("➕"):
    st.markdown("### फाइल अपलोड करें")
    uploaded_doc = st.file_uploader("डॉक्यूमेंट, पीडीएफ या फोटो चुनें", type=["jpg", "png", "pdf", "txt", "docx"])
    if uploaded_doc:
        st.success(f"'{uploaded_doc.name}' सफलतापूर्वक अपलोड हो गई!")

# --- CHAT INPUT ---
prompt = st.chat_input("कुछ पूछो...")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = get_ai_response(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
