#!/usr/bin/env python3
"""
🎵 TEST BLUE BOSSA AUDIO
========================

Test con file audio Blue Bossa per verificare se il problema è nel file audio.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Blue Bossa Test
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

class BlueBossaAudioTest:
    """Test audio con Blue Bossa"""
    
    def __init__(self):
        # File Blue Bossa
        self.audio_file = "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3"
        self.video_file = "/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4"
        
        # YouTube
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "ghfr-q9tg-42fs-xmv7-1fjy"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Processo
        self.ffmpeg_process = None
        
    def verify_files(self) -> bool:
        """Verifica file"""
        print("🔍 Verifica file Blue Bossa...")
        
        if not os.path.exists(self.audio_file):
            print(f"❌ Audio Blue Bossa mancante: {self.audio_file}")
            return False
        
        if not os.path.exists(self.video_file):
            print(f"❌ Video mancante: {self.video_file}")
            return False
        
        print("✅ File Blue Bossa verificati!")
        return True
    
    def start_streaming(self) -> bool:
        """Avvia streaming con Blue Bossa"""
        print("🚀 Avvio Streaming Blue Bossa...")
        
        if not self.verify_files():
            return False
        
        # Comando FFmpeg con Blue Bossa
        cmd = [
            'ffmpeg',
            '-re',
            '-stream_loop', '-1',
            '-i', self.video_file,
            '-stream_loop', '-1', 
            '-i', self.audio_file,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-b:v', '4000k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'flv',
            self.full_rtmp
        ]
        
        print(f"🔧 Comando Blue Bossa: {' '.join(cmd)}")
        
        try:
            self.ffmpeg_process = subprocess.Popen(cmd)
            print(f"✅ Streaming Blue Bossa avviato! PID: {self.ffmpeg_process.pid}")
            return True
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False
    
    def stop_streaming(self):
        """Ferma streaming"""
        if self.ffmpeg_process:
            print("🛑 Arresto streaming Blue Bossa...")
            self.ffmpeg_process.terminate()
            try:
                self.ffmpeg_process.wait(timeout=10)
                print("✅ Streaming Blue Bossa arrestato")
            except:
                self.ffmpeg_process.kill()
                print("✅ Streaming Blue Bossa forzatamente arrestato")
    
    def monitor_streaming(self):
        """Monitora streaming"""
        if not self.ffmpeg_process:
            print("❌ Nessun processo Blue Bossa attivo")
            return
        
        print("📊 Monitoraggio Blue Bossa...")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo Blue Bossa terminato!")
                    break
                time.sleep(30)
                print(f"⏰ Streaming Blue Bossa attivo - PID: {self.ffmpeg_process.pid}")
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎵 TEST BLUE BOSSA AUDIO")
    print("=" * 30)
    
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    streamer = BlueBossaAudioTest()
    
    if streamer.start_streaming():
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming Blue Bossa")
        sys.exit(1)

if __name__ == "__main__":
    main() 