#!/usr/bin/env python3
"""
🎨 FFMPEG WITH TIME OVERLAY
===========================

Streaming FFmpeg con overlay temporale live che mostra:
- Programma corrente
- Tempo rimanente
- Prossimo programma

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Time Overlay
"""

import os
import sys
import subprocess
import time
import signal
import threading
from datetime import datetime, timedelta
from pathlib import Path

class FFmpegTimeOverlayStreamer:
    """Streaming con overlay temporale"""
    
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
        
        # Durate reali (secondi)
        self.minimix_durations = {
            'abyss': 16665,      # 4.62 ore
            'blue_bossa': 18688, # 5.19 ore  
            'meditative_tide': 15083  # 4.18 ore
        }
        
        # Ordine palinsesto
        self.palinsest_order = ['abyss', 'blue_bossa', 'meditative_tide']
        self.friendly_names = {
            'abyss': 'Abyss Deep',
            'blue_bossa': 'Blue Bossa', 
            'meditative_tide': 'Meditative Tide'
        }
        
        # YouTube
        self.youtube_rtmp = "rtmp://a.rtmp.youtube.com/live2"
        self.youtube_key = "ghfr-q9tg-42fs-xmv7-1fjy"
        self.full_rtmp = f"{self.youtube_rtmp}/{self.youtube_key}"
        
        # Processo
        self.ffmpeg_process = None
        self.stream_start_time = datetime.now()
        
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
        
        concat_file = "/tmp/aqua_concat_overlay.txt"
        with open(concat_file, 'w') as f:
            f.write(concat_content)
        
        print(f"📝 File concat creato: {concat_file}")
        return concat_file
    
    def calculate_current_position(self):
        """Calcola posizione corrente nel palinsesto"""
        elapsed_seconds = (datetime.now() - self.stream_start_time).total_seconds()
        
        # Calcola il ciclo completo
        total_cycle_seconds = sum(self.minimix_durations.values())
        
        # Calcola quanti cicli completi sono passati
        cycles_completed = int(elapsed_seconds // total_cycle_seconds)
        
        # Calcola la posizione nel ciclo corrente
        current_cycle_seconds = elapsed_seconds % total_cycle_seconds
        
        # Trova il programma corrente
        current_program = None
        accumulated_time = 0
        
        for program in self.palinsest_order:
            if current_cycle_seconds < accumulated_time + self.minimix_durations[program]:
                current_program = program
                break
            accumulated_time += self.minimix_durations[program]
        
        if not current_program:
            current_program = self.palinsest_order[0]
            accumulated_time = 0
        
        # Calcola tempo rimanente nel programma corrente
        time_in_current = current_cycle_seconds - accumulated_time
        remaining_in_current = self.minimix_durations[current_program] - time_in_current
        
        # Trova il prossimo programma
        current_index = self.palinsest_order.index(current_program)
        next_index = (current_index + 1) % len(self.palinsest_order)
        next_program = self.palinsest_order[next_index]
        
        return {
            'current_program': current_program,
            'current_program_name': self.friendly_names[current_program],
            'remaining_seconds': remaining_in_current,
            'next_program': next_program,
            'next_program_name': self.friendly_names[next_program],
            'cycles_completed': cycles_completed
        }
    
    def format_time(self, seconds):
        """Formatta il tempo in formato leggibile"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    
    def generate_overlay_text(self):
        """Genera testo overlay corrente"""
        position = self.calculate_current_position()
        
        current_time = datetime.now().strftime("%H:%M")
        remaining_time = self.format_time(position['remaining_seconds'])
        
        overlay_text = f"🎵 {position['current_program_name']}\n"
        overlay_text += f"⏳ {remaining_time} rimanenti\n"
        overlay_text += f"🔄 Prossimo: {position['next_program_name']}\n"
        overlay_text += f"🕐 {current_time}"
        
        return overlay_text
    
    def start_streaming(self) -> bool:
        """Avvia streaming con overlay temporale"""
        print("🚀 Avvio Streaming con Overlay Temporale...")
        
        if not self.verify_all_files():
            return False
        
        concat_file = self.create_concat_file()
        
        # Genera testo overlay iniziale
        overlay_text = self.generate_overlay_text()
        
        # Comando FFmpeg con OVERLAY TEMPORALE
        # Usa drawtext filter per overlay dinamico
        cmd = [
            'ffmpeg',
            '-re',
            '-stream_loop', '-1',
            '-i', self.minimix_files['abyss']['video'],
            '-f', 'concat',
            '-safe', '0',
            '-stream_loop', '-1',
            '-i', concat_file,
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-b:v', '6800k',
            '-c:a', 'aac',
            '-b:a', '128k',
            # OVERLAY TEMPORALE
            '-vf', f'drawtext=text=\'{overlay_text}\':fontcolor=white:fontsize=24:box=1:boxcolor=black@0.7:x=50:y=50:reload=1',
            '-f', 'flv',
            self.full_rtmp
        ]
        
        print(f"🔧 Comando con Overlay: {' '.join(cmd)}")
        
        try:
            self.ffmpeg_process = subprocess.Popen(cmd)
            print(f"✅ Streaming con Overlay avviato! PID: {self.ffmpeg_process.pid}")
            return True
        except Exception as e:
            print(f"❌ Errore: {e}")
            return False
    
    def update_overlay_thread(self):
        """Thread per aggiornare overlay ogni 30 secondi"""
        while self.ffmpeg_process and self.ffmpeg_process.poll() is None:
            try:
                # Genera nuovo testo overlay
                overlay_text = self.generate_overlay_text()
                
                # Salva in file temporaneo per FFmpeg reload
                overlay_file = "/tmp/overlay_text.txt"
                with open(overlay_file, 'w') as f:
                    f.write(overlay_text)
                
                print(f"🔄 Overlay aggiornato: {overlay_text.split()[0]} {overlay_text.split()[1]}")
                
                time.sleep(30)  # Aggiorna ogni 30 secondi
            except Exception as e:
                print(f"❌ Errore aggiornamento overlay: {e}")
                time.sleep(30)
    
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
        
        print("📊 Monitoraggio con Overlay...")
        print("   Premi Ctrl+C per fermare")
        
        # Avvia thread aggiornamento overlay
        overlay_thread = threading.Thread(target=self.update_overlay_thread)
        overlay_thread.daemon = True
        overlay_thread.start()
        
        try:
            while True:
                if self.ffmpeg_process.poll() is not None:
                    print("❌ Processo terminato!")
                    break
                time.sleep(30)
                print(f"⏰ Streaming con Overlay attivo - PID: {self.ffmpeg_process.pid}")
        except KeyboardInterrupt:
            print("\n🛑 Interruzione richiesta")
            self.stop_streaming()

def main():
    """Main function"""
    print("🎨 FFMPEG WITH TIME OVERLAY")
    print("=" * 30)
    
    def signal_handler(signum, frame):
        print(f"\n🛑 Segnale {signum} ricevuto")
        if streamer:
            streamer.stop_streaming()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    streamer = FFmpegTimeOverlayStreamer()
    
    if streamer.start_streaming():
        streamer.monitor_streaming()
    else:
        print("❌ Impossibile avviare streaming")
        sys.exit(1)

if __name__ == "__main__":
    main() 