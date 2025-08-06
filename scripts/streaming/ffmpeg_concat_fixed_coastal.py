#!/usr/bin/env python3
"""
🎵 FFMPEG CONCAT FIXED - COASTAL EDITION
========================================

Streaming con concat corretto che include il nuovo minimix Coastal.

Author: AI Assistant
Date: 3 Agosto 2025
Version: 1.1 Coastal Edition
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
            },
            'coastal': {
                'audio': '/home/lofi/media/aqua/ffmpeg_direct/coastal/audio/Coastal_Luxury_ASMR_LOFI_Session.mp3',
                'video': '/home/lofi/media/aqua/ffmpeg_direct/coastal/video/Coastal_Luxury_ASMR_Session.mp4'
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
            print(f"  📁 {name}:")
            
            # Verifica audio
            if os.path.exists(files['audio']):
                size_mb = os.path.getsize(files['audio']) / (1024*1024)
                print(f"    ✅ Audio: {os.path.basename(files['audio'])} ({size_mb:.1f}MB)")
            else:
                print(f"    ❌ Audio mancante: {files['audio']}")
                return False
            
            # Verifica video
            if os.path.exists(files['video']):
                size_mb = os.path.getsize(files['video']) / (1024*1024)
                print(f"    ✅ Video: {os.path.basename(files['video'])} ({size_mb:.1f}MB)")
            else:
                print(f"    ❌ Video mancante: {files['video']}")
                return False
        
        print("✅ Tutti i file verificati!")
        return True
    
    def create_concat_file(self) -> str:
        """Crea file di concatenazione"""
        print("📝 Creazione file di concatenazione...")
        
        concat_content = []
        
        # Ordine: abyss → blue_bossa → meditative_tide → coastal → repeat
        order = ['abyss', 'blue_bossa', 'meditative_tide', 'coastal']
        
        for minimix_name in order:
            files = self.minimix_files[minimix_name]
            
            # File video (una volta, il loop sarà gestito da FFmpeg)
            concat_content.append(f"file '{files['video']}'")
            
            # File audio (una volta)
            concat_content.append(f"file '{files['audio']}'")
            concat_content.append("")  # Linea vuota per separare
        
        concat_text = "\n".join(concat_content)
        
        # Salva file concat
        concat_file = "/tmp/aqua_concat_fixed_coastal.txt"
        with open(concat_file, 'w') as f:
            f.write(concat_text)
        
        print(f"✅ File concat creato: {concat_file}")
        print(f"📊 Contenuto ({len(concat_content)} righe):")
        print(concat_text)
        
        return concat_file
    
    def start_streaming(self, concat_file: str):
        """Avvia streaming"""
        print("🚀 Avvio streaming...")
        
        # Comando FFmpeg ottimizzato per YouTube
        cmd = [
            'ffmpeg',
            '-re',  # Read input at native frame rate
            '-stream_loop', '-1',  # Loop infinito dell'input
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-b:v', '1500k',
            '-maxrate', '1500k',
            '-bufsize', '3000k',
            '-pix_fmt', 'yuv420p',
            '-r', '24',
            '-g', '48',
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-ac', '2',
            '-f', 'flv',
            self.full_rtmp
        ]
        
        print(f"🎯 Comando FFmpeg:")
        print(" ".join(cmd))
        
        try:
            # Avvia processo
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                bufsize=1
            )
            
            print(f"✅ Streaming avviato (PID: {self.ffmpeg_process.pid})")
            
            # Monitora output
            for line in self.ffmpeg_process.stdout:
                print(f"📡 {line.strip()}")
                
                # Controlla se il processo è ancora attivo
                if self.ffmpeg_process.poll() is not None:
                    break
            
        except KeyboardInterrupt:
            print("\n⚠️ Interruzione manuale...")
            self.stop_streaming()
        except Exception as e:
            print(f"❌ Errore durante lo streaming: {e}")
            self.stop_streaming()
    
    def stop_streaming(self):
        """Ferma streaming"""
        if self.ffmpeg_process:
            print(f"🛑 Fermando streaming (PID: {self.ffmpeg_process.pid})...")
            
            try:
                self.ffmpeg_process.terminate()
                self.ffmpeg_process.wait(timeout=10)
                print("✅ Streaming fermato")
            except subprocess.TimeoutExpired:
                print("⚠️ Timeout, forzando terminazione...")
                self.ffmpeg_process.kill()
            except Exception as e:
                print(f"❌ Errore nel fermare streaming: {e}")
    
    def run(self):
        """Esegue streaming completo"""
        print("🎵 FFMPEG CONCAT FIXED - COASTAL EDITION")
        print("=" * 50)
        
        # Verifica file
        if not self.verify_all_files():
            print("❌ Verifica file fallita!")
            return
        
        # Crea file concat
        concat_file = self.create_concat_file()
        
        # Setup signal handler
        def signal_handler(signum, frame):
            print(f"\n⚠️ Segnale {signum} ricevuto...")
            self.stop_streaming()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Avvia streaming
        self.start_streaming(concat_file)

def main():
    """Funzione principale"""
    streamer = ConcatFixedStreamer()
    streamer.run()

if __name__ == "__main__":
    main() 