#!/usr/bin/env python3
"""
🎵 FFMPEG AUDIO FIXED FINAL
===========================

Script finale con fix per specificare esplicitamente lo stream audio corretto.
Il problema era che FFmpeg usava l'audio del video invece del file audio MP3.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Audio Fixed Final
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

class AudioFixedFinalStreamer:
    """Streaming con audio corretto"""
    
    def __init__(self):
        # File
        self.audio_file = "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
        self.video_file = "/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4"
        
        # YouTube
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "ghfr-q9tg-42fs-xmv7-1fjy"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Processo
        self.ffmpeg_process = None
        
    def verify_files(self) -> bool:
        """Verifica file"""
        print("🔍 Verifica file...")
        
        if not os.path.exists(self.audio_file):
            print(f"❌ Audio mancante: {self.audio_file}")
            return False
        
        if not os.path.exists(self.video_file):
            print(f"❌ Video mancante: {self.video_file}")
            return False
        
        print("✅ File verificati!")
        return True
    
    def start_streaming(self) -> bool:
        """Avvia streaming con audio corretto"""
        print("🚀 Avvio Streaming Audio Corretto...")
        
        if not self.verify_files():
            return False
        
        # Comando FFmpeg con FIX AUDIO
        # -map 0:v:0 = usa solo video dal primo input (video)
        # -map 1:a:0 = usa solo audio dal secondo input (audio MP3)
        cmd = [
            'ffmpeg',
            '-re',
            '-stream_loop', '-1',
            '-i', self.video_file,
            '-stream_loop', '-1', 
            '-i', self.audio_file,
            '-map', '0:v:0',  # Solo video dal video
            '-map', '1:a:0',  # Solo audio dal MP3
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-b:v', '4000k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'flv',
            self.full_rtmp
        ]
        
        print(f"🔧 Comando Audio Corretto: {' '.join(cmd)}")
        
        try:
            self.ffmpeg_process = subprocess.Popen(cmd)
            print(f"✅ Streaming Audio Corretto avviato! PID: {self.ffmpeg_process.pid}")
            return True
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False
    
    def stop_streaming(self):
        """Ferma streaming"""
        if self.ffmpeg_process:
            print("🛑 Arresto streaming...")
            self.ffmpeg_process.terminate()
            try:
                self.ffmpeg_process.wait(timeout=10)
                print("✅ Streaming arrestato")
            except:
                self.ffmpeg_process.kill()
                print("✅ Streaming forzatamente arrestato")
    
    def monitor_streaming(self):
        """Monitora streaming"""
        if not self.ffmpeg_process:
            print("❌ Nessun processo attivo")
            return
        
        print("📊 Monitoraggio...")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo terminato!")
                    break
                time.sleep(30)
                print(f"⏰ Streaming attivo - PID: {self.ffmpeg_process.pid}")
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎵 FFMPEG AUDIO FIXED FINAL")
    print("=" * 35)
    
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    streamer = AudioFixedFinalStreamer()
    
    if streamer.start_streaming():
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming")
        sys.exit(1)

if __name__ == "__main__":
    main() 