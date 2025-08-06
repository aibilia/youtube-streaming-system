#!/usr/bin/env python3
"""
📋 CHECK VIDEO FILES
===================

Script per verificare i file video esistenti e creare le playlist.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Check Files
"""

import os
import subprocess
from datetime import datetime

class VideoFileChecker:
    """Verificatore di file video"""
    
    def __init__(self):
        # Configurazione server
        self.server_ip = "159.89.106.38"
        self.server_user = "root"
        
        # Directory video
        self.video_dirs = [
            "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/video",
            "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/video", 
            "/home/lofi/media/aqua/ffmpeg_direct/abyss/video"
        ]
        
        # Directory output
        self.output_dir = "/home/lofi/media/aqua/youtube_videos"
        
    def check_video_files(self):
        """Verifica i file video esistenti"""
        print("📋 VERIFICA FILE VIDEO")
        print("=" * 25)
        
        all_files = {}
        
        for video_dir in self.video_dirs:
            print(f"\n🔍 Controllo directory: {video_dir}")
            
            # Lista file nella directory
            result = subprocess.run([
                'ssh', f'{self.server_user}@{self.server_ip}',
                f'ls -la "{video_dir}"/*.mp4 2>/dev/null || echo "Nessun file MP4 trovato"'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and "Nessun file MP4 trovato" not in result.stdout:
                files = result.stdout.strip().split('\n')
                all_files[video_dir] = files
                
                for file in files:
                    if file.strip():
                        print(f"  ✅ {file.split('/')[-1]}")
            else:
                print(f"  ❌ Nessun file MP4 trovato")
                all_files[video_dir] = []
        
        return all_files
    
    def check_audio_files(self):
        """Verifica i file audio esistenti"""
        print("\n🎵 VERIFICA FILE AUDIO")
        print("=" * 25)
        
        audio_files = {
            'blue_bossa': "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3",
            'meditative_tide': "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3",
            'abyss': "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
        }
        
        for name, path in audio_files.items():
            result = subprocess.run([
                'ssh', f'{self.server_user}@{self.server_ip}',
                f'test -f "{path}" && echo "OK" || echo "MISSING"'
            ], capture_output=True, text=True)
            
            if "OK" in result.stdout:
                print(f"  ✅ {name}: {path.split('/')[-1]}")
            else:
                print(f"  ❌ {name}: File mancante")
    
    def create_playlist_structure(self):
        """Crea la struttura delle playlist"""
        print("\n📁 CREAZIONE STRUTTURA PLAYLIST")
        print("=" * 35)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        playlists = {
            'blue_bossa': {
                'name': 'Blue Bossa - Jazz Lofi Sessions',
                'description': 'Sessioni jazz lofi con chitarra acustica per studio e relax',
                'videos': []
            },
            'meditative_tide': {
                'name': 'Meditative Tide - Ocean Lofi Sessions', 
                'description': 'Sessioni ambient oceaniche per meditazione e pace',
                'videos': []
            },
            'abyss_deep': {
                'name': 'Abyss Deep - Deep Ambient Sessions',
                'description': 'Sessioni deep ambient sottomarine per contemplazione',
                'videos': []
            }
        }
        
        # Crea directory playlist
        for playlist_name in playlists.keys():
            playlist_dir = f"/home/lofi/media/aqua/playlists/{playlist_name}"
            
            subprocess.run([
                'ssh', f'{self.server_user}@{self.server_ip}',
                f'mkdir -p "{playlist_dir}"'
            ])
            
            print(f"  📁 Creata playlist: {playlist_name}")
        
        return playlists
    
    def generate_upload_script(self):
        """Genera script per upload YouTube"""
        print("\n📤 GENERAZIONE SCRIPT UPLOAD")
        print("=" * 30)
        
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        upload_script = f"""#!/bin/bash
# YOUTUBE UPLOAD SCRIPT - {current_date}
# ======================================

echo "📤 UPLOAD VIDEO YOUTUBE"
echo "======================"

# Configurazione
VIDEO_DIR="/home/lofi/media/aqua/youtube_videos"
METADATA_DIR="/home/lofi/media/aqua/youtube_metadata"

# Upload Blue Bossa
echo "🎸 Upload Blue Bossa..."
youtube-upload \\
    --title="Blue Bossa, Session 1, {current_date}" \\
    --description="$(cat $METADATA_DIR/blue_bossa_metadata.txt)" \\
    --category="Music" \\
    --tags="jazzlofi,bluesbossa,chitarra,relax,studymusic,workmusic,lofi,jazz,chill,ambient,meditation,focus,productivity,calm,peaceful,instrumental,acoustic,guitar,beach,sunset,zen" \\
    --playlist="Blue Bossa - Jazz Lofi Sessions" \\
    "$VIDEO_DIR/Blue_Bossa_Session_1_{current_date}.mp4"

# Upload Meditative Tide  
echo "🌊 Upload Meditative Tide..."
youtube-upload \\
    --title="Meditative Tide, Session 1, {current_date}" \\
    --description="$(cat $METADATA_DIR/meditative_tide_metadata.txt)" \\
    --category="Music" \\
    --tags="oceanlofi,meditativetide,waves,meditation,ambient,relax,studymusic,workmusic,lofi,chill,ocean,peace,calm,zen,meditationmusic,focus,productivity,nature,water,flow,tranquility,serenity,mindfulness" \\
    --playlist="Meditative Tide - Ocean Lofi Sessions" \\
    "$VIDEO_DIR/Meditative_Tide_Session_1_{current_date}.mp4"

# Upload Abyss Deep
echo "🌌 Upload Abyss Deep..."
youtube-upload \\
    --title="Abyss Deep, Session 1, {current_date}" \\
    --description="$(cat $METADATA_DIR/abyss_deep_metadata.txt)" \\
    --category="Music" \\
    --tags="deepambient,abyssdeep,underwater,ambient,meditation,relax,studymusic,workmusic,lofi,chill,deep,ocean,peace,calm,zen,meditationmusic,focus,productivity,nature,water,depth,tranquility,serenity,mindfulness,submarine,abyss" \\
    --playlist="Abyss Deep - Deep Ambient Sessions" \\
    "$VIDEO_DIR/Abyss_Deep_Session_1_{current_date}.mp4"

echo "✅ Upload completato!"
"""
        
        # Salva script
        with open('scripts/youtube_upload.sh', 'w') as f:
            f.write(upload_script)
        
        # Rendi eseguibile
        subprocess.run(['chmod', '+x', 'scripts/youtube_upload.sh'])
        
        print("  ✅ Script upload creato: scripts/youtube_upload.sh")

def main():
    """Main function"""
    checker = VideoFileChecker()
    
    # Verifica file
    video_files = checker.check_video_files()
    checker.check_audio_files()
    
    # Crea playlist
    playlists = checker.create_playlist_structure()
    
    # Genera script upload
    checker.generate_upload_script()
    
    print("\n🎉 VERIFICA COMPLETATA!")
    print("=" * 20)
    print("📋 Prossimi passi:")
    print("  1. Esegui: python3 scripts/create_youtube_videos.py")
    print("  2. Verifica i file creati")
    print("  3. Esegui: ./scripts/youtube_upload.sh")

if __name__ == "__main__":
    main() 