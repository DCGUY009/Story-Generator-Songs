import whisper
from datetime import timedelta

# Load Whisper model
model = whisper.load_model("medium")

# File paths (update with actual paths if needed)
audio_path = "./Data/Audio/bilvashtakam_mp3.mp3"
lyrics_path = "./Data/Lyrics/Bilvashtakam_lyrics.txt"
srt_path = "./Data/SRT Files/bilvashtakam.srt"

with open(lyrics_path, mode="r") as file:
    lyrics = file.read()

subtitles_lyrics_prompt = f"""
These are the lyrics of the song:
{lyrics}

Please provide an accurate mapping of each line in the lyrics with the timestamp it occurs in.
Take Timestamp for each sentence, not for each word. 

For example:
0:00:08,000 --> 0:00:14,000
త్రిదళం త్రిగుణాకారం త్రినేత్రం చ త్రియాయుధమ్ ।
"""
# Transcribe the audio file
result = model.transcribe(audio_path, verbose=True, temperature=0, initial_prompt=subtitles_lyrics_prompt, language="te")
print("----------------------------------------------------------->")
print(f"Result:\n{result}")

# Read provided lyrics
with open(lyrics_path, "r", encoding="utf-8") as f:
    lyrics_lines = [line.strip() for line in f.readlines() if line.strip()]
    print("----------------------------------------------------------->")
    print(f"Lyrics Lines: {lyrics_lines}")

# Align Whisper timestamps with provided lyrics
srt_content = ""
num_lines = min(len(result["segments"]), len(lyrics_lines))
print("----------------------------------------------------------->")
print(f"Num Lines:\n{num_lines}")

def format_time(seconds):
    """Convert seconds to SRT timestamp format."""
    millisec = int((seconds - int(seconds)) * 1000)
    return str(timedelta(seconds=int(seconds))) + f",{millisec:03d}"

for i in range(num_lines):
    start = format_time(result["segments"][i]["start"])
    end = format_time(result["segments"][i]["end"])
    text = lyrics_lines[i]

    srt_content += f"{i+1}\n{start} --> {end}\n{text}\n\n"
print("----------------------------------------------------------->")
print(f"Srt Content:\n{srt_content}")

# Save the aligned lyrics as an SRT file
with open(srt_path, "w", encoding="utf-8") as f:
    f.write(srt_content)

print(f"SRT file generated: {srt_path}")
