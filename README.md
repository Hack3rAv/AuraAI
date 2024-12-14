







**Made by :** HackerAv Aka Avrodip Shee  
**Contact :** [avrodipff@gmail.com](mailto:avrodipff@gmail.com)

---

## Features

Aura AI offers a wide range of functionalities, including but not limited to:

1. **Voice Command Processing**:
   - Speech-to-Text (Google or Whisper API).
   - Speech-to-Speech responses using pyttsx3.
   
2. **System Control**:
   - Shutdown and restart the system with voice commands.
   - Display current time on request.
   - Open applications such as Notepad, Calculator, Word, Excel, and PowerPoint.
   
3. **Internet and Network Checking**:
   - Check internet connection status.
   - Measure internet speed (Download, Upload, Ping).
   
4. **Music and Media**:
   - Play MP3 songs from a designated directory.
   
5. **Web Navigation**:
   - Open websites (Google, YouTube, Facebook, etc.) by voice command.
   
---

## Installation

### Prerequisites
1. Python 3.x
2. Required Python libraries listed in `requirements.txt`.

### Installation Steps:

1. **Clone the repository:**
   - You can clone this repository using:
     ```bash
     git clone <repository_url>
     ```

2. **Install Dependencies:**
   - Navigate to the project folder.
   - Install the required dependencies using:
     ```bash
     pip install -r requirements.txt
     ```

3. **Run the Application:**
   - Once everything is set up, run the application with:
     ```bash
     python aura.py
     ```

---

## Code Explanation

The code is structured as follows:

1. **Import Libraries**:  
   `import os`, `sys`, `datetime`, `pyttsx3`, etc. are the necessary libraries imported for system control, speech recognition, network checking, and handling.

2. **Voice Command Handling**:
   - `say(text)` function handles the text-to-speech output using `pyttsx3`.
   - `takeCommand()` and `takeCommandOffline()` functions listen to the user's voice and convert it into text (using Google or Whisper).

3. **Checking Internet Connection**:
   - `check_internet()` checks if the system has internet connectivity by trying to connect to Google's DNS.
   - `check_connection_speed()` checks internet speed (download, upload, and ping).

4. **Command Processing**:
   - The main loop listens for commands like "open notepad", "play song", or "shutdown".
   - It then matches the query with predefined commands (e.g., `shutdown_q`, `restart_q`, etc.) and executes the respective function.

5. **Application Management**:
   - The `open_and_wait(target)` function opens and waits for a specified application to close.
   
6. **Web Navigation**:
   - The `open_website(website)` function opens a specified website in the default browser.
   
7. **Music Player**:
   - The `play_song(song_name)` function plays a song from a specified directory.

---

## Requirements

You will need the following Python libraries:

- `pyttsx3` - For text-to-speech functionality.
- `pyaudio` - Required for capturing microphone input.
- `speech_recognition` - For converting speech to text.
- `speedtest-cli` - To measure internet speed.
- `requests` - For HTTP requests.
- `whisper` - For offline speech recognition.
- `rich` - For enhanced terminal output formatting.
- `platform` - For platform-specific features like handling file paths and commands.

Install the dependencies with the following command:

```bash
pip install -r requirements.txt
