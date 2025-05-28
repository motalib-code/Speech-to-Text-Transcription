# Speech-to-Text & Translation Tool

A web-based tool that converts speech to text, translates text between languages, and converts text back to speech. Features a modern, user-friendly interface with drag-and-drop file upload.

## Features

- Web-based interface with drag-and-drop file upload
- Support for audio files up to 500MB
- Speech-to-text conversion
- Text translation between multiple languages
- Text-to-speech conversion
- Modern, responsive design
- Real-time processing with loading indicators

## Supported Languages

The tool supports translation and text-to-speech in the following languages:
- English
- Spanish
- French
- German
- Italian
- Portuguese
- Russian
- Japanese
- Korean
- Chinese

## Requirements

- Python 3.6 or higher
- Internet connection (for Google Speech Recognition API and translation services)
- Modern web browser (Chrome, Firefox, Safari, Edge)

## Installation

1. Clone this repository or download the files
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

Note: If you have trouble installing PyAudio on Windows, you might need to install it using a wheel file. Visit [https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) to download the appropriate wheel file for your Python version, then install it using:
```bash
pip install PyAudio‑0.2.13‑cp3x‑cp3x‑win_amd64.whl
```
(Replace the filename with the one you downloaded)

## Usage

1. Start the web server:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

3. Using the tool:
   - Drag and drop an audio file or click to select one
   - Wait for the transcription to appear
   - Use the language dropdown to select a target language
   - Click "Translate" to translate the text
   - Click "Text to Speech" to convert the text to speech and download as MP3

## Supported Audio Formats
- WAV
- AIFF
- FLAC
- MP3

## Notes
- The tool uses Google's Speech Recognition API for transcription
- Translation is powered by Google Translate
- Text-to-speech uses Google's Text-to-Speech service
- All processing is done in real-time
- Files are automatically deleted after processing
- Maximum file size is 500MB 