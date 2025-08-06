#!/usr/bin/env python3
"""
📤 UPLOAD TO YOUTUBE LOCAL
==========================

Script per uploadare video su YouTube dal computer locale.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Local Upload
"""

import os
import subprocess
from datetime import datetime

class YouTubeLocalUploader:
    """Uploader YouTube locale"""
    
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.video_dir = "youtube_videos"
        
        # Configurazione video
        self.videos = {
            'blue_bossa': {
                'file': f'{self.video_dir}/Blue_Bossa_Session_1_{self.current_date}.mp4',
                'title': 'Blue Bossa Lofi Jazz Session - Study Music & Relaxation Focus',
                'description': self.get_blue_bossa_description(),
                'tags': 'lofi,studymusic,relaxation,focus,jazz,chill,ambient,meditation,productivity,calm,peaceful,instrumental,acoustic,guitar,beach,sunset,zen,workmusic,concentration,stressrelief',
                'playlist': 'Blue Bossa Collection - Jazz Lofi Sessions'
            },
            'meditative_tide': {
                'file': f'{self.video_dir}/Meditative_Tide_Session_1_{self.current_date}.mp4',
                'title': 'Meditative Tide Lofi Ocean Session - Meditation & Deep Focus Music',
                'description': self.get_meditative_tide_description(),
                'tags': 'lofi,meditation,focus,ocean,ambient,relaxation,studymusic,chill,peace,calm,zen,meditationmusic,productivity,nature,water,flow,tranquility,serenity,mindfulness,concentration',
                'playlist': 'Meditative Tide Collection - Ocean Lofi Sessions'
            },
            'abyss_deep': {
                'file': f'{self.video_dir}/Abyss_Deep_Session_1_{self.current_date}.mp4',
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
    
    def upload_video(self, video_name, video_info):
        """Upload singolo video"""
        print(f"📤 Upload: {video_info['title']}")
        
        # Verifica che il file esista
        if not os.path.exists(video_info['file']):
            print(f"❌ File mancante: {video_info['file']}")
            return False
        
        # Comando youtube-upload
        upload_cmd = f"""youtube-upload \\
    --title="{video_info['title']}" \\
    --description="{video_info['description']}" \\
    --category="Music" \\
    --tags="{video_info['tags']}" \\
    --privacy="public" \\
    "{video_info['file']}" """
        
        print("🔄 Upload in corso...")
        print(f"📁 File: {video_info['file']}")
        
        try:
            # Esegui l'upload
            result = subprocess.run(upload_cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Upload completato: {video_info['title']}")
                print(f"🔗 Output: {result.stdout}")
                return True
            else:
                print(f"❌ Errore upload: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False
    
    def upload_all_videos(self):
        """Upload tutti i video"""
        print("📤 UPLOAD AQUA LOFI CHILL - YouTube")
        print("=" * 35)
        
        success_count = 0
        
        for video_name, video_info in self.videos.items():
            print(f"\n🎵 Upload {video_name.upper()}:")
            
            if self.upload_video(video_name, video_info):
                success_count += 1
        
        print(f"\n🎉 UPLOAD COMPLETATO!")
        print(f"✅ Video caricati: {success_count}/{len(self.videos)}")
        
        if success_count == len(self.videos):
            print("🎊 Tutti i video sono stati caricati con successo!")
            print("📁 Le playlist verranno create automaticamente")
        else:
            print("⚠️ Alcuni video non sono stati caricati")
    
    def check_video_files(self):
        """Verifica che i file video esistano"""
        print("🔍 VERIFICA FILE VIDEO")
        print("=" * 20)
        
        missing_files = []
        
        for video_name, video_info in self.videos.items():
            if os.path.exists(video_info['file']):
                file_size = os.path.getsize(video_info['file']) / (1024 * 1024)  # MB
                print(f"✅ {video_name}: {video_info['file']} ({file_size:.1f} MB)")
            else:
                print(f"❌ {video_name}: {video_info['file']} - MANCANTE")
                missing_files.append(video_name)
        
        if missing_files:
            print(f"\n⚠️ File mancanti: {', '.join(missing_files)}")
            print("🔄 Esegui prima: python3 scripts/create_local_videos.py")
            return False
        else:
            print(f"\n✅ Tutti i file sono pronti per l'upload!")
            return True

def main():
    """Main function"""
    uploader = YouTubeLocalUploader()
    
    # Verifica prima i file
    if uploader.check_video_files():
        # Chiedi conferma prima dell'upload
        print("\n📤 Vuoi procedere con l'upload su YouTube? (y/n)")
        response = input().lower().strip()
        
        if response in ['y', 'yes', 'sì', 'si']:
            uploader.upload_all_videos()
        else:
            print("❌ Upload annullato")
    else:
        print("❌ Impossibile procedere con l'upload")

if __name__ == "__main__":
    main() 