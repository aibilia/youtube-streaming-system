#!/usr/bin/env python3
"""
Streaming con sequenza video corretta:
1. Blue Bossa (chitarra) 
2. Meditative Tide (kid meditating)
3. Abyss Deep (submarine)
"""

import subprocess
import time
import os
import signal
import sys

# Configurazione
YOUTUBE_KEY = "ghfr-q9tg-42fs-xmv7-1fjy"
RTMP_URL = f"rtmp://a.rtmp.youtube.com/live2/{YOUTUBE_KEY}"

# Percorsi audio
AUDIO_FILES = [
    "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3",
    "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3", 
    "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
]

# Percorsi video corrispondenti
VIDEO_FILES = [
    "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/video/Blue Bossa_Guitar.mp4",
    "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/video/Meditative Tide_Kid Meditating.mp4",
    "/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4"
]

def create_concat_file():
    """Crea il file di concatenazione audio"""
    with open("/tmp/aqua_concat_sequence.txt", "w") as f:
        for audio_file in AUDIO_FILES:
            f.write(f"file '{audio_file}'\n")
    print("✅ File di concatenazione audio creato")

def get_audio_duration(audio_file):
    """Ottiene la durata di un file audio"""
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
           "-of", "csv=p=0", audio_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def calculate_sequence_timing():
    """Calcola i tempi di ogni sezione"""
    timings = []
    current_time = 0
    
    for audio_file in AUDIO_FILES:
        duration = get_audio_duration(audio_file)
        timings.append({
            'start': current_time,
            'end': current_time + duration,
            'duration': duration,
            'audio_file': audio_file
        })
        current_time += duration
    
    return timings

def start_streaming():
    """Avvia lo streaming con sequenza video"""
    
    # Crea file di concatenazione
    create_concat_file()
    
    # Calcola timing
    timings = calculate_sequence_timing()
    
    print("🎵 SEQUENZA STREAMING:")
    for i, timing in enumerate(timings):
        hours = timing['duration'] / 3600
        print(f"  {i+1}. {os.path.basename(timing['audio_file'])}: {hours:.2f} ore")
    
    total_hours = sum(t['duration'] for t in timings) / 3600
    print(f"📊 CICLO TOTALE: {total_hours:.2f} ore")
    
    # Comando FFmpeg con video dinamico
    cmd = [
        "ffmpeg",
        "-re",  # Read input at native frame rate
        "-stream_loop", "-1",  # Loop video infinitamente
        "-i", VIDEO_FILES[0],  # Video iniziale (Blue Bossa)
        "-f", "concat",
        "-safe", "0", 
        "-stream_loop", "-1",
        "-i", "/tmp/aqua_concat_sequence.txt",
        "-map", "0:v:0",  # Video dal primo input
        "-map", "1:a:0",  # Audio dal secondo input (concatenazione)
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-b:v", "6800k",
        "-c:a", "aac", 
        "-b:a", "128k",
        "-f", "flv",
        RTMP_URL
    ]
    
    print("🚀 Avvio streaming...")
    print(f"📺 Video iniziale: {os.path.basename(VIDEO_FILES[0])}")
    print(f"🎧 Audio: Concatenazione di {len(AUDIO_FILES)} minimix")
    
    try:
        process = subprocess.Popen(cmd)
        print(f"✅ Streaming avviato con PID: {process.pid}")
        
        # Mantieni il processo attivo
        process.wait()
        
    except KeyboardInterrupt:
        print("\n⏹️ Interruzione richiesta dall'utente")
        if process:
            process.terminate()
            process.wait()
        print("✅ Streaming fermato")

if __name__ == "__main__":
    start_streaming() 