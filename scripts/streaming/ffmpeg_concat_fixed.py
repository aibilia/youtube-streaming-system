#!/usr/bin/env python3
"""
🎵 FFMPEG CONCAT FIXED
======================

Streaming con concat corretto che funziona come il test singolo.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Concat Fixed
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

class ConcatFixedStreamer:
    """Streaming con concat corretto"""
    
    def __init__(self):
        # File minimix e video
        self.minimix_files = {
            'abyss': {
                'audio': '/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3',
                'video': '/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4'
            },
            'blue_bossa': {
                'audio': '/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3',
                'video': '/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/video/Blue_Bossa_Guitar_On_The_Sand.mp4'
            },
            'meditative_tide': {
                'audio': '/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3',
                'video': '/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/video/Meditative Tide_Kid_Underwater.mp4'
            }
        }
        
        # YouTube
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "ghfr-q9tg-42fs-xmv7-1fjy"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Processo
        self.ffmpeg_process = None
        
    def verify_all_files(self) -> bool:
        """Verifica tutti i file"""
        print("🔍 Verifica tutti i file...")
        
        for name, files in self.minimix_files.items():
            if not os.path.exists(files['audio']):
                print(f"❌ Audio {name} mancante: {files['audio']}")
                return False
            
            if not os.path.exists(files['video']):
                print(f"❌ Video {name} mancante: {files['video']}")
                return False
        
        print("✅ Tutti i file verificati!")
        return True
    
    def create_concat_file(self) -> str:
        """Crea file concat per audio"""
        concat_content = ""
        for name, files in self.minimix_files.items():
            concat_content += f"file '{files['audio']}'\n"
        
        concat_file = "/tmp/aqua_concat_fixed.txt"
        with open(concat_file, 'w') as f:
            f.write(concat_content)
        
        print(f"📝 File concat creato: {concat_file}")
        return concat_file
    
    def start_streaming(self) -> bool:
        """Avvia streaming con concat corretto"""
        print("🚀 Avvio Streaming Concat Corretto...")
        
        if not self.verify_all_files():
            return False
        
        concat_file = self.create_concat_file()
        
        # Comando FFmpeg con CONCAT CORRETTO
        # - Usa il primo video in loop per tutto
        # - Concatena tutti e 3 i minimix audio
        # - Stesso mapping del test singolo che funziona
        cmd = [
            'ffmpeg',
            '-re',
            '-stream_loop', '-1',
            '-i', self.minimix_files['abyss']['video'],  # Video loop infinito
            '-f', 'concat',
            '-safe', '0',
            '-stream_loop', '-1',
            '-i', concat_file,  # Audio concatenato
            '-map', '0:v:0',  # Video dal primo input
            '-map', '1:a:0',  # Audio dal concat (come nel test singolo)
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-b:v', '6800k',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-f', 'flv',
            self.full_rtmp
        ]
        
        print(f"🔧 Comando Concat Corretto: {' '.join(cmd)}")
        
        try:
            self.ffmpeg_process = subprocess.Popen(cmd)
            print(f"✅ Streaming Concat Corretto avviato! PID: {self.ffmpeg_process.pid}")
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
        
        print("📊 Monitoraggio Concat Corretto...")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo terminato!")
                    break
                time.sleep(30)
                print(f"⏰ Streaming Concat Corretto attivo - PID: {self.ffmpeg_process.pid}")
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎵 FFMPEG CONCAT FIXED")
    print("=" * 25)
    
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    streamer = ConcatFixedStreamer()
    
    if streamer.start_streaming():
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming")
        sys.exit(1)

if __name__ == "__main__":
    main() 