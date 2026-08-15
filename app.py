import streamlit as st
from groq import Groq
from gtts import gTTS
import io
import datetime
import requests

# --- CONFIGURATION ---
client = Groq(api_key="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")

st.set_page_config(page_title="OmniLearn Assistant", page_icon="🤖", layout="wide")

# --- CSS (Dark Mode & Chat Input Text Visibility Fix) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e0e10 !important; }
    h1, h2, h3, p, div, span, label, .stMarkdown { color: #ffffff !important; }
    [data-testid="stSidebar"] { background-color: #161621 !important; }
    .stChatMessage { background-color: #1e1e24 !important; border-radius: 10px; }
    .stButton > button { background-color: #2b2b36 !important; color: #ffffff !important; border: 1px solid #444; width: 100%; }
    .st-expander { background-color: #1e1e24 !important; border: 1px solid #333 !important; }
    
    /* चैट इनपुट बॉक्स टेक्स्ट विजिबिलिटी फिक्स */
    [data-testid="stChatInput"] textarea {
        background-color: #1e1e24 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }
    
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

# --- AI RESPONSE (With Groq/Ollama Switch, Diagram Tags & Handwritten Notes Support) ---
def get_ai_response(prompt, task_type="general"):
    now = datetime.datetime.now()
    current_date = now.strftime("%A, %d %B %Y")
    
    if task_type == "notes":
        system_instruction = (
            "You are an expert student and tutor making clean, high-yield, handwritten-style study notes "
            "based on NCERT textbooks. Format the notes like a human topper's notebook: "
            "Use clear headings, concise bullet points, important keywords in bold, and simple explanations. "
            "CRITICAL: Wherever a diagram, flow-chart, or anatomical/scientific sketch would help explain the concept, "
            "insert contextually relevant diagram tags like [attachment_0](attachment) right where it belongs (e.g., [attachment_1](attachment), "
            "[attachment_2](attachment)). Avoid any weird code formatting."
        )
    elif task_type == "math":
        system_instruction = "You are an expert Math tutor. Solve the mathematical problem step by step clearly and explain each formula."
    elif task_type == "science":
        system_instruction = "You are an expert Science tutor. Explain the scientific concept clearly in simple points, including relevant scientific diagrams or tags where helpful."
    elif task_type == "song":
        system_instruction = "You are a professional lyricist. Write full, beautiful, emotional song lyrics with Sthayi and Antara based on the user's mood."
    elif task_type == "image":
        system_instruction = "You are a professional AI prompt engineer. Create a detailed, high-quality prompt and concept description for image generation."
    else:
        system_instruction = f"Today is {current_date}. You are a helpful AI assistant. Respond clearly in the user's language."

    full_prompt = f"{system_instruction}\n\nTask/Query: {prompt}"
    
    # मॉडल स्विच चेक (Groq या Ollama)
    selected_model = st.session_state.get("ai_model", "Groq (Cloud - Fast)")
    
    try:
        if "Groq" in selected_model:
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": full_prompt}], 
                model="llama-3.3-70b-versatile"
            )
            return chat.choices[0].message.content
        else:
            # लोकल Ollama मॉडल के लिए
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "llama3", "prompt": full_prompt, "stream": False},
                timeout=10
            )
            if response.status_code == 200:
                return response.json().get("response", "Ollama response error.")
            else:
                return "Error: Ollama server not running locally. Please make sure Ollama is active on your device."
    except Exception as e: 
        return f"Error: {str(e)} (Note: Ollama requires local server running if selected)."

# --- TEXT TO SPEECH ---
def
