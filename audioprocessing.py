import whisper
from datetime import timedelta

# Load Whisper model
model = whisper.load_model("medium")

# File paths (update with actual paths if needed)
audio_path = "./Data/Audio/bilvashtakam_mp3.mp3"
lyrics_path = "./Data/Lyrics/Bilvashtakam_lyrics.txt"
srt_path = "./Data/SRT Files/bilvashtakam.srt"

# Transcribe the audio file
result = model.transcribe(audio_path)

# Read provided lyrics
with open(lyrics_path, "r", encoding="utf-8") as f:
    lyrics_lines = [line.strip() for line in f.readlines() if line.strip()]

# Align Whisper timestamps with provided lyrics
srt_content = ""
num_lines = min(len(result["segments"]), len(lyrics_lines))

def format_time(seconds):
    """Convert seconds to SRT timestamp format."""
    millisec = int((seconds - int(seconds)) * 1000)
    return str(timedelta(seconds=int(seconds))) + f",{millisec:03d}"

for i in range(num_lines):
    start = format_time(result["segments"][i]["start"])
    end = format_time(result["segments"][i]["end"])
    text = lyrics_lines[i]

    srt_content += f"{i+1}\n{start} --> {end}\n{text}\n\n"

# Save the aligned lyrics as an SRT file
with open(srt_path, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"SRT file generated: {srt_path}")
