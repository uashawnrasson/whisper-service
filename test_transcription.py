from gtts import gTTS
import requests
import os

# Create a test audio file
text = "Hello, this is a test of the Whisper transcription service. It should transcribe this audio accurately."
tts = gTTS(text=text, lang='en')
audio_file = "test_audio.mp3"
tts.save(audio_file)

print("Created test audio file...")

# Send the file to our service
url = "http://localhost:5001/transcribe"
files = {
    'file': ('test_audio.mp3', open(audio_file, 'rb'), 'audio/mpeg')
}

print("Sending file to transcription service...")
response = requests.post(url, files=files)
print("\nResponse from service:")
print(response.json())

# Clean up
os.remove(audio_file)
print("\nTest complete!")
