import pandas as pd
import random
import os
from elevenlabs import generate, save, voices, set_api_key

# --- Config ---
csv_path = "sentences.csv"
text_column = "Text"  # change if your column is named differently
start_line = 1       # continue from here
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)
set_api_key("api")

# Load all available voices
all_voices = voices()

# Filter only voices with a known gender (i.e., skip music/sfx voices)
valid_voices = [v for v in all_voices if v.labels.get("gender") in ["male", "female"]]

print(f"Found {len(valid_voices)} usable voices.")

# --- Load CSV and start from line ---
df = pd.read_csv(csv_path)
lines = df[text_column].tolist()

for idx in range(start_line - 1, len(lines)):
    line_num = idx + 1
    text = str(lines[idx]).strip()
    if not text:
        continue

    voice = random.choice(valid_voices)
    print(f"Speaking line {line_num} with {voice.name} ({voice.labels.get('gender')})")


    try:
        audio = generate(
            text=text,
            voice=voice,
            model="eleven_monolingual_v1"
        )
        save(audio, f"{output_dir}/line_{line_num:03d}.mp3")
    except Exception as e:
        print(f"Error on line {line_num}: {e}")
