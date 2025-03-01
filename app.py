import cv2
import openai
import speech_recognition as sr
import pytesseract
import pyttsx3
import fitz
import requests
import streamlit as st
import time
import keyboard
import os
from PIL import Image
from dotenv import load_dotenv



load_dotenv()

# STREAMLIT CODE
st.set_page_config(page_title="Voice Command App", page_icon="🎤", layout="centered")

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        /* Main background color */
        .stApp {
            background-color: #000000;
        }
        /* Main container styling */
        .main {
            background-color: #000;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            margin-top: 2rem;
            color: #ffffff;
            text-align: center;
        }
        /* Header and subheader styling */
        .stHeader, .stSubheader {
            color: #ffffff;
            text-align: center;
        }
        /* Tabs styling */
        .stTabs [role="tablist"] button {
            margin-top: 1rem;
            font-size: 1.2rem;
            padding: .35rem;
            border-radius: 5px;
            background-color: black;
            color: #ffffff;
            border: 1px solid #555555;
            transition: all 1s ease;
        }
        .stTabs [role="tablist"] button:hover {
            color: green;
            border: 1px solid green;
        }
        .stTabs [role="tablist"] button[data-baseweb="tab-highlighted"] {
            background-color: #4CAF50;
            color: white;
            border-bottom-color: white; /* Change underline color */
        }
        /* Text styling */
        .stText {
            font-size: 1.1rem;
            padding: 1rem;
            background-color: black;
            border: 1px solid #555555;
            border-radius: 5px;
            color: #ffffff;
            margin-top: 1rem;
            text-align: center;
        }
        /* Divider styling */
        .stDivider {
            border-top: 1px solid #4CAF50;
            margin: 2rem 0;
        }
        /* Tooltip styling */
        .tooltip {
            position: relative;
            display: inline-block;
            border-bottom: 1px dotted white;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 200px;
            background-color: #4CAF50;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%; /* Position the tooltip above the text */
            left: 50%;
            margin-left: -100px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        /* Icon styling */
        .icon {
            margin-right: 10px;
        }
        /* Centered GIF styling */
        .centered-gif {
            display: flex;
            justify-content: center;
            align-items: center;

        }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align: center;'>| Nayan |</h1>", unsafe_allow_html=True)
st.divider()

st.markdown('<div class="centered-gif"><img src="https://media1.tenor.com/m/BOu8ryjIR38AAAAd/sound-wave-wave.gif" alt="Soundwave Animation" height=200 width=800></div>', unsafe_allow_html=True)



tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Start audio", "Translate", "Summarise Notes", "Contextual Question", "Upload", "Playback Speed", "Quiz"
])


with tab1:
    st.markdown("""
        <div class="stText">
            <div>🎧 To start playing the audio say <strong>'START'</strong></div>
        </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
        <div class="stText">
            <div>🌐 To translate the audio say <strong>'TRANSLATE'</strong></div>
        </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown("""
        <div class="stText">
            <div>📝 To summarise your notes say <strong>'SUMMARISE'</strong></div>
        </div>
    """, unsafe_allow_html=True)

with tab4:
    st.markdown("""
        <div class="stText">
            <div>❓ To ask a question about the content of your notes say <strong>'QUESTION'</strong></div>
        </div>
    """, unsafe_allow_html=True)

with tab5:
    st.markdown("""
        <div class="stText">
            <div>📤 To upload notes say <strong>'UPLOAD'</strong></div>
        </div>
    """, unsafe_allow_html=True)

with tab6:
    st.markdown("""
        <div class="stText">
            <div>⏩ Say <strong>'FAST'</strong> for faster speeds,  <strong>'MEDIUM'</strong> for normal speeds, and  <strong>'SLOW'</strong> for slower speeds.</div>
        </div>
    """, unsafe_allow_html=True)

with tab7:
    st.markdown("""
        <div class="stText">
            <div>⏩ Say <strong>'QUIZ'</strong> to be quizzed about the contents of the file.</div>
        </div>
    """, unsafe_allow_html=True)


# api keys
openai.api_key = os.getenv("OPENAI_API_KEY")
deepl_api_key = os.getenv("DEEPL_API_KEY")

# for voice recognition
r = sr.Recognizer()

# speed settings
speeds = {
    "slow" : 125,
    "medium" : 200,
    "fast" : 275
}

messages = [
    {"role": "system", "content": "You are a kind helpful assistant."},
]

def speech_recog():
    try:
        with sr.Microphone() as source:
            print("Listening")
            audio_text = r.listen(source, timeout = 5, phrase_time_limit = 5)
            print("Done")
            
            try:
                text = r.recognize_google(audio_text).lower()
                print(text)
                return text
            except sr.UnknownValueError:
                speak("Sorry, I did not understand that")
            except sr.RequestError as e:
                print("Could not request results; {0}".format(e))
    except Exception as e:
        print(f"An error occurred: {e}")
        
client = openai.OpenAI(api_key="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")  # OpenAI client initialize karein

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")




def ask_gemini(message):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"  # Add the key directly to the URL

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [{
            "parts": [{"text": message}]
        }]
    }

    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Will raise an error for bad status codes
        
        # Debug: Print the raw response to check its structure
        response_json = response.json()
        print("API Response:", response_json)

        # Extract the main content text from the response
        if "candidates" in response_json and len(response_json["candidates"]) > 0:
            content = response_json["candidates"][0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return content.strip()  # Return the main text without extra spaces

        return "No content found in the response."

    except requests.exceptions.RequestException as e:
        print(f"❌ Error: {e}")
        return "An error occurred while processing your request."

    
MAX_RETRIES = 3  # Maximum retries allowed

def ask_gpt(message, retries=0, max_retries=3):
    if retries >= max_retries:
        print("❌ Maximum retry limit reached! Stopping execution.")
        return "Rate limit exceeded, please try again later."

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content
    except openai.RateLimitError:
        print(f"⚠️ Rate Limit exceeded! Retrying in 5 seconds... ({retries+1}/{max_retries})")
        time.sleep(5)
        return ask_gemini(message, retries + 1)
    except Exception as e:
        print(f"❌ OpenAI API Error: {e}")
        return "An error occurred while processing your request."


# language codes for deepl api with their codes
languages = {
    "bulgarian": "BG",
    "czech": "CS",
    "danish": "DA",
    "german": "DE",
    "greek": "EL",
    "english": "EN-GB",
    "spanish": "ES",
    "estonian": "ET",
    "finnish": "FI",
    "french": "FR",
    "hungarian": "HU",
    "indonesian": "ID",
    "italian": "IT",
    "japanese": "JA",
    "korean": "KO",
    "lithuanian": "LT",
    "latvian": "LV",
    "norwegian": "NB",
    "dutch": "NL",
    "polish": "PL",
    "portuguese": "PT-BR",
    "romanian": "RO",
    "russian": "RU",
    "slovak": "SK",
    "slovenian": "SL",
    "swedish": "SV",
    "turkish": "TR",
    "ukrainian": "UK",
    "chinese": "ZH"
}

#function to get data from pdf
def extract_text_from_pdf(pdf_path):
    
    pdf_document = fitz.open(pdf_path)
    
    all_text = ""
    
    for page_num in range(len(pdf_document)):
        
        page = pdf_document.load_page(page_num)
        
        text = page.get_text()
        
        all_text += text

    pdf_document.close()
    
    return all_text

#function for generating speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

#functions for image processing
def resize(img):
    return cv2.resize(img, (0,0), fx = 10, fy = 10)

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image,5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def ocr(img):
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    img = resize(img)
    img = get_grayscale(img)
    img = thresholding(img)
    img = remove_noise(img)
    text = str(pytesseract.image_to_string(img))
    return text

# deepl api access
def translate_text(text):
    speak("What language do you want?")
    target_language = speech_recog()  # Capture the language from speech

    if target_language is None:
        return None

    # Construct the prompt for translation
    message = f"Translate the following text to {target_language}: {text}"

    translated_text = ask_gemini(message)  # Use Gemini to get the translation
    speak(translated_text)  # Speak the translated text
    return translated_text

def summarise_text(text):
    message = f"Summarise the following text into a few words: {text}"
    summary = ask_gemini(message)  # Get summary from Gemini
    speak(summary)  # Speak out the summarized text
    
def question_and_answer():
    speak("What is your question?")
    question = speech_recog()
    speak(ask_gemini(question))

def quiz(text):
    message = f"Generate me a question from the following text: {text}. The question you generate can be many words but the answer to the generated question should be only a single word. Don't tell me the answer though."
    question = ask_gemini(message)
    speak(question)
    answer = speech_recog()
    message = f"You asked me the question: {question}. Is the answer: {answer} ?"
    reply = ask_gemini(message)
    speak(reply)

# setting up engine for speaking
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# intro message for when the website loads
intro_message = "Remember to tap spacebar before you say any voice commands. To upload a file say UPLOAD, to start say START, to translate to a different language say TRANSLATE, to summarize say SUMMARISE, to ask questions say QUESTION, to quiz yourself say QUIZ, to change the playback speed say FAST, MEDIUM, or SLOW. "
speak(intro_message)

# paths for the notes
PATH = r"C:\Projects\nayan_project\static"
files = os.listdir(PATH)

text = None
while True:
    user = None
    if keyboard.is_pressed('space'):
        user = speech_recog()
        time.sleep(0.2)
    if user is not None:
            if user == "upload":
                speak("What is the name of the note you want to upload?")
                user_file = speech_recog()
                found = False
                if user_file is not None:
                    for file_name in files:
                        if user_file in file_name:
                            user_file = os.path.join(PATH, file_name)
                            found = True
                            break
                    if found:
                        if ".pdf" in user_file:
                            text = extract_text_from_pdf(user_file)
                        else:
                            img = cv2.imread(user_file)
                            text = pytesseract.image_to_string(img)
                    else:
                        speak("I could not find the file.")   
            elif user == "slow":
                engine.setProperty("rate", speeds["slow"])
            elif user == "medium":
                engine.setProperty("rate", speeds["medium"])
            elif user == "fast":
                engine.setProperty("rate", speeds["fast"])
            elif user == "question":
                question_and_answer()
            elif user == "quiz":
                quiz(text)
            elif user == "translate":
                if text is None:
                    print("Please upload a file first.")
                else:
                    translated = translate_text(text)
                    if translated is None:
                        pass
                    else:
                        text = translated
            elif user == "summarise":
                summarise_text(text)
            elif user == "start":
                if text is None:
                    speak("Please upload a file first.")
                else:
                    speak(text)
                    