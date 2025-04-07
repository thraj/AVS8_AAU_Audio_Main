from elevenlabs import generate, save, voices, set_api_key
import random
import os
import pandas as pd

set_api_key("api")  # Replace this

# Load CSV
df = pd.read_csv("sentences.csv")

# Output folder
output_dir = "/Users/raj/University/AVS 8/Main Project Audio/tts_outputs"
os.makedirs(output_dir, exist_ok=True)

# Load all available voices
all_voices = voices()

# Filter only voices with a known gender (i.e., skip music/sfx voices)
valid_voices = [v for v in all_voices if v.labels.get("gender") in ["male", "female"]]

print(f"Found {len(valid_voices)} usable voices.")

# Loop and save
for idx, row in df.iterrows():
    text = row["text"]
    voice = random.choice(valid_voices)
    print(f"▶️ Speaking line {idx+1} with {voice.name} ({voice.labels['gender']})")

    audio = generate(
        text=text,
        voice=voice,
        model="eleven_multilingual_v2"
    )

    filename = os.path.join(output_dir, f"line_{idx+1}_{voice.name}.mp3")
    save(audio, filename)
