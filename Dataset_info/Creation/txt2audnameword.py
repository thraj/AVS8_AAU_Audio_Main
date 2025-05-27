import pandas as pd
import random
import os
from elevenlabs import generate, save, voices, set_api_key

# --- Config ---
csv_path = "/Users/raj/University/AVS 8/AVS8_AAU_Audio_Main/Tapad/word.csv"
text_column = "Text"  # column in CSV with words like 'anus', 'fuck', etc.
start_line = 1
output_dir = "/Users/raj/University/AVS 8/AVS8_AAU_Audio_Main/Tapad/newaudio/ten"
os.makedirs(output_dir, exist_ok=True)

# Set your ElevenLabs API key
set_api_key("API_KEY")

# --- Load available voices ---
all_voices = voices()
valid_voices = [v for v in all_voices if v.labels.get("gender") in ["male", "female"]]
print(f"Found {len(valid_voices)} usable voices.")

# --- Load the CSV ---
df = pd.read_csv(csv_path)
lines = df[text_column].tolist()

# --- Loop through words and generate audio ---
for idx in range(start_line - 1, len(lines)):
    line_num = idx + 1
    text = str(lines[idx]).strip()

    if not text:
        continue

    # Sanitize filename
    filename = f"{text.lower().replace(' ', '_')}.mp3"
    output_path = os.path.join(output_dir, filename)

    if os.path.exists(output_path):
        print(f"Skipping existing file: {filename}")
        continue

    # Pick a random voice
    voice = random.choice(valid_voices)
    print(f"🗣️ Line {line_num}: '{text}' → Voice: {voice.name} ({voice.labels.get('gender')})")

    # Generate and save audio
    try:
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        save(audio, output_path)
        print(f"Saved: {filename}")
    except Exception as e:
        print(f"Error on line {line_num}: {e}")
