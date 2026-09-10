import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import wikipedia
import os
import re
import math
from urllib.parse import quote_plus
from gui import create_gui
# Text To Speech
engine = None
def speak(text, gui=None):
    global engine
    print("MAHA:", text)
    # Update GUI safely
    if gui:
        gui.root.after(
            0,
            lambda message=text: gui.add_message(
                "MAHA",
                message
            )
        )
    # Initialize TTS inside assistant thread
    if engine is None:
        engine = pyttsx3.init()
        engine.setProperty(
            "rate",
            170
        )
        engine.setProperty(
            "volume",
            1.0
        )
    engine.say(text)
    engine.runAndWait()

# Speech Recognition
recognizer = sr.Recognizer()
def listen(gui=None):
    try:
        with sr.Microphone() as source:
            print("Listening...")
            # Update GUI status
            if gui:
                gui.root.after(
                    0,
                    lambda: gui.update_status(
                        "LISTENING..."
                    )
                )
            audio = recognizer.listen(
                source,
                timeout=5,
                phrase_time_limit=8
            )

            # Update GUI status
            if gui:
                gui.root.after(
                    0,
                    lambda: gui.update_status(
                        "PROCESSING..."
                    )
                )
            command = recognizer.recognize_google(
                audio,
                language="en-IN"
            )

            print("You:", command)
            # Add command to GUI
            if gui:
                gui.root.after(
                    0,
                    lambda message=command: gui.add_message(
                        "YOU",
                        message
                    )
                )
            return command.lower().strip()
    except sr.WaitTimeoutError:
        print("No speech detected.")
        return ""
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""
    except sr.RequestError:
        speak(
            "Sorry, I am unable to connect to the speech service.",
            gui
        )
        return ""
    except Exception as e:
        print("Microphone error:", e)
        if gui:
            gui.root.after(
                0,
                lambda error=e: gui.add_message(
                    "SYSTEM",
                    f"Microphone error: {error}"
                )
            )
        return ""
# Wake Word Detection
def wait_for_wake_word(gui=None):
    # Wake word
    wake_words = [
        "hello"
    ]
    while True:
        if gui:
            gui.root.after(
                0,
                lambda: gui.update_status(
                    "WAITING FOR WAKE WORD..."
                )
            )
        command = listen(gui)
        if command:
            print(
                "Checking wake word:",
                command
            )
            for word in wake_words:
                if word in command:
                    speak(
                        "Yes, how can I help you?",
                        gui
                    )
                    return True
# Calculator
def calculate(command, gui=None):
    command = command.lower().strip()
    # Square Root
    match = re.search(
        r"square root of (\d+(?:\.\d+)?)",
        command
    )
    if match:
        num = float(
            match.group(1)
        )
        if num < 0:
            speak(
                "Sorry, I cannot find the square root of a negative number.",
                gui
            )
            return True
        result = math.sqrt(num)
        speak(
            f"The square root of {num:g} is {result:g}",
            gui
        )
        return True
    # Square
    match = re.search(
        r"square of (\d+(?:\.\d+)?)",
        command
    )
    if match:
        num = float(
            match.group(1)
        )
        result = num ** 2
        speak(
            f"The square of {num:g} is {result:g}",
            gui
        )
        return True
    # Percentage
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:percent|%)\s*(?:of)\s*(\d+(?:\.\d+)?)",
        command
    )
    if match:
        percentage = float(
            match.group(1)
        )
        number = float(
            match.group(2)
        )
        result = (
            percentage / 100
        ) * number
        speak(
            f"{percentage:g} percent of {number:g} is {result:g}",
            gui
        )
        return True
    # Power
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:power|to the power of)\s*(\d+(?:\.\d+)?)",
        command
    )
    if match:
        num1 = float(
            match.group(1)
        )
        num2 = float(
            match.group(2)
        )
        result = num1 ** num2
        speak(
            f"{num1:g} power {num2:g} is {result:g}",
            gui
        )
        return True
   
    # Remainder
    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(?:remainder|modulus|mod)\s*(?:of|by)?\s*(\d+(?:\.\d+)?)",
        command
    )
    if match:
        num1 = float(
            match.group(1)
        )
        num2 = float(
            match.group(2)
        )
        if num2 == 0:
            speak(
                "Sorry, I cannot calculate remainder with zero.",
                gui
            )
            return True
        result = num1 % num2
        speak(
            f"The remainder is {result:g}",
            gui
        )
        return True
    # Addition
    match = re.search(
        r"(?:add|plus)\s+(\d+(?:\.\d+)?)\s+(?:and|to)\s+(\d+(?:\.\d+)?)",
        command
    )
    if match:
        num1 = float(
            match.group(1)
        )
        num2 = float(
            match.group(2)
        )
        result = num1 + num2
        speak(
            f"The answer is {result:g}",
            gui
        )
        return True
    # Subtraction
    match = re.search(
        r"subtract\s+(\d+(?:\.\d+)?)\s+from\s+(\d+(?:\.\d+)?)",
        command
    )
    if match:

        num1 = float(
            match.group(2)
        )
        num2 = float(
            match.group(1)
        )
        result = num1 - num2
        speak(
            f"The answer is {result:g}",
            gui
        )
        return True
    # Multiplication
    match = re.search(
        r"(?:multiply|times)\s+(\d+(?:\.\d+)?)\s+(?:and|by)\s+(\d+(?:\.\d+)?)",
        command
    )
    if match:

        num1 = float(
            match.group(1)
        )

        num2 = float(
            match.group(2)
        )

        result = num1 * num2

        speak(
            f"The answer is {result:g}",
            gui
        )

        return True

    # -------------------------
    # Division
    # -------------------------

    match = re.search(
        r"divide\s+(\d+(?:\.\d+)?)\s+by\s+(\d+(?:\.\d+)?)",
        command
    )

    if match:

        num1 = float(
            match.group(1)
        )

        num2 = float(
            match.group(2)
        )

        if num2 == 0:

            speak(
                "Sorry, I cannot divide by zero.",
                gui
            )

            return True

        result = num1 / num2

        speak(
            f"The answer is {result:g}",
            gui
        )

        return True

    return False


# -----------------------------
# Execute Commands
# -----------------------------

def execute_command(command, gui=None):

    # -------------------------
    # What Can Maha Do?
    # -------------------------

    if (
        "what will you do" in command
        or "what can you do" in command
        or "what do you do" in command
    ):

        speak(
            "I can tell you the time and date, "
            "open Google and YouTube, "
            "search the web, "
            "search Wikipedia, "
            "open Notepad and Calculator, "
            "play music, and perform calculations "
            "such as addition, subtraction, "
            "multiplication, division, percentage, "
            "square, square root, power and remainder.",
            gui
        )

    # -------------------------
    # Calculator
    # -------------------------

    elif calculate(
        command,
        gui
    ):

        pass

    # -------------------------
    # Time
    # -------------------------

    elif "time" in command:

        current_time = datetime.datetime.now().strftime(
            "%I:%M %p"
        )

        speak(
            f"The time is {current_time}",
            gui
        )

    # -------------------------
    # Date
    # -------------------------

    elif "date" in command:

        current_date = datetime.datetime.now().strftime(
            "%d %B %Y"
        )

        speak(
            f"Today's date is {current_date}",
            gui
        )

    # -------------------------
    # Google
    # -------------------------

    elif "open google" in command:

        speak(
            "Opening Google",
            gui
        )

        webbrowser.open(
            "https://www.google.com"
        )

    # -------------------------
    # YouTube
    # -------------------------

    elif "open youtube" in command:

        speak(
            "Opening YouTube",
            gui
        )

        webbrowser.open(
            "https://www.youtube.com"
        )

    # -------------------------
    # Google Search
    # -------------------------

    elif command.startswith("search"):

        search_query = command.replace(
            "search",
            "",
            1
        ).strip()

        if search_query:

            speak(
                f"Searching for {search_query}",
                gui
            )

            encoded_query = quote_plus(
                search_query
            )

            webbrowser.open(
                "https://www.google.com/search?q="
                + encoded_query
            )

        else:

            speak(
                "What would you like me to search?",
                gui
            )

    # -------------------------
    # Wikipedia
    # -------------------------

    elif command.startswith("wikipedia"):

        topic = command.replace(
            "wikipedia",
            "",
            1
        ).strip()

        if topic:

            speak(
                f"Searching Wikipedia for {topic}",
                gui
            )

            try:

                result = wikipedia.summary(
                    topic,
                    sentences=2
                )

                speak(
                    result,
                    gui
                )

            except wikipedia.exceptions.DisambiguationError:

                speak(
                    "There are multiple results for that topic. "
                    "Please be more specific.",
                    gui
                )

            except wikipedia.exceptions.PageError:

                speak(
                    "Sorry, I could not find that Wikipedia page.",
                    gui
                )

            except wikipedia.exceptions.HTTPTimeoutError:

                speak(
                    "Wikipedia is taking too long to respond.",
                    gui
                )

            except Exception as e:

                print(
                    "Wikipedia error:",
                    e
                )

                speak(
                    "Sorry, I could not find that information.",
                    gui
                )

        else:

            speak(
                "Please tell me what you want to search on Wikipedia.",
                gui
            )

    # -------------------------
    # Notepad
    # -------------------------

    elif "open notepad" in command:

        speak(
            "Opening Notepad",
            gui
        )

        os.system(
            "notepad.exe"
        )

    # -------------------------
    # Calculator App
    # -------------------------

    elif "open calculator" in command:

        speak(
            "Opening Calculator",
            gui
        )

        os.system(
            "calc.exe"
        )

    # -------------------------
    # Music
    # -------------------------

    elif "play music" in command:

        speak(
            "Opening YouTube Music",
            gui
        )

        webbrowser.open(
            "https://music.youtube.com"
        )

    # -------------------------
    # Stop
    # -------------------------

    elif (
        command == "stop"
        or command == "exit"
        or command == "quit"
        or command == "goodbye"
        or "stop maha" in command
        or "exit maha" in command
    ):

        speak(
            "Goodbye. Have a nice day!",
            gui
        )

        return False

   
    # Unknown Command
  

    else:

        speak(
            "Sorry, I don't understand that command yet.",
            gui
        )

    return True



# Main Assistant


def start_assistant(gui=None):

    global engine

    # Initialize TTS inside assistant thread

    engine = pyttsx3.init()

    engine.setProperty(
        "rate",
        170
    )

    engine.setProperty(
        "volume",
        1.0
    )

    # -------------------------
    # Calibrate Microphone
    # -------------------------

    try:

        with sr.Microphone() as source:

            print(
                "Calibrating microphone..."
            )

            if gui:

                gui.root.after(
                    0,
                    lambda: gui.update_status(
                        "CALIBRATING MICROPHONE..."
                    )
                )

            recognizer.adjust_for_ambient_noise(
                source,
                duration=1
            )

        print(
            "Microphone calibration complete."
        )

    except Exception as e:

        print(
            "Microphone initialization error:",
            e
        )

        if gui:

            gui.root.after(
                0,
                lambda error=e: gui.add_message(
                    "SYSTEM",
                    f"Microphone error: {error}"
                )
            )

        return

    # Maha Introduction
   

    speak(
        "Hello! I am Maha, your AI voice assistant.",
        gui
    )

    speak(
        "Say Hello when you need me.",
        gui
    )

# Main Loop
    
    while True:

        # Wait for "Hello"

        wake_detected = wait_for_wake_word(
            gui
        )

        if not wake_detected:

            continue

        # Listen for actual command

        command = listen(
            gui
        )

        if not command:

            speak(
                "I didn't hear your command.",
                gui
            )

            continue

        # Execute command

        running = execute_command(
            command,
            gui
        )

        # Stop assistant

        if not running:

            break
# Start GUI
if __name__ == "__main__":

    create_gui(
        start_assistant
    )

