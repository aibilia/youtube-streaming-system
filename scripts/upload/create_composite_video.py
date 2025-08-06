#!/usr/bin/env python3
"""
Crea un video composito che combina tutti e 3 i video in sequenza:
1. Blue Bossa (chitarra) 
2. Meditative Tide (kid meditating)
3. Abyss Deep (submarine)
"""

import subprocess
import os

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

def get_audio_duration(audio_file):
    """Ottiene la durata di un file audio"""
    cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
           "-of", "csv=p=0", audio_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())

def create_video_concat_file():
    """Crea il file di concatenazione video"""
    with open("/tmp/video_concat.txt", "w") as f:
        for i, video_file in enumerate(VIDEO_FILES):
            audio_duration = get_audio_duration(AUDIO_FILES[i])
            f.write(f"file '{video_file}'\n")
            f.write(f"duration {audio_duration}\n")
        # Ripeti l'ultimo video per il loop
        f.write(f"file '{VIDEO_FILES[-1]}'\n")
    
    print("✅ File di concatenazione video creato")

def create_composite_video():
    """Crea il video composito"""
    
    output_file = "/home/lofi/media/aqua/ffmpeg_direct/composite_video.mp4"
    
    # Crea file di concatenazione video
    create_video_concat_file()
    
    # Calcola durate
    durations = [get_audio_duration(audio) for audio in AUDIO_FILES]
    total_duration = sum(durations)
    
    print("🎬 CREAZIONE VIDEO COMPOSITO:")
    for i, (video, audio, duration) in enumerate(zip(VIDEO_FILES, AUDIO_FILES, durations)):
        hours = duration / 3600
        print(f"  {i+1}. {os.path.basename(video)}: {hours:.2f} ore")
    
    total_hours = total_duration / 3600
    print(f"📊 DURATA TOTALE: {total_hours:.2f} ore")
    
    # Comando FFmpeg per creare video composito
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", "/tmp/video_concat.txt",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "23",
        "-pix_fmt", "yuv420p",
        "-y",  # Sovrascrivi output
        output_file
    ]
    
    print("🚀 Creazione video composito...")
    print(f"📁 Output: {output_file}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Video composito creato con successo!")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore nella creazione del video: {e}")
        return None

def create_audio_concat_file():
    """Crea il file di concatenazione audio"""
    with open("/tmp/audio_concat.txt", "w") as f:
        for audio_file in AUDIO_FILES:
            f.write(f"file '{audio_file}'\n")
    print("✅ File di concatenazione audio creato")

if __name__ == "__main__":
    print("🎵 CREAZIONE VIDEO COMPOSITO PER STREAMING")
    print("=" * 50)
    
    # Crea video composito
    video_file = create_composite_video()
    
    if video_file:
        # Crea file di concatenazione audio
        create_audio_concat_file()
        
        print("\n🎯 PROSSIMI PASSI:")
        print("1. Video composito creato: /home/lofi/media/aqua/ffmpeg_direct/composite_video.mp4")
        print("2. File audio concatenato: /tmp/audio_concat.txt")
        print("3. Pronto per streaming con video sincronizzato!")
    else:
        print("❌ Errore nella creazione del video composito") 