import os
import sys
import datetime
import pyttsx3
import platform
import subprocess
import socket
import speech_recognition as sr
from rich.console import Console
import pyaudio
import webbrowser
import threading
import speedtest
import requests
import whisper

sys.stderr = open(os.devnull, 'w')

color = Console()

conversation_history = ""
model = "llama3.2:1b"

engine = pyttsx3.init()

time_q = {
    "what's the time",
    "what time is it",
    "tell me the time",
    "can you tell me the time",
    "please tell the time",
    "what is the time",
    "what is the time going on",
    "what's the time going on"
}

shutdown_q = {
    "shutdown the pc"
}

restart_q = {
    "restart the pc"
}

internet = [
    "check the internet",
    "internet status"
]

check_connection = [
    "what is the speed of the internet",
    "what is the speed of the internet",
    "check the speed of internet",
    "check the internet speed",
]

def say(text):
    """Text-to-Speech function."""
    engine.say(text)
    engine.runAndWait()

def check_internet():
    """Check if the machine is connected to the internet."""
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except (socket.timeout, socket.gaierror):
        return False

def takeCommand():
    """Take command using Google Speech-to-Text API."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening with Google...")
        try:
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=30, phrase_time_limit=30)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except sr.UnknownValueError:
            say("Sorry, I couldn't understand that. Could you please repeat?")
            return None  
        except sr.RequestError:
            say("Sorry, there was an issue with the speech recognition service.")
            return None 
        except Exception as e:
            say(f"Sorry, I encountered an error: {e}")
            return None  

def check_connection_speed():
    st = speedtest.Speedtest()
    
    # Get the best server based on ping
    st.get_best_server()
    
    # Measure download and upload speed
    download_speed = st.download() / 1_000_000  # Convert from bits/sec to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bits/sec to Mbps
    
    # Measure ping
    ping = st.results.ping
    
    return download_speed, upload_speed, ping

def takeCommandOffline():
    """Take command using Whisper for offline speech recognition."""
    try:
        model = whisper.load_model("base")
        print("Listening with Whisper...")
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source, timeout=30, phrase_time_limit=30)

            print("Processing audio with Whisper...")
            temp_path = "temp_audio.wav"
            with open(temp_path, "wb") as f:
                f.write(audio.get_wav_data())

            result = model.transcribe(temp_path, language="en")  # Specify language
            os.remove(temp_path)  # Clean up temporary audio file

            query = result["text"]
            print(f"User said: {query}")
            return query.lower()
    except Exception as e:
        say(f"Sorry, I encountered an error: {e}")
        return None

def aura(query):
    """AI query handler with memory."""
    global conversation_history
    try:
        print("Aura AI is thinking...")
        conversation_history += f"User: {query}\n"
        
        result = subprocess.run(
            ["wsl", "ollama", "run", model],
            input=query,
            text=True,
            capture_output=True,
            encoding="utf-8"
        )
        
        ai_response = result.stdout.strip()
        if not ai_response:
            raise ValueError("No response from AI model.")
        
        conversation_history += f"Aura: {ai_response}\n"
        color.print(f"[cyan]{ai_response}[/cyan]")
        say(ai_response)
        return ai_response
    except Exception as e:
        say(f"Error: The AI model did not respond. Details: {e}")
        return f"Error: {e}"

def open_and_wait(target):
    """Handles opening an app or file and waits for it to close."""
    try:
        # Extract the app name from the 'apps' dictionary
        app_name = [key for key, value in apps.items() if value == target][0].capitalize()

        say(f"Opening {app_name}")  # Say just the app name (e.g., "Opening Word")
        
        if platform.system() == "Windows":
            process = subprocess.Popen(target, shell=True)
        elif platform.system() == "Darwin":  # macOS
            process = subprocess.Popen(["open", target])
        else:  # Linux
            process = subprocess.Popen(["xdg-open", target])

        process.wait()  # Wait for the process to finish
        say(f"{app_name} closed successfully.")
        return  # Prevent AI query handling after app closure
    except Exception as e:
        say(f"Sorry, I couldn't open {target}. Error: {e}")
        return  # Prevent AI query handling after an error

def open_website(website):
    """Opens the website in the default web browser."""
    try:
        website_name = [key for key, value in websites.items() if value == website][0].capitalize()  # Get just the domain name (e.g., "YouTube")

        say(f"Opening {website_name}")  # Say just the website name
        webbrowser.open(website)  # Open the website in the default browser
        say(f"{website_name} opened successfully.")
    except Exception as e:
        say(f"Sorry, I couldn't open {website}. Error: {e}")

def play_song(song_name, music_directory="C:\\Users\\HackerAV\\Music"):
    """Plays the song from the music directory."""
    song_path = os.path.join(music_directory, f"{song_name}.mp3")
    if os.path.exists(song_path):
        try:
            say(f"Playing {song_name}")
            if platform.system() == "Windows":
                subprocess.Popen(["start", song_path], shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", song_path])
            else:  # Linux
                subprocess.Popen(["xdg-open", song_path])
            return f"Playing {song_name}"
        except Exception as e:
            say(f"Sorry, I encountered an error while playing {song_name}. Error: {e}")
            return f"Error playing {song_name}: {e}"
    else:
        say(f"Sorry, {song_name} not found.")
        return f"Error: {song_name} not found"

if __name__ == '__main__':
    print('Welcome to Aura AI')
    say("Aura AI With The Most Aura")

    apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "word": "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE",
        "powerpoint": "C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE",
        "excel": "C:\\Program Files\\Microsoft Office\\root\\Office16\\EXCEL.EXE"
    }

    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "facebook": "https://www.facebook.com",
        "twitter": "https://www.twitter.com",
        "github": "https://www.github.com"
    }

    if check_internet():
        print("Internet is available, using Google Speech-to-Text.")
    else:
        print("No internet detected, using Whisper.")

    while True:
        if check_internet():
            query = takeCommand()  
        else:
            query = takeCommandOffline()  

        if query is None:
            continue  

        if query == "shutdown aura":
            say("Aura is shutting down.")
            break

        app_opened = False
        for app_name, app_cmd in apps.items():
            if app_name in query:
                open_and_wait(app_cmd)
                app_opened = True
                break

        if app_opened:
            continue  # Skip AI query handling if an application was opened

        website_opened = False
        for website_name, website_url in websites.items():
            if website_name in query:
                open_website(website_url)
                website_opened = True
                break

        if website_opened:
            continue  # Skip AI query handling if a website was opened

        if query.lower().startswith("play "):
            song_name = query[5:].strip()
            play_song(song_name) 

        elif any(phrase in query for phrase in time_q):
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            color.print(f"[cyan]{current_time}[/cyan]")
            say(f"The time is {current_time}")

        elif any(phrase in query for phrase in shutdown_q):
            say("The PC will shut down in 10 seconds")
            os.system("shutdown /s /t 10")
        
        elif any(phrase in query for phrase in restart_q):
            say("The PC will restart in 10 seconds")
            os.system("shutdown /r /t 10")
        
        elif any(phrase in query for phrase in internet):
            if check_internet():
                say("The internet is connected")
            else:
                say("The internet is not connected")
        
        elif any(phrase in query for phrase in check_connection):
            download_speed, upload_speed, ping = check_connection_speed()
            color.print(f"[cyan]Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps, Ping: {ping} ms[/cyan]")
            say(f"Download Speed: {download_speed:.2f} Mbps, Upload Speed: {upload_speed:.2f} Mbps, Ping: {ping} ms")

        elif "what is your name" in query:
            color.print("I am Aura" , style= "bold green")
            say("I am Aura")

        else:
            aura(query)
