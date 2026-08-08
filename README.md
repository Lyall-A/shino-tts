ElevenLabs compatible API for Chatterbox TTS

# Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 main.py
```

## Usage
Note: The API doesn't use any voice settings from the request, only the text. For configuration check `config.json`
```bash
curl -X POST http://localhost:8080/v1/text-to-speech/0 \
    -H "Content-Type: application/json" \
    -d '{ "text": "Hello, World!" }' | ffplay -i pipe:0
```