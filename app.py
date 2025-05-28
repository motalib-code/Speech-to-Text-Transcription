from flask import Flask, render_template, request, jsonify, send_file
import speech_recognition as sr
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import datetime
import tempfile

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB limit
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'wav'}

def transcribe_audio(audio_file_path):
    """Convert speech from an audio file to text."""
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text, None
    except sr.UnknownValueError:
        return None, "Could not understand audio"
    except sr.RequestError as e:
        return None, f"Could not request results; {e}"
    except Exception as e:
        return None, str(e)

def translate_text(text, target_lang='en'):
    """Translate text to target language."""
    try:
        translator = GoogleTranslator(source='auto', target=target_lang)
        translated_text = translator.translate(text)
        return translated_text, None
    except Exception as e:
        return None, str(e)

def text_to_speech(text, lang='en'):
    """Convert text to speech and save as audio file."""
    try:
        tts = gTTS(text=text, lang=lang)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        return temp_file.name, None
    except Exception as e:
        return None, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400
    
    try:
        # Save the uploaded file
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"audio_{timestamp}.{file.filename.rsplit('.', 1)[1].lower()}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Transcribe the audio
        text, error = transcribe_audio(filepath)
        if error:
            # Clean up the uploaded file before returning error
            os.remove(filepath)
            return jsonify({'error': error}), 400
        
        # Clean up the uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'text': text
        })
    
    except Exception as e:
        # Make sure to clean up the file in case of any error
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or 'text' not in data or 'target_lang' not in data:
        return jsonify({'error': 'Missing text or target language'}), 400
    
    text = data['text']
    target_lang = data['target_lang']
    
    translated_text, error = translate_text(text, target_lang)
    if error:
        return jsonify({'error': error}), 400
    
    return jsonify({
        'success': True,
        'translated_text': translated_text
    })

@app.route('/text-to-speech', methods=['POST'])
def convert_to_speech():
    data = request.get_json()
    if not data or 'text' not in data or 'lang' not in data:
        return jsonify({'error': 'Missing text or language'}), 400
    
    text = data['text']
    lang = data['lang']
    
    audio_file, error = text_to_speech(text, lang)
    if error:
        return jsonify({'error': error}), 400
    
    try:
        return send_file(
            audio_file,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='speech.mp3'
        )
    finally:
        # Clean up the temporary file
        os.unlink(audio_file)

if __name__ == '__main__':
    app.run(debug=True) 