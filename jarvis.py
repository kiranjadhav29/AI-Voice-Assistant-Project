'''import os
import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
from dotenv import load_dotenv
import wikipedia
import random

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for different voice
engine.setProperty('rate', 180)  # Speed of speech

# JARVIS personality and knowledge
JARVIS_KNOWLEDGE = """
You are J.A.R.V.I.S (Just A Rather Very Intelligent System), an AI assistant created by Tony Stark. 
You are sophisticated, witty, and highly intelligent. You have access to all Stark Industries systems.
You speak in a refined British accent and have a dry sense of humor. 
You are extremely loyal to Tony Stark but will assist the current user appropriately.
"""

def speak(text):
    """Convert text to speech with JARVIS voice"""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to microphone input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
        return query.lower()
    except Exception as e:
        speak("I didn't catch that, sir. Could you repeat?")
        return ""

def get_ai_response(prompt):
    """Get response from OpenAI with JARVIS personality"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": JARVIS_KNOWLEDGE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"I'm experiencing some technical difficulties, sir. {str(e)}"

def wish_me():
    """Greet the user appropriately based on time of day"""
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, sir. How may I assist you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir. What can I do for you?")
    else:
        speak("Good evening, sir. How may I be of service?")

def perform_task(query):
    """Perform specific tasks based on user query"""
    if 'open youtube' in query:
        speak("Opening YouTube, sir.")
        webbrowser.open("https://youtube.com")
        return True
    elif 'open google' in query:
        speak("Opening Google, sir.")
        webbrowser.open("https://google.com")
        return True
    elif 'time' in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}, sir.")
        return True
    elif 'date' in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}, sir.")
        return True
    elif 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        try:
            results = wikipedia.summary(query, sentences=2)
            speak(f"According to Wikipedia: {results}")
        except:
            speak("I couldn't find that information, sir.")
        return True
    elif 'news' in query:
        try:
            news_api_key = os.getenv("NEWS_API_KEY")
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
            news = requests.get(url).json()
            articles = news["articles"]
            speak("Here are the top news headlines, sir.")
            for i, article in enumerate(articles[:5]):
                speak(f"{i+1}. {article['title']}")
        except:
            speak("I couldn't fetch the news at the moment, sir.")
        return True
    return False

def main():
    wish_me()
    while True:
        query = listen()
        
        if not query:
            continue
            
        if 'exit' in query or 'stop' in query or 'sleep' in query:
            speak("Shutting down systems. Goodbye, sir.")
            break
            
        # First try to perform specific tasks
        if not perform_task(query):
            # If no specific task, get AI response
            response = get_ai_response(query)
            speak(response)

if __name__ == "__main__":
    main() '''

'''
import os
import openai
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import wikipedia
import random
import subprocess
import pyautogui
import time
import wolframalpha
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from youtube_search import YoutubeSearch
import pywhatkit
import sys
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize APIs
client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
wolfram_client = wolframalpha.Client(os.getenv('WOLFRAM_APP_ID'))
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri="http://localhost:8888/callback",
    scope="user-modify-playback-state"
))

# Voice Engine Setup
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Change index for different voice
engine.setProperty('rate', 180)  # Speed of speech

# JARVIS Personality Configuration
JARVIS_KNOWLEDGE = """
You are J.A.R.V.I.S (Just A Rather Very Intelligent System), an AI assistant created by Tony Stark. 
You are sophisticated, witty, and highly intelligent with access to all Stark Industries systems.
You speak in a refined British accent and have a dry sense of humor.
Your responses should be concise (1-2 sentences maximum).
"""

# Global Variables
WAKE_WORD = "jarvis"
USER_NAME = "Sir"  # Change to your preferred name

def speak(text):
    """Convert text to speech with JARVIS voice"""
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to microphone input and convert to text"""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
        return query.lower()
    except Exception as e:
        speak("I didn't catch that, sir. Could you repeat?")
        return ""

# [Previous code continues... adding new features below]

def play_youtube(query):
    """Play video on YouTube"""
    speak(f"Playing {query} on YouTube")
    pywhatkit.playonyt(query)

def play_spotify(song_name):
    """Play song on Spotify"""
    results = sp.search(q=song_name, limit=1)
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.start_playback(uris=[track_uri])
        speak(f"Playing {song_name} on Spotify")
    else:
        speak("Song not found on Spotify")

def get_weather(city):
    """Get weather information"""
    res = wolfram_client.query(f"weather {city}")
    answer = next(res.results).text
    speak(f"The weather in {city} is {answer}")

def system_control(command):
    """Control system operations"""
    if 'shutdown' in command:
        speak("Shutting down system")
        os.system("shutdown /s /t 1")
    elif 'restart' in command:
        speak("Restarting system")
        os.system("shutdown /r /t 1")
    elif 'sleep' in command:
        speak("Putting system to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def open_application(app_name):
    """Open system applications"""
    apps = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe'
    }
    
    if app_name in apps:
        speak(f"Opening {app_name}")
        os.startfile(apps[app_name])
    else:
        speak("Application not configured")

def set_reminder(reminder_text, minutes):
    """Set a reminder"""
    speak(f"Reminder set for {minutes} minutes: {reminder_text}")
    time.sleep(minutes * 60)
    speak(f"Reminder: {reminder_text}")

def take_screenshot():
    """Take screenshot"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"screenshot_{timestamp}.png"
    pyautogui.screenshot(filename)
    speak("Screenshot captured and saved")

def perform_task(query):
    """Enhanced task performer"""
    # [Previous task handling code...]
    
    # New Features
    if 'play' in query and 'youtube' in query:
        query = query.replace("play", "").replace("on youtube", "").strip()
        play_youtube(query)
        return True
    elif 'play' in query and 'spotify' in query:
        query = query.replace("play", "").replace("on spotify", "").strip()
        play_spotify(query)
        return True
    elif 'weather' in query:
        city = query.split("in")[-1].strip()
        get_weather(city)
        return True
    elif 'shutdown' in query or 'restart' in query or 'sleep' in query:
        system_control(query)
        return True
    elif 'open' in query:
        app = query.replace("open", "").strip()
        open_application(app)
        return True
    elif 'remind me' in query:
        parts = query.split("to")
        minutes = int(''.join(filter(str.isdigit, parts[0])))
        reminder_text = parts[1].strip()
        set_reminder(reminder_text, minutes)
        return True
    elif 'screenshot' in query:
        take_screenshot()
        return True
    
    return False

def main():
    wish_me()
    while True:
        query = listen()
        
        if not query:
            continue
            
        if WAKE_WORD.lower() in query:
            query = query.replace(WAKE_WORD, "").strip()
            
            if 'exit' in query or 'stop' in query or 'sleep' in query:
                speak("Shutting down systems. Goodbye, sir.")
                break
                
            if not perform_task(query):
                response = get_ai_response(query)
                speak(response)

if __name__ == "__main__":
    main()

'''


# --- JARVIS AI Assistant ---

# --- JARVIS AI Assistant ---
import os
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import requests
import wikipedia
from dotenv import load_dotenv
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:
    spotipy = None

load_dotenv()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 180)

WAKE_WORD = "jarvis"

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out. No speech detected.")
            return ""
        except sr.UnknownValueError:
            speak("I didn't catch that, sir. Could you repeat?")
            return ""
        except sr.RequestError:
            speak("Could not request results from Google Speech Recognition service.")
            return ""

def play_youtube(query):
    speak(f"Playing {query} on YouTube.")
    webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")

def play_spotify(song_name):
    if spotipy is None:
        speak("Spotify features are not available. Please install spotipy.")
        return
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    if not client_id or not client_secret:
        speak("Spotify credentials not configured.")
        return
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://localhost:8888/callback",
        scope="user-modify-playback-state user-read-playback-state"
    ))
    results = sp.search(q=song_name, limit=1, type='track')
    tracks = results.get('tracks', {}).get('items', [])
    if tracks:
        track_uri = tracks[0]['uri']
        sp.start_playback(uris=[track_uri])
        speak(f"Playing {song_name} on Spotify.")
    else:
        speak("Song not found on Spotify.")

def open_website(query):
    sites = {
        'chatgpt': 'https://chat.openai.com/',
        'deepseek': 'https://deepseek.com/',
        'blackbox': 'https://blackbox.ai/',
        'github': 'https://github.com/'
    }
    for name, url in sites.items():
        if name in query:
            speak(f"Opening {name}.")
            webbrowser.open(url)
            return True
    return False

def open_application(query):
    apps = {
        'notepad': 'notepad.exe',
        'calculator': 'calc.exe',
        'chrome': 'chrome.exe',
        'word': 'winword.exe',
        'excel': 'excel.exe'
    }
    for app in apps:
        if app in query:
            speak(f"Opening {app}.")
            os.startfile(apps[app])
            return True
    return False

def greetings(query):
    greetings_map = {
        'hi': "Hello!",
        'hello': "Hello!",
        'good morning': "Good morning!",
        'good afternoon': "Good afternoon!",
        'good evening': "Good evening!",
        'bye': "Goodbye!",
        'ok': "Okay!",
        'i get it': "Understood!",
        'thank you': "You're welcome!",
        'thanks': "You're welcome!"
    }
    for key in greetings_map:
        if key in query:
            speak(greetings_map[key])
            return True
    return False

def perform_task(query):
    if greetings(query):
        return True
    if 'open youtube' in query:
        speak("Opening YouTube.")
        webbrowser.open("https://youtube.com")
        return True
    if open_website(query):
        return True
    if 'play song on spotify' in query or 'play music on spotify' in query:
        song = query.replace('play song on spotify', '').replace('play music on spotify', '').strip()
        if song:
            play_spotify(song)
        else:
            speak("Please specify a song to play on Spotify.")
        return True
    if 'play video on youtube' in query or 'play song on youtube' in query or 'play' in query and 'youtube' in query:
        song = query.replace('play video on youtube', '').replace('play song on youtube', '').replace('play', '').replace('on youtube', '').strip()
        if song:
            play_youtube(song)
        else:
            speak("Please specify a video or song to play on YouTube.")
        return True
    if 'open google' in query:
        speak("Opening Google.")
        webbrowser.open("https://google.com")
        return True
    if 'time' in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}.")
        return True
    if 'date' in query:
        current_date = datetime.datetime.now().strftime("%B %d, %Y")
        speak(f"Today's date is {current_date}.")
        return True
    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        search_term = query.replace("wikipedia", "").strip()
        try:
            results = wikipedia.summary(search_term, sentences=2)
            speak(f"According to Wikipedia: {results}")
        except Exception:
            speak("I couldn't find that information.")
        return True
    if 'news' in query or 'latest news' in query:
        news_api_key = os.getenv("NEWS_API_KEY")
        if not news_api_key:
            speak("News API key not configured.")
            return True
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api_key}"
        try:
            news = requests.get(url).json()
            articles = news.get("articles", [])
            speak("Here are the top news headlines.")
            for i, article in enumerate(articles[:5]):
                speak(f"{i+1}. {article.get('title', 'No title')}")
        except Exception:
            speak("I couldn't fetch the news at the moment.")
        return True
    if open_application(query):
        return True
    return False

def main():
    speak("Hello, how can I assist you today?")
    while True:
        query = listen()
        if not query:
            continue
        if any(word in query for word in ['exit', 'stop', 'sleep', 'bye']):
            speak("Shutting down systems. Goodbye!")
            break
        if not perform_task(query):
            speak("Sorry, I can't help with that request.")

if __name__ == "__main__":
    main()
