import os
import speech_recognition as sr
import pyttsx3
import pywhatkit
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import psutil
import pyautogui
import pygetwindow as gw
import time
import platform

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """Make the assistant speak."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for voice commands."""
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return None
        except sr.RequestError:
            speak("Could not request results from Google Speech Recognition service.")
            return None

def open_application(command):
    """Open specific applications."""
    if "firefox" in command:
        os.system("start firefox")
        speak("Opening Firefox.")
    elif "chrome" in command:
        os.system("start chrome")
        speak("Opening Chrome.")
    elif "settings" in command or "system settings" in command:
        if platform.system() == "Windows":
            os.system("start ms-settings:")
            speak("Opening system settings.")
        elif platform.system() == "Darwin":  # macOS
            os.system("open /System/Applications/System\ Preferences.app")
            speak("Opening System Preferences.")
        elif platform.system() == "Linux":
            os.system("gnome-control-center")  # Adjust based on your Linux distro
            speak("Opening System Settings.")
    elif "notepad" in command:
        os.system("notepad")
        speak("Opening Notepad.")
    elif "calculator" in command:
        os.system("calc")
        speak("Opening Calculator.")
    else:
        speak("Sorry, I can't open that application yet.")

def search_web(command):
    """Search the web for a query."""
    if "search for" in command:
        query = command.replace("search for", "").strip()
        speak(f"Searching for {query} on the web.")
        pywhatkit.search(query)
    elif "play" in command:
        song = command.replace("play", "").strip()
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)

def adjust_volume(level):
    """Adjust system volume."""
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level / 100.0, None)
    speak(f"Volume set to {level} percent.")

def process_command(command):
    """Process the given command and execute corresponding actions."""
    if "stop" in command:
        speak("Goodbye!")
        return False
    elif "hello" in command:
        speak("Hello! How are you?")
    elif "open" in command:
        open_application(command)
    elif "search for" in command or "play" in command:
        search_web(command)
    elif "set volume to" in command:
        try:
            level = int(command.split("set volume to")[1].strip())
            adjust_volume(level)
        except ValueError:
            speak("Please provide a valid number for the volume level.")
    elif "shutdown" in command:
        speak("Shutting down the laptop.")
        os.system("shutdown /s /f /t 0")  # Windows
    elif "sleep" in command:
        speak("Putting the laptop to sleep.")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Windows Sleep command
    elif "brightness" in command:
        set_brightness(command)
    else:
        speak("I didn't understand that command.")
    return True

def set_brightness(command):
    """Set the screen brightness (Windows only)."""
    try:
        if platform.system() == "Windows":
            if "increase" in command:
                current_brightness = pyautogui.screenshot().getbrightness()  # Placeholder for actual brightness adjustment
                new_brightness = min(current_brightness + 10, 100)
                # Adjust brightness here
                speak(f"Increasing brightness to {new_brightness}%.")
            elif "decrease" in command:
                current_brightness = pyautogui.screenshot().getbrightness()  # Placeholder for actual brightness adjustment
                new_brightness = max(current_brightness - 10, 0)
                # Adjust brightness here
                speak(f"Decreasing brightness to {new_brightness}%.")
            else:
                speak("Please specify if you want to increase or decrease the brightness.")
        else:
            speak("Brightness adjustment is only supported on Windows at the moment.")
    except Exception as e:
        speak(f"Could not adjust brightness: {str(e)}")



def main():
    """Main function to run LapBuddy."""
    while True:
      #  if detect_wake_word() == "hi lapbuddy":  # Replace with actual wake word detection
            #speak("Hi, I'm LapBuddy. How can I help you?")
            while True:
                command = listen()  # Listen for commands after the wake word is detected
                if command:
                    if not process_command(command):
                        break

if __name__ == "__main__":
    main()
