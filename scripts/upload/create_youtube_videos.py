#!/usr/bin/env python3
"""
🎬 CREATE YOUTUBE VIDEOS
========================

Script per creare file video completi per i canali YouTube.
Combina minimix audio con video di base per ogni programma.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 YouTube Videos
"""

import os
import sys
import subprocess
from datetime import datetime

class YouTubeVideoCreator:
    """Creatore di video per YouTube"""
    
    def __init__(self):
        # Configurazione server
        self.server_ip = "159.89.106.38"
        self.server_user = "root"
        
        # Data corrente
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        
        # File minimix
        self.blue_bossa_audio = "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3"
        self.meditative_tide_audio = "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3"
        self.abyss_audio = "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
        
        # Video di base
        self.blue_bossa_video = "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/video/Blue_Bossa_Guitar_On_The_Sand.mp4"
        self.meditative_tide_video = "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/video/Meditative Tide_Kid_Underwater.mp4"
        self.abyss_video = "/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss_Deep_Submarine.mp4"
        
        # Directory output
        self.output_dir = "/home/lofi/media/aqua/youtube_videos"
        
    def create_video(self, audio_path, video_path, output_name, title):
        """Crea video combinando audio e video"""
        print(f"🎬 Creazione video: {title}")
        
        # Comando FFmpeg per creare video
        ffmpeg_cmd = f"""ffmpeg -i '{video_path}' \\
    -i '{audio_path}' \\
    -map 0:v:0 -map 1:a:0 \\
    -c:v libx264 -preset medium -crf 18 \\
    -c:a aac -b:a 192k \\
    -shortest \\
    '{self.output_dir}/{output_name}.mp4'"""
        
        print(f"🔧 Comando FFmpeg:")
        print(ffmpeg_cmd)
        print()
        
        # Esegui comando sul server
        result = subprocess.run([
            'ssh', f'{self.server_user}@{self.server_ip}', 
            f'mkdir -p {self.output_dir} && {ffmpeg_cmd}'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Video creato: {output_name}.mp4")
            return True
        else:
            print(f"❌ Errore creazione video: {result.stderr}")
            return False
    
    def create_all_videos(self):
        """Crea tutti i video per YouTube"""
        print("🎬 CREAZIONE VIDEO YOUTUBE")
        print("=" * 30)
        
        # Verifica directory output
        subprocess.run([
            'ssh', f'{self.server_user}@{self.server_ip}', 
            f'mkdir -p {self.output_dir}'
        ])
        
        # 1. Blue Bossa
        blue_bossa_output = f"Blue_Bossa_Session_1_{self.current_date}"
        success1 = self.create_video(
            self.blue_bossa_audio,
            self.blue_bossa_video,
            blue_bossa_output,
            "Blue Bossa - Jazz Lofi Session"
        )
        
        # 2. Meditative Tide
        meditative_tide_output = f"Meditative_Tide_Session_1_{self.current_date}"
        success2 = self.create_video(
            self.meditative_tide_audio,
            self.meditative_tide_video,
            meditative_tide_output,
            "Meditative Tide - Ocean Lofi Session"
        )
        
        # 3. Abyss Deep
        abyss_output = f"Abyss_Deep_Session_1_{self.current_date}"
        success3 = self.create_video(
            self.abyss_audio,
            self.abyss_video,
            abyss_output,
            "Abyss Deep - Deep Ambient Session"
        )
        
        # Risultato finale
        if success1 and success2 and success3:
            print("\n🎉 TUTTI I VIDEO CREATI CON SUCCESSO!")
            print(f"📁 Directory: {self.output_dir}")
            print("\n📋 File creati:")
            print(f"  • {blue_bossa_output}.mp4")
            print(f"  • {meditative_tide_output}.mp4")
            print(f"  • {abyss_output}.mp4")
        else:
            print("\n❌ Alcuni video non sono stati creati correttamente")
            sys.exit(1)

def main():
    """Main function"""
    creator = YouTubeVideoCreator()
    creator.create_all_videos()

if __name__ == "__main__":
    main() 