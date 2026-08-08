import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS
# from chatterbox.tts_turbo import ChatterboxTurboTTS
from flask import Flask, request, send_file
import json
import tempfile

from torchcodec.encoders import AudioEncoder

# Load config
with open("config.json", "r") as file:
    config = json.load(file)

# Configs
device = config.get("device")
if not device:
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"

host = config.get("host")
port = config.get("port")
audio_prompt = config.get("audioPrompt", "input.wav")
audio_format = config.get("audioFormat", "wav")
audio_mime_type = config.get("audioMimeType", "audio/wav")
cfg_weight = config.get("cfgWeight", 0.5)
exaggeration = config.get("exaggeration", 0.5)
repetition_penalty = config.get("repetitionPenalty", 1.2)
temperature = config.get("temperature", 0.8)
min_p = config.get("minP", 0.05)
top_p = config.get("topP", 1)

# Load model
print(f"Loading model with {device.upper()}...")
model = ChatterboxTTS.from_pretrained(device=device)
# model = ChatterboxTurboTTS.from_pretrained(device=device)

# Create flask app
app = Flask(__name__)

# /v1/text-to-speech/:voice_id
@app.route("/v1/text-to-speech/<voice_id>", methods=["POST"])
def text_to_speech(voice_id):
    data = request.get_json()
    text = data.get("text")

    print(f"Generating speech for text \"{text}\"...")

    generated = model.generate(
        text=text,
        audio_prompt_path=audio_prompt,
        cfg_weight=cfg_weight,
        exaggeration=exaggeration,
        repetition_penalty=repetition_penalty,
        temperature=temperature,
        min_p=min_p,
        top_p=top_p
    )

    with tempfile.NamedTemporaryFile(suffix=f".{audio_format}") as file:
        ta.save(
            uri=file.name,
            src=generated,
            sample_rate=model.sr,
            format=audio_format
        )

        return send_file(file.name, mimetype=audio_mime_type)

if __name__ == "__main__":
    # Start server
    app.run(host=host, port=port)
