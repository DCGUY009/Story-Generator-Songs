import json
import os
from dotenv import load_dotenv
from deepgram import DeepgramClient, PrerecordedOptions, FileSource
from datetime import timedelta

load_dotenv()

# File paths
audio_path = "./Data/Audio/bilvashtakam_mp3.mp3"  # Audio file
lyrics_path = "./Data/Lyrics/Bilvashtakam_lyrics.txt"  # Correct lyrics file
srt_path = "./Data/SRT Files/bilvashtakam_deepgram.srt"  # Output subtitle file

# Set your Deepgram API key
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

def format_time(seconds):
    """Convert seconds to SRT timestamp format (HH:MM:SS,ms)"""
    millisec = int((seconds - int(seconds)) * 1000)
    return str(timedelta(seconds=int(seconds))) + f",{millisec:03d}"

def convert_to_srt(transcription, lyrics):
    """Align Deepgram timestamps with provided lyrics and create an SRT file"""
    srt_content = ""
    segments = transcription["results"]["utterances"]
    num_lines = min(len(segments), len(lyrics))  # Ensure correct mapping

    for i in range(num_lines):
        start = format_time(segments[i]["start"])
        end = format_time(segments[i]["end"])
        text = lyrics[i]  # Use correct lyrics instead of Deepgram's text

        srt_content += f"{i+1}\n{start} --> {end}\n{text}\n\n"

    return srt_content

def save_srt_file(srt_content, output_path):
    """Save SRT content to a file"""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

def main():
    try:
        # STEP 1: Create a Deepgram client
        deepgram = DeepgramClient(DEEPGRAM_API_KEY)

        with open(audio_path, "rb") as file:
            buffer_data = file.read()

        payload: FileSource = {"buffer": buffer_data}

        # STEP 2: Configure Deepgram options
        options = PrerecordedOptions(
            model="nova-3",  # Best model for transcription
            smart_format=True,
            utterances=True,  # Enables word-level timestamps
            punctuate=True
        )

        # STEP 3: Transcribe audio (Extract timestamps only)
        response = deepgram.listen.rest.v("1").transcribe_file(payload, options)
        transcript_data = json.loads(response.to_json())

        # STEP 4: Read the correct lyrics
        with open(lyrics_path, "r", encoding="utf-8") as f:
            lyrics_lines = [line.strip() for line in f.readlines() if line.strip()]

        # STEP 5: Convert to SRT format using correct lyrics
        srt_content = convert_to_srt(transcript_data, lyrics_lines)

        # STEP 6: Save SRT file
        save_srt_file(srt_content, srt_path)

        print(f"SRT file generated successfully: {srt_path}")

    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    main()
