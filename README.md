# Whisper Transcription Service

A self-hosted service that uses OpenAI's Whisper model to transcribe audio files. This service is designed to work with n8n and other HTTP clients.

## Setup

1. Build the Docker image:
```bash
docker build -t whisper-service .
```

2. Run the container:
```bash
docker run -p 5000:5000 whisper-service
```

## API Endpoints

### POST /transcribe
Transcribe an audio file.

- Method: POST
- Content-Type: multipart/form-data
- Body parameter: `file` (audio file)
- Supported formats: WAV, MP3, OGG, M4A, FLAC

Example response:
```json
{
    "text": "Transcribed text content",
    "language": "detected language",
    "segments": [
        {
            "text": "segment text",
            "start": 0.0,
            "end": 2.5
        }
    ]
}
```

### GET /health
Check if the service is running.

## n8n Integration

To use this service in n8n:

1. Use the HTTP Request node
2. Set method to POST
3. Set URL to `http://your-server:5000/transcribe`
4. Set "Binary Data" to true
5. Connect a node that provides an audio file (like the Read Binary File node)
6. The response will contain the transcribed text and metadata

## Error Handling

The service will return appropriate HTTP status codes and error messages:
- 400: Bad Request (no file, empty file, or invalid file type)
- 500: Internal Server Error (transcription failed)
- 200: Success
