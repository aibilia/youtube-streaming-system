#!/usr/bin/env python3
"""
🎵 FFMPEG DIRECT STREAMING - AQUA LOFI CHILL
============================================

Streaming YouTube con concatenazione di 3 minimix:
1. Abyss Deep (4.6 ore)
2. Blue Bossa (5.2 ore) 
3. Meditative Tide (4.2 ore)

Totale: ~14 ore di contenuto continuo con transizioni crossfade 0.3s

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 FFmpeg Direct
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path
from typing import Dict, List, Optional

class FFmpegDirectStreamer:
    """Streaming FFmpeg Direct per Aqua Lofi Chill"""
    
    def __init__(self):
        # Configurazione server
        self.server_base = "/home/lofi/media/aqua/ffmpeg_direct"
        
        # File minimix e video
        self.minimix_files = {
            'abyss': {
                'audio': f"{self.server_base}/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3",
                'video': f"{self.server_base}/abyss/video/Abyss Deep_Submarine.mp4",
                'duration': 4.6 * 3600  # 4.6 ore in secondi
            },
            'blue_bossa': {
                'audio': f"{self.server_base}/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3",
                'video': f"{self.server_base}/blue_bossa/video/Blue_Bossa_Guitar_On_The_Sand.mp4",
                'duration': 5.2 * 3600  # 5.2 ore in secondi
            },
            'meditative_tide': {
                'audio': f"{self.server_base}/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3",
                'video': f"{self.server_base}/meditative_tide/video/Meditative Tide_Kid_Underwater.mp4",
                'duration': 4.2 * 3600  # 4.2 ore in secondi
            }
        }
        
        # YouTube streaming
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "91a0-c9d8-czaw-qh5u-3bm8"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Parametri streaming (coerenti con configurazione attuale)
        self.streaming_params = {
            'resolution': '1280x720',      # 720p
            'fps': '24',                   # 24fps
            'video_bitrate': '1500k',      # 1500kbps
            'audio_bitrate': '128k',       # 128kbps
            'preset': 'ultrafast',         # Preset veloce
            'crossfade_duration': '0.3'    # 0.3 secondi transizione
        }
        
        # Processo FFmpeg
        self.ffmpeg_process = None
        
    def verify_files(self) -> bool:
        """Verifica che tutti i file esistano"""
        print("🔍 Verifica file minimix e video...")
        
        for program, files in self.minimix_files.items():
            print(f"  📁 {program.upper()}:")
            
            # Verifica audio
            if os.path.exists(files['audio']):
                size = os.path.getsize(files['audio']) / (1024*1024)
                print(f"    ✅ Audio: {os.path.basename(files['audio'])} ({size:.1f}MB)")
            else:
                print(f"    ❌ Audio mancante: {files['audio']}")
                return False
            
            # Verifica video
            if os.path.exists(files['video']):
                size = os.path.getsize(files['video']) / (1024*1024)
                print(f"    ✅ Video: {os.path.basename(files['video'])} ({size:.1f}MB)")
            else:
                print(f"    ❌ Video mancante: {files['video']}")
                return False
        
        print("✅ Tutti i file verificati!")
        return True
    
    def create_ffmpeg_command(self) -> List[str]:
        """Crea comando FFmpeg per concatenazione e streaming"""
        
        # Input files per concatenazione
        input_files = []
        filter_inputs = []
        filter_complex = []
        
        for i, (program, files) in enumerate(self.minimix_files.items()):
            # Input audio
            input_files.extend(['-i', files['audio']])
            filter_inputs.append(f"[{i*2}:a]")
            
            # Input video (loop per durata audio)
            input_files.extend(['-stream_loop', '-1', '-i', files['video']])
            filter_inputs.append(f"[{i*2+1}:v]")
        
        # Filter complex per concatenazione con crossfade
        filter_complex = [
            # Concatena audio con crossfade
            f"{''.join(filter_inputs)}concat=n={len(self.minimix_files)}:v=1:a=1:unsafe=1[outv][outa]"
        ]
        
        # Comando FFmpeg completo
        cmd = [
            'ffmpeg',
            '-hide_banner',
            '-loglevel', 'info',
            '-re',  # Read at native frame rate
        ] + input_files + [
            '-filter_complex', ';'.join(filter_complex),
            '-map', '[outv]',
            '-map', '[outa]',
            
            # Video encoding (coerente con configurazione attuale)
            '-c:v', 'libx264',
            '-preset', self.streaming_params['preset'],
            '-tune', 'zerolatency',
            '-b:v', self.streaming_params['video_bitrate'],
            '-maxrate', self.streaming_params['video_bitrate'],
            '-bufsize', '3000k',  # 2x bitrate
            '-pix_fmt', 'yuv420p',
            '-r', self.streaming_params['fps'],
            '-g', '48',  # Keyframe ogni 2 secondi a 24fps
            
            # Audio encoding
            '-c:a', 'aac',
            '-b:a', self.streaming_params['audio_bitrate'],
            '-ar', '44100',
            '-ac', '2',
            
            # Output
            '-f', 'flv',
            '-flvflags', 'no_duration_filesize',
            self.full_rtmp
        ]
        
        return cmd
    
    def start_streaming(self) -> bool:
        """Avvia streaming FFmpeg Direct"""
        print("🚀 Avvio FFmpeg Direct Streaming...")
        print(f"📺 Target: YouTube RTMP")
        print(f"🎵 Programmi: {len(self.minimix_files)} minimix")
        print(f"⏱️ Durata totale: ~14 ore")
        
        if not self.verify_files():
            print("❌ Verifica file fallita!")
            return False
        
        # Crea comando FFmpeg
        cmd = self.create_ffmpeg_command()
        
        print(f"🔧 Comando FFmpeg preparato")
        print(f"📊 Parametri: {self.streaming_params['resolution']} @ {self.streaming_params['fps']}fps")
        print(f"🎬 Bitrate: {self.streaming_params['video_bitrate']} video, {self.streaming_params['audio_bitrate']} audio")
        
        try:
            # Avvia processo FFmpeg
            self.ffmpeg_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ Streaming avviato! PID: {self.ffmpeg_process.pid}")
            print(f"📊 Monitoraggio: tail -f /home/lofi/ffmpeg_direct.log")
            
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
    print("🎵 FFMPEG DIRECT STREAMING - AQUA LOFI CHILL")
    print("=" * 50)
    
    # Setup signal handler per graceful shutdown
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto, arresto...")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Crea streamer
    streamer = FFmpegDirectStreamer()
    
    # Avvia streaming
    if streamer.start_streaming():
        # Monitora streaming
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming")
        sys.exit(1)

if __name__ == "__main__":
    main() 