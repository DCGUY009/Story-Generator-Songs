import whisper
from datetime import timedelta

# Load Whisper model (use "medium" or "large" for better accuracy)
model = whisper.load_model("small")

# File paths (update if needed)
audio_path = "./Data/Audio/bilvashtakam_mp3.mp3"  # Audio file
lyrics_path = "./Data/Lyrics/Bilvashtakam_lyrics.txt"  # Correct lyrics file
srt_path = "./Data/SRT Files/bilvashtakam_corrected.srt"  # Output subtitle file

# Step 1: Transcribe the audio file (extracting only timestamps)
result = model.transcribe(audio_path, verbose=True, initial_prompt=lyrics_path, language="te")  # Force Telugu language
print("----------------------------------------------------------->")
print(f"Result:\n{result}")

# Step 2: Read provided lyrics
with open(lyrics_path, "r", encoding="utf-8") as f:
    lyrics_lines = [line.strip() for line in f.readlines() if line.strip()]
    print("----------------------------------------------------------->")
    print(f"Lyrics Lines:\n{lyrics_lines}")


# Step 3: Extract timestamps and align with lyrics
timestamps = result["segments"]  # Get Whisper's detected time segments
num_lines = min(len(timestamps), len(lyrics_lines))  # Match segment count

print("----------------------------------------------------------->")
print(f"Timestamps:\n{timestamps}")

print("----------------------------------------------------------->")
print(f"Num Lines:\n{num_lines}")


# Function to format time for SRT
def format_time(seconds):
    millisec = int((seconds - int(seconds)) * 1000)
    return str(timedelta(seconds=int(seconds))) + f",{millisec:03d}"

# Step 4: Generate SRT content with correct lyrics
srt_content = ""
for i in range(num_lines):
    start = format_time(timestamps[i]["start"])
    end = format_time(timestamps[i]["end"])
    text = lyrics_lines[i]  # Use correct lyrics instead of Whisper's text

    srt_content += f"{i+1}\n{start} --> {end}\n{text}\n\n"

print("----------------------------------------------------------->")
print(f"SRT Content:\n{srt_content}")


# Step 5: Save the corrected SRT file
with open(srt_path, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"SRT file generated: {srt_path}")
