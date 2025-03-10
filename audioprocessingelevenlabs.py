import os
import requests
import json
from datetime import timedelta
from dotenv import load_dotenv
from difflib import SequenceMatcher

load_dotenv()

# 🔹 API Key & File Paths
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
AUDIO_FILE = "./Data/Audio/bilvashtakam_mp3.mp3"  # Audio file
LYRICS_FILE = "./Data/Lyrics/Bilvashtakam_lyrics.txt"  # Lyrics file
SRT_FILE = "./Data/SRT Files/bilvashtakam_elevenlabs.srt"  # Output SRT file

# 🔹 ElevenLabs API Endpoint
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/speech-to-text"

def format_time(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,ms)"""
    millisec = int((seconds - int(seconds)) * 1000)
    return str(timedelta(seconds=int(seconds))) + f",{millisec:03d}"

def similar(a, b):
    """Returns similarity ratio between two strings"""
    return SequenceMatcher(None, a, b).ratio()

def align_transcription_with_lyrics(transcription, lyrics):
    """Align transcribed words with correct lyrics based on phonetic similarity."""
    srt_content = ""
    words = [w for w in transcription["words"] if w["type"] == "word"]  # Ignore spacing/audio_event
    num_lines = min(len(words), len(lyrics))  # Match number of lines

    print(f"🔹 Words in Transcription: {len(words)}, Lines in Lyrics: {len(lyrics)}")

    for i in range(num_lines):
        transcribed_word = words[i]["text"]
        start = format_time(words[i]["start"])
        end = format_time(words[i]["end"])

        # Match lyrics based on best similarity
        matched_lyric = max(lyrics, key=lambda l: similar(transcribed_word, l))

        srt_content += f"{i+1}\n{start} --> {end}\n{matched_lyric}\n\n"

    return srt_content

def save_srt_file(srt_content, output_path):
    """Save SRT content to a file"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

def main():
    try:
        # STEP 1: Read correct lyrics
        with open(LYRICS_FILE, "r", encoding="utf-8") as f:
            lyrics_lines = [line.strip() for line in f.readlines() if line.strip()]

        # STEP 2: Send audio to ElevenLabs for transcription
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        files = {"file": open(AUDIO_FILE, "rb")}
        data = {
            "model_id": "scribe_v1",
            "language_code": "te",  # Telugu
            "timestamps_granularity": "word"
        }

        response = requests.post(ELEVENLABS_URL, headers=headers, files=files, data=data)

        if response.status_code != 200:
            print(f"❌ API Error: {response.text}")
            return

        transcript_data = response.json()

        print("---------------------------------------------------------->")
        print(f"Transcript Data:\n {transcript_data}")

        # STEP 3: Align transcription with lyrics
        srt_content = align_transcription_with_lyrics(transcript_data, lyrics_lines)

        print("---------------------------------------------------------->")
        print(f"SRT Content:\n {srt_content}")

        # STEP 4: Save SRT file
        save_srt_file(srt_content, SRT_FILE)

        print(f"✅ SRT file generated successfully: {SRT_FILE}")

    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    main()
