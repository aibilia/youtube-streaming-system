#!/usr/bin/env python3
# Playlist Manager Unificato per OBS
import time
import subprocess
from pathlib import Path

PLAYLIST_FILE = "/home/lofi/media/aqua/playlists/unified_playlist.txt"
VIDEO_FILE = "/home/lofi/media/aqua/video/background.mp4"

def get_playlist_files():
    """Ottiene la lista dei file audio dalla playlist"""
    try:
        with open(PLAYLIST_FILE, 'r') as f:
            files = [line.strip() for line in f.readlines() if line.strip()]
        return files
    except Exception as e:
        print(f"❌ Errore lettura playlist: {e}")
        return []

def play_unified_playlist():
    """Riproduce la playlist unificata in loop infinito"""
    print("🎵 Avvio playlist unificata in loop...")
    
    playlist_files = get_playlist_files()
    if not playlist_files:
        print("❌ Nessun file nella playlist!")
        return
    
    print(f"📋 Playlist caricata: {len(playlist_files)} file")
    print(f"🎥 Video background: {VIDEO_FILE}")
    print("🔄 Modalità: Loop infinito")
    print("⏹️ Premi Ctrl+C per fermare")
    
    current_index = 0
    
    try:
        while True:
            # File audio corrente
            current_file = playlist_files[current_index]
            print(f"\n🎵 Riproducendo ({current_index + 1}/{len(playlist_files)}): {Path(current_file).name}")
            
            # Qui andrà l'integrazione con OBS per cambiare audio source
            # Per ora simula durata brano (3 minuti)
            time.sleep(180)
            
            # Prossimo file
            current_index = (current_index + 1) % len(playlist_files)
            
            # Se torniamo all'inizio
            if current_index == 0:
                print("🔄 Playlist completata, ricomincio da capo...")
                
    except KeyboardInterrupt:
        print("\n⏹️ Playlist fermata dall'utente")

if __name__ == "__main__":
    play_unified_playlist()
