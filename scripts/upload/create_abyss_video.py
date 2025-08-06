#!/usr/bin/env python3
"""
🌌 CREATE ABYSS DEEP VIDEO
==========================

Script per creare il video Abyss Deep per YouTube.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Abyss Video
"""

import subprocess
from datetime import datetime

def create_abyss_video():
    """Crea il video Abyss Deep"""
    print("🌌 CREAZIONE VIDEO ABYSS DEEP")
    print("=" * 30)
    
    # Configurazione
    server_ip = "159.89.106.38"
    server_user = "root"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # File sorgente
    audio_path = "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
    video_path = "/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4"
    output_dir = "/home/lofi/media/aqua/youtube_videos"
    output_name = f"Abyss_Deep_Session_1_{current_date}"
    
    # Comando FFmpeg
    ffmpeg_cmd = f"""ffmpeg -i '{video_path}' \\
    -i '{audio_path}' \\
    -map 0:v:0 -map 1:a:0 \\
    -c:v libx264 -preset medium -crf 18 \\
    -c:a aac -b:a 192k \\
    -shortest \\
    '{output_dir}/{output_name}.mp4'"""
    
    print(f"🎬 Creazione video: Abyss Deep - Deep Ambient Session")
    print(f"🔧 Comando FFmpeg:")
    print(ffmpeg_cmd)
    print()
    
    # Esegui comando
    result = subprocess.run([
        'ssh', f'{server_user}@{server_ip}', 
        f'{ffmpeg_cmd}'
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ Video creato: {output_name}.mp4")
        return True
    else:
        print(f"❌ Errore creazione video: {result.stderr}")
        return False

if __name__ == "__main__":
    create_abyss_video() 