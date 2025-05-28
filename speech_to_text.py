import speech_recognition as sr
import datetime
import os

def transcribe_from_microphone():
    """Record audio from microphone and convert to text."""
    recognizer = sr.Recognizer()
    
    print("Starting microphone recording...")
    print("Speak now (press Ctrl+C to stop)...")
    
    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            # Record audio
            audio = recognizer.listen(source)
            
        print("Processing speech...")
        # Use Google's speech recognition
        text = recognizer.recognize_google(audio)
        return text
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    except KeyboardInterrupt:
        print("\nRecording stopped by user")
        return None

def transcribe_from_file(audio_file_path):
    """Convert speech from an audio file to text."""
    if not os.path.exists(audio_file_path):
        print(f"Error: File {audio_file_path} not found")
        return None
        
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
            
        print("Processing audio file...")
        # Use Google's speech recognition
        text = recognizer.recognize_google(audio)
        return text
        
    except sr.UnknownValueError:
        print("Could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None

def save_transcription(text, output_file=None):
    """Save transcription to a file."""
    if text is None:
        return
        
    if output_file is None:
        # Create a filename with timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"transcription_{timestamp}.txt"
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Transcription saved to: {output_file}")
    except Exception as e:
        print(f"Error saving transcription: {e}")

def main():
    while True:
        print("\nSpeech-to-Text Transcription Tool")
        print("1. Record from microphone")
        print("2. Transcribe from audio file")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ")
        
        if choice == '1':
            text = transcribe_from_microphone()
            if text:
                print("\nTranscription:")
                print(text)
                save_transcription(text)
                
        elif choice == '2':
            file_path = input("Enter the path to your audio file: ")
            text = transcribe_from_file(file_path)
            if text:
                print("\nTranscription:")
                print(text)
                save_transcription(text)
                
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 