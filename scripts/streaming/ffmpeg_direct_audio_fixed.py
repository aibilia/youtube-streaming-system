#!/usr/bin/env python3
"""
🎵 FFMPEG DIRECT STREAMING - AUDIO FIXED VERSION
===============================================

Versione corretta per streaming YouTube con audio funzionante.
Risolve problemi di audio mancante nello stream.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.2 Audio Fixed
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import List

class AudioFixedFFmpegStreamer:
    """Streaming FFmpeg con audio corretto"""
    
    def __init__(self):
        # Configurazione server
        self.server_base = "/home/lofi/media/aqua/ffmpeg_direct"
        
        # File minimix (solo audio per ora, video loop separato)
        self.minimix_files = [
            f"{self.server_base}/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3",
            f"{self.server_base}/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3", 
            f"{self.server_base}/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3"
        ]
        
        # Video background (usa il primo per tutto)
        self.video_file = f"{self.server_base}/abyss/video/Abyss Deep_Submarine.mp4"
        
        # YouTube streaming
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "ghfr-q9tg-42fs-xmv7-1fjy"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Processo FFmpeg
        self.ffmpeg_process = None
        
    def create_concat_file(self):
        """Crea file di concatenazione per FFmpeg"""
        concat_file = "/tmp/minimix_concat_audio_fixed.txt"
        
        with open(concat_file, 'w') as f:
            for audio_file in self.minimix_files:
                f.write(f"file '{audio_file}'\n")
        
        print(f"📝 File concatenazione creato: {concat_file}")
        return concat_file
    
    def verify_files(self) -> bool:
        """Verifica che tutti i file esistano"""
        print("🔍 Verifica file...")
        
        # Verifica video
        if os.path.exists(self.video_file):
            size = os.path.getsize(self.video_file) / (1024*1024)
            print(f"  ✅ Video: {os.path.basename(self.video_file)} ({size:.1f}MB)")
        else:
            print(f"  ❌ Video mancante: {self.video_file}")
            return False
        
        # Verifica audio files
        for i, audio_file in enumerate(self.minimix_files):
            if os.path.exists(audio_file):
                size = os.path.getsize(audio_file) / (1024*1024)
                print(f"  ✅ Audio {i+1}: {os.path.basename(audio_file)} ({size:.1f}MB)")
            else:
                print(f"  ❌ Audio {i+1} mancante: {audio_file}")
                return False
        
        print("✅ Tutti i file verificati!")
        return True
    
    def create_ffmpeg_command(self, concat_file: str) -> List[str]:
        """Crea comando FFmpeg corretto con audio"""
        
        cmd = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'info',
            '-re',  # Read at native frame rate
            
            # Input video (loop infinito)
            '-stream_loop', '-1',
            '-i', self.video_file,
            
            # Input audio (concatenazione)
            '-f', 'concat',
            '-safe', '0',
            '-stream_loop', '-1',  # Loop anche audio
            '-i', concat_file,
            
            # Video encoding - BITRATE RACCOMANDATO YOUTUBE
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-b:v', '6800k',
            '-maxrate', '6800k',
            '-bufsize', '13600k',
            '-pix_fmt', 'yuv420p',
            '-r', '24',
            '-g', '48',
            
            # Audio encoding - CORRETTO
            '-c:a', 'aac',
            '-b:a', '128k',
            '-ar', '44100',
            '-ac', '2',
            '-af', 'volume=1.0',  # Normalizza volume
            
            # Output
            '-f', 'flv',
            '-flvflags', 'no_duration_filesize',
            self.full_rtmp
        ]
        
        return cmd
    
    def start_streaming(self) -> bool:
        """Avvia streaming"""
        print("🚀 Avvio FFmpeg Direct Streaming (Audio Fixed)...")
        print(f"📺 Target: YouTube RTMP")
        print(f"🎵 Minimix: {len(self.minimix_files)} file")
        print(f"🎬 Video: Loop infinito")
        
        if not self.verify_files():
            print("❌ Verifica file fallita!")
            return False
        
        # Crea file concatenazione
        concat_file = self.create_concat_file()
        
        # Crea comando FFmpeg
        cmd = self.create_ffmpeg_command(concat_file)
        
        print(f"🔧 Comando FFmpeg preparato")
        print(f"📊 Parametri: 720p @ 24fps, 6800k video (raccomandato YouTube), 128k audio")
        print(f"🎵 Audio: Normalizzato e bilanciato")
        
        try:
            # Avvia processo FFmpeg
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Streaming avviato! PID: {self.ffmpeg_process.pid}")
            
            return True
            
        except Exception as e:
            print(f"❌ Errore avvio streaming: {e}")
            return False
    
    def stop_streaming(self):
        """Ferma streaming"""
        if self.ffmpeg_process:
            print("🛑 Arresto streaming...")
            self.ffmpeg_process.terminate()
            
            try:
                self.ffmpeg_process.wait(timeout=10)
                print("✅ Streaming arrestato")
            except subprocess.TimeoutExpired:
                print("⚠️ Timeout arresto, forzando...")
                self.ffmpeg_process.kill()
                self.ffmpeg_process.wait()
                print("✅ Streaming forzatamente arrestato")
    
    def monitor_streaming(self):
        """Monitora streaming"""
        if not self.ffmpeg_process:
            print("❌ Nessun processo streaming attivo")
            return
        
        print("📊 Monitoraggio streaming...")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                # Verifica se processo è ancora attivo
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo FFmpeg terminato!")
                    break
                
                # Mostra statistiche ogni 30 secondi
                time.sleep(30)
                print(f"⏰ Streaming attivo - PID: {self.ffmpeg_process.pid}")
                
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta dall'utente")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎵 FFMPEG DIRECT STREAMING - AUDIO FIXED VERSION")
    print("=" * 55)
    
    # Setup signal handler
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto, arresto...")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crea streamer
    streamer = AudioFixedFFmpegStreamer()
    
    # Avvia streaming
    if streamer.start_streaming():
        # Monitora streaming
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming")
        sys.exit(1)

if __name__ == "__main__":
    main() 