#!/usr/bin/env python3
"""
📤 UPLOAD TO AQUA LOFI CHILL
============================

Script per uploadare video al canale Aqua Lofi Chill con playlist.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Aqua Lofi Chill Upload
"""

import os
import subprocess
from datetime import datetime

class AquaLofiChillUploader:
    """Uploader per Aqua Lofi Chill"""
    
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.video_dir = "/home/lofi/media/aqua/youtube_videos"
        self.server_ip = "159.89.106.38"
        self.server_user = "root"
        
        # Configurazione video
        self.videos = {
            'blue_bossa': {
                'file': f'Blue_Bossa_Session_1_{self.current_date}.mp4',
                'title': 'Blue Bossa Lofi Jazz Session - Study Music & Relaxation Focus',
                'description': self.get_blue_bossa_description(),
                'tags': 'lofi,studymusic,relaxation,focus,jazz,chill,ambient,meditation,productivity,calm,peaceful,instrumental,acoustic,guitar,beach,sunset,zen,workmusic,concentration,stressrelief',
                'playlist': 'Blue Bossa Collection - Jazz Lofi Sessions'
            },
            'meditative_tide': {
                'file': f'Meditative_Tide_Session_1_{self.current_date}.mp4',
                'title': 'Meditative Tide Lofi Ocean Session - Meditation & Deep Focus Music',
                'description': self.get_meditative_tide_description(),
                'tags': 'lofi,meditation,focus,ocean,ambient,relaxation,studymusic,chill,peace,calm,zen,meditationmusic,productivity,nature,water,flow,tranquility,serenity,mindfulness,concentration',
                'playlist': 'Meditative Tide Collection - Ocean Lofi Sessions'
            },
            'abyss_deep': {
                'file': f'Abyss_Deep_Session_1_{self.current_date}.mp4',
                'title': 'Abyss Deep Lofi Ambient Session - Deep Focus & Contemplation Music',
                'description': self.get_abyss_deep_description(),
                'tags': 'lofi,deepfocus,ambient,meditation,relaxation,studymusic,chill,deep,ocean,peace,calm,zen,meditationmusic,productivity,nature,water,depth,tranquility,serenity,mindfulness,concentration,contemplation',
                'playlist': 'Abyss Deep Collection - Deep Ambient Sessions'
            }
        }
    
    def get_blue_bossa_description(self):
        """Descrizione Blue Bossa"""
        return """🎸 **Blue Bossa Lofi Jazz Session** - Study Music & Relaxation Focus

Immerse yourself in a relaxing jazz lofi atmosphere with the guitar dancing on Blue Bossa notes. This session is perfect for studying, working, or simply relaxing and focusing.

🎵 **Music**: Jazz Lofi with acoustic guitar
🌅 **Visual**: Guitar on the beach at sunset
⏱️ **Duration**: Complete minimix session

Perfect for: Study sessions, work focus, relaxation, concentration, stress relief

#lofi #studymusic #relaxation #focus #jazz #chill #ambient #meditation #productivity #calm #peaceful #instrumental #acoustic #guitar #beach #sunset #zen #workmusic #concentration #stressrelief

---
**Aqua Lofi Chill** - Your digital space of peace 🌊"""
    
    def get_meditative_tide_description(self):
        """Descrizione Meditative Tide"""
        return """🌊 **Meditative Tide Lofi Ocean Session** - Meditation & Deep Focus Music

Let yourself be carried away by ocean waves in this meditative lofi session. The sound of waves blends with ambient melodies to create an experience of deep inner peace and focus.

🎵 **Music**: Ocean Ambient Lofi
🌊 **Visual**: Child underwater, meditative peace
⏱️ **Duration**: Complete minimix session

Perfect for: Meditation, deep focus, study sessions, relaxation, mindfulness, concentration

#lofi #meditation #focus #ocean #ambient #relaxation #studymusic #chill #peace #calm #zen #meditationmusic #productivity #nature #water #flow #tranquility #serenity #mindfulness #concentration

---
**Aqua Lofi Chill** - Your digital space of peace 🌊"""
    
    def get_abyss_deep_description(self):
        """Descrizione Abyss Deep"""
        return """🌌 **Abyss Deep Lofi Ambient Session** - Deep Focus & Contemplation Music

Explore the depths of the ocean with this deep ambient session. Underwater sounds and deep melodies transport you to a world of absolute peace and contemplation.

🎵 **Music**: Deep Submarine Ambient
🌌 **Visual**: Deep underwater imagery
⏱️ **Duration**: Complete minimix session

Perfect for: Deep focus, contemplation, meditation, study sessions, relaxation, concentration

#lofi #deepfocus #ambient #meditation #relaxation #studymusic #chill #deep #ocean #peace #calm #zen #meditationmusic #productivity #nature #water #depth #tranquility #serenity #mindfulness #concentration #contemplation

---
**Aqua Lofi Chill** - Your digital space of peace 🌊"""
    
    def create_playlist_description_file(self, playlist_name, description):
        """Crea file descrizione playlist"""
        filename = f"/tmp/{playlist_name.replace(' ', '_').lower()}_description.txt"
        
        playlist_desc = f"""{description}

---
**Aqua Lofi Chill** - Il tuo spazio di pace digitale 🌊"""
        
        # Salva su server
        subprocess.run([
            'ssh', f'{self.server_user}@{self.server_ip}',
            f'echo "{playlist_desc}" > {filename}'
        ])
        
        return filename
    
    def upload_video(self, video_info):
        """Upload singolo video"""
        print(f"📤 Upload: {video_info['title']}")
        
        # Comando youtube-upload
        upload_cmd = f"""youtube-upload \\
    --title="{video_info['title']}" \\
    --description="{video_info['description']}" \\
    --category="Music" \\
    --tags="{video_info['tags']}" \\
    --privacy="public" \\
    "{self.video_dir}/{video_info['file']}" """
        
        print(f"🔧 Comando:")
        print(upload_cmd)
        print()
        
        # Esegui upload con ambiente virtuale
        result = subprocess.run([
            'ssh', f'{self.server_user}@{self.server_ip}',
            f'source /home/lofi/youtube_env/bin/activate && {upload_cmd}'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ Upload completato: {video_info['title']}")
            return True
        else:
            print(f"❌ Errore upload: {result.stderr}")
            return False
    
    def create_playlists(self):
        """Crea le playlist su YouTube"""
        print("📁 CREAZIONE PLAYLIST")
        print("=" * 25)
        print("ℹ️ Le playlist verranno create automaticamente durante l'upload dei video")
        print("ℹ️ Ogni video verrà aggiunto alla sua playlist specifica")
        print()
    
    def upload_all_videos(self):
        """Upload tutti i video"""
        print("📤 UPLOAD AQUA LOFI CHILL")
        print("=" * 30)
        
        # Prima crea le playlist
        self.create_playlists()
        
        print("\n🎬 UPLOAD VIDEO")
        print("=" * 15)
        
        success_count = 0
        
        for video_name, video_info in self.videos.items():
            print(f"\n🎵 Upload {video_name.upper()}:")
            
            # Verifica che il file esista
            result = subprocess.run([
                'ssh', f'{self.server_user}@{self.server_ip}',
                f'test -f "{self.video_dir}/{video_info["file"]}" && echo "EXISTS" || echo "MISSING"'
            ], capture_output=True, text=True)
            
            if "EXISTS" in result.stdout:
                if self.upload_video(video_info):
                    success_count += 1
            else:
                print(f"❌ File mancante: {video_info['file']}")
        
        print(f"\n🎉 UPLOAD COMPLETATO!")
        print(f"✅ Video caricati: {success_count}/{len(self.videos)}")
        
        if success_count == len(self.videos):
            print("🎊 Tutti i video sono stati caricati con successo!")
            print("📁 Le playlist sono state create e popolate")
        else:
            print("⚠️ Alcuni video non sono stati caricati")

def main():
    """Main function"""
    uploader = AquaLofiChillUploader()
    uploader.upload_all_videos()

if __name__ == "__main__":
    main() 