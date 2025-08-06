#!/usr/bin/env python3
"""
🎵 TEST SINGLE AUDIO CONCAT
===========================

Test con un singolo file audio per verificare se il problema è nel concat.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Single Audio Test
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

class SingleAudioTest:
    """Test con singolo audio"""
    
    def __init__(self):
        # File singolo per test
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
        print("🔍 Verifica file singolo...")
        
        if not os.path.exists(self.audio_file):
            print(f"❌ Audio mancante: {self.audio_file}")
            return False
        
        if not os.path.exists(self.video_file):
            print(f"❌ Video mancante: {self.video_file}")
            return False
        
        print("✅ File verificati!")
        return True
    
    def start_streaming(self) -> bool:
        """Avvia streaming con singolo audio"""
        print("🚀 Avvio Streaming Singolo Audio...")
        
        if not self.verify_files():
            return False
        
        # Comando FFmpeg con singolo audio
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
            '-b:v', '6800k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'flv',
            self.full_rtmp
        ]
        
        print(f"🔧 Comando Singolo: {' '.join(cmd)}")
        
        try:
            self.ffmpeg_process = subprocess.Popen(cmd)
            print(f"✅ Streaming Singolo avviato! PID: {self.ffmpeg_process.pid}")
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
        
        print("📊 Monitoraggio Singolo...")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo terminato!")
                    break
                time.sleep(30)
                print(f"⏰ Streaming Singolo attivo - PID: {self.ffmpeg_process.pid}")
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎵 TEST SINGLE AUDIO CONCAT")
    print("=" * 30)
    
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    streamer = SingleAudioTest()
    
    if streamer.start_streaming():
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming singolo")
        sys.exit(1)

if __name__ == "__main__":
    main() 