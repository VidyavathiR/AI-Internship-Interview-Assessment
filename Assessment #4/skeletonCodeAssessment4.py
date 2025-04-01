import random
import time
import os
import pygame
import logging
from gtts import gTTS

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Sample patient database with language, preferred communication channel, and age
patients = [
    {"id": 1, "name": "Ravi Kumar", "language": "Tamil", "channel": "SMS", "age": 65},
    {"id": 2, "name": "Ananya Rao", "language": "Telugu", "channel": "WhatsApp", "age": 30},
    {"id": 3, "name": "Joseph Mathew", "language": "Malayalam", "channel": "IVR", "age": 70},
    {"id": 4, "name": "Rahul Sharma", "language": "Hindi", "channel": "SMS", "age": 40},
    {"id": 5, "name": "David Thomas", "language": "English", "channel": "WhatsApp", "age": 28},
]

# Language code mapping
language_codes = {
    "Tamil": "ta",
    "Telugu": "te",
    "Malayalam": "ml",
    "Hindi": "hi",
    "English": "en"
}

# Predefined multi-language messages
messages = {
    "A": {
        "Tamil": "உங்கள் நேரம் உறுதிசெய்யப்பட்டது. தயவுசெய்து வருக!",
        "Telugu": "మీ నియామకం నిర్ధారించబడింది. దయచేసి రండి!",
        "Malayalam": "നിങ്ങളുടെ അപോയിന്റ്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു. ദയവായി വരൂ!",
        "Hindi": "आपका अपॉइंटमेंट कन्फर्म हो गया है। कृपया आएं!",
        "English": "Your appointment is confirmed. Please visit!"
    },
    "B": {
        "Tamil": "நீங்கள் நாளை சந்திக்க தயாரா? உங்கள் சந்திப்பு உறுதிசெய்யப்பட்டுள்ளது!",
        "Telugu": "మీరు రేపు సిద్ధంగా ఉన్నారా? మీ అపాయింట్మెంట్ నిర్ధారించబడింది!",
        "Malayalam": "നിങ്ങൾ നാളെയായി തയ്യാറാണോ? നിങ്ങളുടെ അപോയிண்ட്മെന്റ് സ്ഥിരീകരിച്ചിരിക്കുന്നു!",
        "Hindi": "क्या आप कल के लिए तैयार हैं? आपका अपॉइंटमेंट कन्फर्म हो गया है!",
        "English": "Are you ready for tomorrow? Your appointment is confirmed!"
    }
}

# Function to format messages for elderly patients
def format_message_for_elderly(message):
    return f"🔊 {message.upper()} 🔊 (Larger font for WhatsApp)"

# Function to send messages with A/B testing
def send_ab_test_message(patient):
    """Randomly assigns a message variation to a patient for A/B testing"""
    language = patient["language"]
    version = random.choice(["A", "B"])
    message = messages[version].get(language, messages["A"]["English"])  # Default to English if missing
    
    # Adjust formatting for elderly patients
    if patient["age"] >= 60 and patient["channel"] != "IVR":
        message = format_message_for_elderly(message)
    
    channel = patient["channel"]
    
    if channel == "IVR":
        text_to_speech(message, language)
    else:
        logging.info(f"📩 Sending Version {version} via {channel} to {patient['name']} ({language}): {message}")
    
    return version

# Function to convert text to speech and play it
def text_to_speech(message, language):
    """Convert text to speech and play it"""
    filename = f"message_{language}.mp3"
    lang_code = language_codes.get(language, "en")
    
    tts = gTTS(text=message, lang=lang_code)
    tts.save(filename)
    
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)  # Prevent high CPU usage
    
    pygame.mixer.music.unload()
    os.remove(filename)

# Track A/B effectiveness
effectiveness_tracker = {"A": 0, "B": 0}

def measure_effectiveness():
    """Simulates confirmation tracking separately for A/B messages"""
    for patient in patients:
        version = send_ab_test_message(patient)
        confirmed = random.choice([0, 1])  # Simulated confirmation
        effectiveness_tracker[version] += confirmed
    
    total_confirmed = sum(effectiveness_tracker.values())
    confirmation_rate = (total_confirmed / len(patients)) * 100
    logging.info(f"✅ Overall Confirmation Rate: {confirmation_rate:.2f}%")
    logging.info(f"📊 Version A Confirmations: {effectiveness_tracker['A']}, Version B Confirmations: {effectiveness_tracker['B']}")

measure_effectiveness()

# Patient satisfaction survey
def send_survey(patient):
    """Send a feedback survey to the patient after their appointment"""
    logging.info(f"📩 Sending satisfaction survey to {patient['name']} via {patient['channel']}.")
    logging.info(f"Survey Link: https://clinic-feedback.com/{patient['id']}")

# Simulate sending surveys
for patient in patients:
    send_survey(patient)
