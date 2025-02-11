import os
import whisper
import torch
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg', 'm4a', 'flac'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Whisper model
device = "cpu"
model = whisper.load_model("tiny")  # Using tiny model for faster processing
model.to(device)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # Check if a file was sent in the request
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    # Check if a file was selected
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename and save the file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Convert to mono
            audio = AudioSegment.from_file(filepath)
            audio = audio.set_channels(1)  # Convert to mono
            mono_filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'mono_' + os.path.splitext(filename)[0] + '.wav')
            audio.export(mono_filepath, format='wav')
            
            # Remove the original file
            os.remove(filepath)
            
            # Transcribe the mono audio file
            result = model.transcribe(mono_filepath)
            
            # Clean up the mono file
            os.remove(mono_filepath)
            
            # Return the transcription
            return jsonify({
                'text': result['text'],
                'language': result.get('language', 'unknown'),
                'segments': result.get('segments', [])
            })
            
        except Exception as e:
            # Clean up files in case of error
            if os.path.exists(filepath):
                os.remove(filepath)
            if os.path.exists(mono_filepath):
                os.remove(mono_filepath)
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
