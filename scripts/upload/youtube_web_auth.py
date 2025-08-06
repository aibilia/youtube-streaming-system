#!/usr/bin/env python3
"""
🌐 YOUTUBE WEB AUTH
===================

Script per autenticazione YouTube API con server web locale.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Web Auth
"""

import os
import json
import subprocess
import threading
import time
import webbrowser
from datetime import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
import pickle
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

class AuthHandler(BaseHTTPRequestHandler):
    """Handler per gestire l'autenticazione OAuth"""
    
    def __init__(self, *args, auth_code_callback=None, **kwargs):
        self.auth_code_callback = auth_code_callback
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Gestisce le richieste GET"""
        if self.path.startswith('/oauth2callback'):
            # Estrai il codice di autorizzazione
            query_components = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            auth_code = query_components.get('code', [None])[0]
            
            if auth_code:
                # Chiama la callback con il codice
                if self.auth_code_callback:
                    self.auth_code_callback(auth_code)
                
                # Invia risposta di successo
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                success_html = """
                <html>
                <head><title>Autenticazione Completata</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #4CAF50;">✅ Autenticazione Completata!</h1>
                    <p>L'autenticazione con YouTube è stata completata con successo.</p>
                    <p>Puoi chiudere questa finestra e tornare al terminale.</p>
                    <div style="margin-top: 30px; padding: 20px; background-color: #f0f0f0; border-radius: 10px;">
                        <h3>🎬 Prossimi passi:</h3>
                        <p>I video verranno caricati automaticamente su YouTube.</p>
                    </div>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode())
            else:
                # Errore
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                error_html = """
                <html>
                <head><title>Errore di Autenticazione</title></head>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #f44336;">❌ Errore di Autenticazione</h1>
                    <p>Si è verificato un errore durante l'autenticazione.</p>
                    <p>Riprova più tardi.</p>
                </body>
                </html>
                """
                self.wfile.write(error_html.encode())
        else:
            # Pagina di default
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            default_html = """
            <html>
            <head><title>YouTube Auth Server</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1>🌐 Server di Autenticazione YouTube</h1>
                <p>Questo server gestisce l'autenticazione per l'upload dei video.</p>
            </body>
            </html>
            """
            self.wfile.write(default_html.encode())

class YouTubeWebAuth:
    """Autenticazione YouTube con server web locale"""
    
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
        
        self.auth_code = None
        self.server = None
    
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
    
    def auth_code_callback(self, auth_code):
        """Callback per ricevere il codice di autorizzazione"""
        self.auth_code = auth_code
        print(f"✅ Codice di autorizzazione ricevuto!")
    
    def start_auth_server(self):
        """Avvia il server di autenticazione"""
        print("🌐 Avvio server di autenticazione...")
        
        # Crea il server
        server_address = ('localhost', 8080)
        
        # Crea una classe handler personalizzata con la callback
        class CustomAuthHandler(AuthHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, auth_code_callback=self.auth_code_callback, **kwargs)
        
        self.server = HTTPServer(server_address, CustomAuthHandler)
        
        # Avvia il server in un thread separato
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        print("✅ Server avviato su http://localhost:8080")
    
    def stop_auth_server(self):
        """Ferma il server di autenticazione"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            print("🛑 Server fermato")
    
    def authenticate_youtube(self):
        """Autenticazione con YouTube API"""
        print("🔐 Autenticazione YouTube API...")
        
        # File per le credenziali
        credentials_file = "/root/.client_secrets.json"
        token_file = "/root/youtube_token.pickle"
        
        try:
            # Avvia il server di autenticazione
            self.start_auth_server()
            
            # Crea il flow di autenticazione
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, 
                self.SCOPES,
                redirect_uri='http://localhost:8080/oauth2callback'
            )
            
            # Genera l'URL di autorizzazione
            auth_url, _ = flow.authorization_url(prompt='consent')
            
            print(f"\n🌐 URL di autenticazione generato!")
            print(f"📋 Apri questo URL nel tuo browser:")
            print(f"\n{auth_url}")
            print(f"\n⏳ In attesa dell'autorizzazione...")
            
            # Aspetta che l'utente completi l'autenticazione
            while not self.auth_code:
                time.sleep(1)
            
            # Scambia il codice per le credenziali
            flow.fetch_token(code=self.auth_code)
            credentials = flow.credentials
            
            # Salva le credenziali
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
            
            print("✅ Autenticazione completata!")
            print("🔑 Credenziali salvate per uso futuro")
            
            # Ferma il server
            self.stop_auth_server()
            
            return credentials
            
        except Exception as e:
            print(f"❌ Errore autenticazione: {e}")
            self.stop_auth_server()
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
                print("❌ Credenziali non trovate. Eseguo l'autenticazione...")
                credentials = self.authenticate_youtube()
                if not credentials:
                    print("❌ Autenticazione fallita")
                    return
            else:
                # Carica le credenziali esistenti
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
                        print("❌ Credenziali scadute. Eseguo nuova autenticazione...")
                        credentials = self.authenticate_youtube()
                        if not credentials:
                            print("❌ Autenticazione fallita")
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
        finally:
            # Assicurati che il server sia fermato
            self.stop_auth_server()

def main():
    """Main function"""
    auth = YouTubeWebAuth()
    auth.upload_all_videos()

if __name__ == "__main__":
    main() 