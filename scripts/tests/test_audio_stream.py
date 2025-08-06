#!/usr/bin/env python3
"""
🎵 TEST AUDIO STREAMING
=======================

Script di test per verificare se l'audio viene trasmesso correttamente.
Usa solo il primo file audio per test semplificato.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Test Audio
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import List

class AudioTestStreamer:
    """Test streaming audio"""
    
    def __init__(self):
        # File di test (solo primo audio)
        self.audio_file = "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
        self.video_file = "/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4"
        
        # YouTube streaming
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "ghfr-q9tg-42fs-xmv7-1fjy"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Processo FFmpeg
        self.ffmpeg_process = None
        
    def verify_files(self) -> bool:
        """Verifica che i file esistano"""
        print("🔍 Verifica file di test...")
        
        if os.path.exists(self.audio_file):
            size = os.path.getsize(self.audio_file) / (1024*1024)
            print(f"  ✅ Audio: {os.path.basename(self.audio_file)} ({size:.1f}MB)")
        else:
            print(f"  ❌ Audio mancante: {self.audio_file}")
            return False
        
        if os.path.exists(self.video_file):
            size = os.path.getsize(self.video_file) / (1024*1024)
            print(f"  ✅ Video: {os.path.basename(self.video_file)} ({size:.1f}MB)")
        else:
            print(f"  ❌ Video mancante: {self.video_file}")
            return False
        
        print("✅ File di test verificati!")
        return True
    
    def create_simple_ffmpeg_command(self) -> List[str]:
        """Crea comando FFmpeg semplice per test audio"""
        
        cmd = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'info',
            '-re',  # Read at native frame rate
            
            # Input video (loop infinito)
            '-stream_loop', '-1',
            '-i', self.video_file,
            
            # Input audio (solo primo file)
            '-stream_loop', '-1',
            '-i', self.audio_file,
            
            # Video encoding
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-b:v', '6800k',
            '-maxrate', '6800k',
            '-bufsize', '13600k',
            '-pix_fmt', 'yuv420p',
            '-r', '24',
            '-g', '48',
            
            # Audio encoding - SEMPLIFICATO
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-ac', '2',
            
            # Output
            '-f', 'flv',
            '-flvflags', 'no_duration_filesize',
            self.full_rtmp
        ]
        
        return cmd
    
    def start_test_streaming(self) -> bool:
        """Avvia test streaming"""
        print("🎵 Avvio Test Audio Streaming...")
        print(f"📺 Target: YouTube RTMP")
        print(f"🎵 Audio: Solo Abyss Deep (test)")
        print(f"🎬 Video: Loop infinito")
        
        if not self.verify_files():
            print("❌ Verifica file fallita!")
            return False
        
        # Crea comando FFmpeg
        cmd = self.create_simple_ffmpeg_command()
        
        print(f"🔧 Comando FFmpeg test preparato")
        print(f"📊 Parametri: 720p @ 24fps, 6800k video, 128k audio")
        print(f"🎵 Audio: Test semplificato senza concatenazione")
        
        try:
            # Avvia processo FFmpeg
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Test streaming avviato! PID: {self.ffmpeg_process.pid}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore avvio test streaming: {e}")
            return False
    
    def stop_streaming(self):
        """Ferma streaming"""
        if self.ffmpeg_process:
            print("🛑 Arresto test streaming...")
            self.ffmpeg_process.terminate()
            
            try:
                self.ffmpeg_process.wait(timeout=10)
                print("✅ Test streaming arrestato")
            except subprocess.TimeoutExpired:
                print("⚠️ Timeout arresto, forzando...")
                self.ffmpeg_process.kill()
                self.ffmpeg_process.wait()
                print("✅ Test streaming forzatamente arrestato")
    
    def monitor_streaming(self):
        """Monitora streaming"""
        if not self.ffmpeg_process:
            print("❌ Nessun processo test streaming attivo")
            return
        
        print("📊 Monitoraggio test streaming...")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                # Verifica se processo è ancora attivo
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo FFmpeg test terminato!")
                    break
                
                # Mostra statistiche ogni 30 secondi
                time.sleep(30)
                print(f"⏰ Test streaming attivo - PID: {self.ffmpeg_process.pid}")
                
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta dall'utente")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎵 TEST AUDIO STREAMING")
    print("=" * 30)
    
    # Setup signal handler
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto, arresto...")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crea streamer
    streamer = AudioTestStreamer()
    
    # Avvia test streaming
    if streamer.start_test_streaming():
        # Monitora streaming
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare test streaming")
        sys.exit(1)

if __name__ == "__main__":
    main() 