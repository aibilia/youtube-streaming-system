#!/usr/bin/env python3
"""
🔐 YOUTUBE AUTH HELPER
======================

Script per generare URL di autenticazione YouTube API.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Auth Helper
"""

import os
import json
import subprocess
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle

class YouTubeAuthHelper:
    """Helper per autenticazione YouTube API"""
    
    def __init__(self):
        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.video_dir = "/home/lofi/media/aqua/youtube_videos"
        self.server_ip = "159.89.106.38"
        self.server_user = "root"
        
        # Scopes per YouTube API
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        
        # Configurazione video
        self.videos = {
            'blue_bossa': {
                'file': f'Blue_Bossa_Session_1_{self.current_date}.mp4',
                'title': 'Blue Bossa Lofi Jazz Session - Study Music & Relaxation Focus',
                'description': self.get_blue_bossa_description(),
                'tags': ['lofi', 'studymusic', 'relaxation', 'focus', 'jazz', 'chill', 'ambient', 'meditation', 'productivity', 'calm', 'peaceful', 'instrumental', 'acoustic', 'guitar', 'beach', 'sunset', 'zen', 'workmusic', 'concentration', 'stressrelief'],
                'category_id': '10',  # Music
                'playlist': 'Blue Bossa Collection - Jazz Lofi Sessions'
            },
            'meditative_tide': {
                'file': f'Meditative_Tide_Session_1_{self.current_date}.mp4',
                'title': 'Meditative Tide Lofi Ocean Session - Meditation & Deep Focus Music',
                'description': self.get_meditative_tide_description(),
                'tags': ['lofi', 'meditation', 'focus', 'ocean', 'ambient', 'relaxation', 'studymusic', 'chill', 'peace', 'calm', 'zen', 'meditationmusic', 'productivity', 'nature', 'water', 'flow', 'tranquility', 'serenity', 'mindfulness', 'concentration'],
                'category_id': '10',  # Music
                'playlist': 'Meditative Tide Collection - Ocean Lofi Sessions'
            },
            'abyss_deep': {
                'file': f'Abyss_Deep_Session_1_{self.current_date}.mp4',
                'title': 'Abyss Deep Lofi Ambient Session - Deep Focus & Contemplation Music',
                'description': self.get_abyss_deep_description(),
                'tags': ['lofi', 'deepfocus', 'ambient', 'meditation', 'relaxation', 'studymusic', 'chill', 'deep', 'ocean', 'peace', 'calm', 'zen', 'meditationmusic', 'productivity', 'nature', 'water', 'depth', 'tranquility', 'serenity', 'mindfulness', 'concentration', 'contemplation'],
                'category_id': '10',  # Music
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
    
    def generate_auth_url(self):
        """Genera URL di autenticazione"""
        print("🔐 Generazione URL di autenticazione...")
        
        # File per le credenziali
        credentials_file = "/root/.client_secrets.json"
        
        try:
            # Crea il flow di autenticazione con redirect URI
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, 
                self.SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Out-of-band redirect
            )
            
            # Genera l'URL di autorizzazione
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print(f"\n🌐 URL di autenticazione generato!")
            print(f"📋 Copia questo URL e aprilo nel tuo browser:")
            print(f"\n{auth_url}")
            print(f"\n📝 Dopo l'autorizzazione, copia il codice di autorizzazione")
            print(f"🔗 Poi esegui: python3 youtube_auth_helper.py <codice>")
            
            return auth_url
            
        except Exception as e:
            print(f"❌ Errore generazione URL: {e}")
            return None
    
    def complete_auth_with_code(self, auth_code):
        """Completa l'autenticazione con il codice"""
        print("🔐 Completamento autenticazione...")
        
        # File per le credenziali
        credentials_file = "/root/.client_secrets.json"
        token_file = "/root/youtube_token.pickle"
        
        try:
            # Crea il flow di autenticazione con redirect URI
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, 
                self.SCOPES,
                redirect_uri='urn:ietf:wg:oauth:2.0:oob'  # Out-of-band redirect
            )
            
            # Scambia il codice per le credenziali
            flow.fetch_token(code=auth_code)
            credentials = flow.credentials
            
            # Salva le credenziali
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
            
            print("✅ Autenticazione completata!")
            print("🔑 Credenziali salvate per uso futuro")
            
            return credentials
            
        except Exception as e:
            print(f"❌ Errore completamento autenticazione: {e}")
            return None
    
    def upload_video(self, youtube, video_info):
        """Upload singolo video"""
        print(f"📤 Upload: {video_info['title']}")
        
        # Prepara il body della richiesta
        body = {
            'snippet': {
                'title': video_info['title'],
                'description': video_info['description'],
                'tags': video_info['tags'],
                'categoryId': video_info['category_id']
            },
            'status': {
                'privacyStatus': 'public',
                'selfDeclaredMadeForKids': False
            }
        }
        
        # Crea il media upload
        media = MediaFileUpload(
            f"{self.video_dir}/{video_info['file']}", 
            chunksize=1024*1024, 
            resumable=True
        )
        
        # Esegui l'upload
        try:
            request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=media
            )
            
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    print(f"Uploaded {int(status.progress() * 100)}%")
            
            print(f"✅ Upload completato: {video_info['title']}")
            print(f"🎬 Video ID: {response['id']}")
            return response['id']
            
        except HttpError as e:
            print(f"❌ Errore upload: {e}")
            return None
    
    def create_playlist(self, youtube, playlist_name, description):
        """Crea una playlist"""
        print(f"📁 Creazione playlist: {playlist_name}")
        
        body = {
            'snippet': {
                'title': playlist_name,
                'description': description
            },
            'status': {
                'privacyStatus': 'public'
            }
        }
        
        try:
            request = youtube.playlists().insert(
                part='snippet,status',
                body=body
            )
            response = request.execute()
            print(f"✅ Playlist creata: {playlist_name}")
            return response['id']
        except HttpError as e:
            print(f"❌ Errore creazione playlist: {e}")
            return None
    
    def add_video_to_playlist(self, youtube, playlist_id, video_id):
        """Aggiunge un video a una playlist"""
        body = {
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
        
        try:
            request = youtube.playlistItems().insert(
                part='snippet',
                body=body
            )
            response = request.execute()
            print(f"✅ Video aggiunto alla playlist")
            return True
        except HttpError as e:
            print(f"❌ Errore aggiunta video alla playlist: {e}")
            return False
    
    def upload_all_videos(self):
        """Upload tutti i video"""
        print("📤 UPLOAD AQUA LOFI CHILL - YouTube API")
        print("=" * 40)
        
        try:
            # File per le credenziali
            token_file = "/root/youtube_token.pickle"
            
            if not os.path.exists(token_file):
                print("❌ Credenziali non trovate. Esegui prima l'autenticazione.")
                return
            
            # Carica le credenziali
            with open(token_file, 'rb') as token:
                credentials = pickle.load(token)
            
            # Verifica se le credenziali sono valide
            if not credentials.valid:
                if credentials.expired and credentials.refresh_token:
                    credentials.refresh(Request())
                    # Salva le credenziali aggiornate
                    with open(token_file, 'wb') as token:
                        pickle.dump(credentials, token)
                else:
                    print("❌ Credenziali scadute. Esegui nuovamente l'autenticazione.")
                    return
            
            # Crea il client YouTube
            youtube = build('youtube', 'v3', credentials=credentials)
            
            # Dizionario per le playlist
            playlists = {}
            
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
                    # Upload video
                    video_id = self.upload_video(youtube, video_info)
                    
                    if video_id:
                        success_count += 1
                        
                        # Crea playlist se non esiste
                        playlist_name = video_info['playlist']
                        if playlist_name not in playlists:
                            playlist_description = f"Collection of {video_name.replace('_', ' ').title()} sessions"
                            playlist_id = self.create_playlist(youtube, playlist_name, playlist_description)
                            if playlist_id:
                                playlists[playlist_name] = playlist_id
                        
                        # Aggiungi video alla playlist
                        if playlist_name in playlists:
                            self.add_video_to_playlist(youtube, playlists[playlist_name], video_id)
                else:
                    print(f"❌ File mancante: {video_info['file']}")
            
            print(f"\n🎉 UPLOAD COMPLETATO!")
            print(f"✅ Video caricati: {success_count}/{len(self.videos)}")
            
            if success_count == len(self.videos):
                print("🎊 Tutti i video sono stati caricati con successo!")
                print("📁 Le playlist sono state create e popolate")
            else:
                print("⚠️ Alcuni video non sono stati caricati")
                
        except Exception as e:
            print(f"❌ Errore generale: {e}")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1:
        # Modalità completamento autenticazione
        auth_code = sys.argv[1]
        helper = YouTubeAuthHelper()
        helper.complete_auth_with_code(auth_code)
    else:
        # Modalità generazione URL
        helper = YouTubeAuthHelper()
        helper.generate_auth_url()

if __name__ == "__main__":
    main() 