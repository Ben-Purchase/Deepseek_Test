import speech_recognition as sr
import pyaudio

def interpret_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust these parameters to control listening duration
        timeout = 10  # Maximum time (in seconds) to wait for speech to start
        phrase_time_limit = 60  # Maximum time (in seconds) for a single phrase

        # Listen for speech with adjusted parameters
        audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        try:
            text = recognizer.recognize_google(audio)
            print(f"Interpreted speech: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return ""

if __name__ == "__main__":
    speech_text = interpret_speech()
    print(speech_text)