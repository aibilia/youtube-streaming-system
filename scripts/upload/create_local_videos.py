#!/usr/bin/env python3
"""
🎬 CREATE LOCAL VIDEOS
======================

Script per creare file video completi (audio + video in loop) sul computer locale.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Local Video Creation
"""

import os
import subprocess
from datetime import datetime

class LocalVideoCreator:
    """Creatore di video locali"""
    
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.output_dir = "youtube_videos"
        
        # Crea la directory di output se non esiste
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        
        # Configurazione video
        self.videos = {
            'blue_bossa': {
                'audio_file': '/Users/andreafeo/Desktop/Songs/Aqua_Lofi_Chill/Blue Bossa/20250721/20250721_BlueBossa_Minimix/Blue_Bossa_Minimix_20250721_175819.mp3',
                'video_file': '/Users/andreafeo/Desktop/Videos/Aqua_Lofi_Chill/Blue_Bossa/20250722/Blue_Bossa_Guitar_On_The_Sand.mp4',
                'output_file': f'{self.output_dir}/Blue_Bossa_Session_1_{self.current_date}.mp4',
                'title': 'Blue Bossa Lofi Jazz Session - Study Music & Relaxation Focus',
                'description': self.get_blue_bossa_description(),
                'tags': 'lofi,studymusic,relaxation,focus,jazz,chill,ambient,meditation,productivity,calm,peaceful,instrumental,acoustic,guitar,beach,sunset,zen,workmusic,concentration,stressrelief'
            },
            'meditative_tide': {
                'audio_file': '/Users/andreafeo/Desktop/Songs/Aqua_Lofi_Chill/Meditative Tide/20250717/20250723_Meditative_Tide_Minimix/Meditative_Tide Minimix_20250723_113602.mp3',
                'video_file': '/Users/andreafeo/Desktop/Videos/Aqua_Lofi_Chill/Meditative_Tide/20250722/Meditative Tide_Kid_Underwater.mp4',
                'output_file': f'{self.output_dir}/Meditative_Tide_Session_1_{self.current_date}.mp4',
                'title': 'Meditative Tide Lofi Ocean Session - Meditation & Deep Focus Music',
                'description': self.get_meditative_tide_description(),
                'tags': 'lofi,meditation,focus,ocean,ambient,relaxation,studymusic,chill,peace,calm,zen,meditationmusic,productivity,nature,water,flow,tranquility,serenity,mindfulness,concentration'
            },
            'abyss_deep': {
                'audio_file': '/Users/andreafeo/Desktop/Songs/Aqua_Lofi_Chill/Abyss Deep/20250707/20250722_Abyss_Deep_Minimix/Abyss_Deep_Minimix_20250722_220340.mp3',
                'video_file': '/Users/andreafeo/Desktop/Videos/Aqua_Lofi_Chill/Abyss_Deep/20250722/Abyss Deep_Submarine.mp4',
                'output_file': f'{self.output_dir}/Abyss_Deep_Session_1_{self.current_date}.mp4',
                'title': 'Abyss Deep Lofi Ambient Session - Deep Focus & Contemplation Music',
                'description': self.get_abyss_deep_description(),
                'tags': 'lofi,deepfocus,ambient,meditation,relaxation,studymusic,chill,deep,ocean,peace,calm,zen,meditationmusic,productivity,nature,water,depth,tranquility,serenity,mindfulness,concentration,contemplation'
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
    
    def create_video(self, video_name, video_info):
        """Crea un singolo video"""
        print(f"🎬 Creazione video: {video_name.upper()}")
        
        audio_file = video_info['audio_file']
        video_file = video_info['video_file']
        output_file = video_info['output_file']
        
        # Verifica che i file esistano
        if not os.path.exists(audio_file):
            print(f"❌ File audio mancante: {audio_file}")
            return False
        
        if not os.path.exists(video_file):
            print(f"❌ File video mancante: {video_file}")
            return False
        
        print(f"📁 Audio: {audio_file}")
        print(f"🎥 Video: {video_file}")
        print(f"📤 Output: {output_file}")
        
        # Comando FFmpeg per creare il video
        # Il video viene messo in loop per coprire tutta la durata dell'audio
        cmd = [
            'ffmpeg',
            '-i', audio_file,  # Input audio
            '-stream_loop', '-1',  # Loop infinito per il video
            '-i', video_file,  # Input video
            '-c:v', 'libx264',  # Codec video
            '-c:a', 'aac',  # Codec audio
            '-shortest',  # Termina quando l'audio finisce
            '-pix_fmt', 'yuv420p',  # Formato pixel compatibile
            '-crf', '23',  # Qualità video
            '-preset', 'medium',  # Preset di encoding
            '-y',  # Sovrascrivi file esistenti
            output_file
        ]
        
        try:
            print("🔄 Encoding in corso...")
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Video creato: {output_file}")
                
                # Verifica la dimensione del file
                file_size = os.path.getsize(output_file) / (1024 * 1024)  # MB
                print(f"📊 Dimensione file: {file_size:.1f} MB")
                
                return True
            else:
                print(f"❌ Errore encoding: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Errore creazione video: {e}")
            return False
    
    def create_all_videos(self):
        """Crea tutti i video"""
        print("🎬 CREAZIONE VIDEO LOCALI")
        print("=" * 30)
        
        success_count = 0
        
        for video_name, video_info in self.videos.items():
            print(f"\n🎵 Creazione {video_name.upper()}:")
            
            if self.create_video(video_name, video_info):
                success_count += 1
                
                # Crea file di metadati
                self.create_metadata_file(video_name, video_info)
        
        print(f"\n🎉 CREAZIONE COMPLETATA!")
        print(f"✅ Video creati: {success_count}/{len(self.videos)}")
        
        if success_count == len(self.videos):
            print("🎊 Tutti i video sono stati creati con successo!")
            print(f"📁 I file si trovano nella directory: {self.output_dir}")
            print("\n📤 Prossimo passo: Upload su YouTube")
        else:
            print("⚠️ Alcuni video non sono stati creati")
    
    def create_metadata_file(self, video_name, video_info):
        """Crea file di metadati per YouTube"""
        metadata_file = f"{self.output_dir}/{video_name}_metadata.txt"
        
        metadata = f"""TITLE: {video_info['title']}

DESCRIPTION:
{video_info['description']}

TAGS: {video_info['tags']}

CATEGORY: Music
PRIVACY: Public
"""
        
        with open(metadata_file, 'w', encoding='utf-8') as f:
            f.write(metadata)
        
        print(f"📝 Metadati salvati: {metadata_file}")

def main():
    """Main function"""
    creator = LocalVideoCreator()
    creator.create_all_videos()

if __name__ == "__main__":
    main() 