#!/usr/bin/env python3
"""
⏰ AQUA TIME OVERLAY
===================

Overlay temporale per Aqua Lofi con:
- Posizionamento: basso a sinistra (allineato con logo)
- Font: Open Sans / Noto Sans
- Dimensione: compatta e leggibile
- Aggiornamento: ogni 30 secondi

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Aqua Overlay
"""

import os
import sys
import subprocess
import time
import signal
import threading
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
import textwrap

class AquaTimeOverlay:
    """Overlay temporale Aqua Lofi"""
    
    def __init__(self):
        # Durate reali (secondi)
        self.minimix_durations = {
            'blue_bossa': 18688, # 5.19 ore
            'abyss': 16665,      # 4.62 ore
            'meditative_tide': 15083  # 4.18 ore
        }
        
        # Ordine palinsesto aggiornato
        self.palinsest_order = ['blue_bossa', 'meditative_tide', 'abyss']
        self.friendly_names = {
            'blue_bossa': 'Blue Bossa',
            'meditative_tide': 'Meditative Tide',
            'abyss': 'Abyss Deep'
        }
        
        # Stream start time (da log del riavvio)
        self.stream_start_time = self.get_stream_start_time()
        
        # Configurazione overlay
        self.overlay_width = 280
        self.overlay_height = 80
        self.margin_left = 30
        self.margin_bottom = 30
        
    def get_stream_start_time(self):
        """Ottiene orario inizio stream dal log del riavvio"""
        try:
            result = subprocess.run([
                'ssh', 'root@159.89.106.38', 
                'head -1 /home/lofi/ffmpeg_blue_bossa_restart.log | cut -d" " -f1-2'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                start_time_str = result.stdout.strip()
                return datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        except:
            pass
        
        # Fallback: ora corrente meno 5 minuti (riavvio recente)
        return datetime.now() - timedelta(minutes=5)
    
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
    
    def get_font(self, size):
        """Ottiene font Open Sans o fallback"""
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/open-sans/OpenSans-Regular.ttf",  # Linux
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",  # Linux Noto
            "/Library/Fonts/Open Sans/OpenSans-Regular.ttf",  # macOS custom
        ]
        
        for font_path in font_paths:
            try:
                return ImageFont.truetype(font_path, size)
            except:
                continue
        
        # Fallback a font di default
        return ImageFont.load_default()
    
    def create_overlay_image(self):
        """Crea immagine overlay compatta in basso a sinistra"""
        position = self.calculate_current_position()
        
        # Crea immagine con sfondo semi-trasparente
        img = Image.new('RGBA', (self.overlay_width, self.overlay_height), (0, 0, 0, 160))
        draw = ImageDraw.Draw(img)
        
        # Font
        font_main = self.get_font(16)
        font_small = self.get_font(12)
        
        # Testo overlay - formato richiesto
        remaining_time = self.format_time(position['remaining_seconds'])
        
        # Linee di testo con nuovo formato
        lines = [
            f"Now streaming: {position['current_program_name']}",
            f"Next on Aqua Lofi: {position['next_program_name']}",
            f"{remaining_time} to go"
        ]
        
        # Disegna testo
        y_offset = 8
        for i, line in enumerate(lines):
            color = (255, 255, 255) if i == 0 else (220, 220, 220)
            font = font_main if i == 0 else font_small
            
            # Allinea a sinistra con margine
            x = 10
            
            draw.text((x, y_offset), line, fill=color, font=font)
            y_offset += 22 if i == 0 else 18
        
        # Salva immagine
        overlay_path = "/tmp/aqua_time_overlay.png"
        img.save(overlay_path, "PNG")
        
        return overlay_path
    
    def update_overlay_loop(self):
        """Loop per aggiornare overlay ogni 30 secondi"""
        while True:
            try:
                overlay_path = self.create_overlay_image()
                
                # Upload al server
                subprocess.run([
                    'scp', overlay_path, 
                    'root@159.89.106.38:/tmp/aqua_time_overlay.png'
                ], check=True)
                
                print(f"🔄 Overlay aggiornato: {datetime.now().strftime('%H:%M:%S')}")
                
                time.sleep(30)  # Aggiorna ogni 30 secondi
            except Exception as e:
                print(f"❌ Errore aggiornamento overlay: {e}")
                time.sleep(30)
    
    def start_overlay_service(self):
        """Avvia servizio overlay"""
        print("🚀 Avvio Overlay Temporale Aqua Lofi...")
        print(f"📍 Posizione: basso a sinistra ({self.margin_left}px, {self.margin_bottom}px)")
        print(f"📏 Dimensione: {self.overlay_width}x{self.overlay_height}px")
        print(f"⏰ Aggiornamento: ogni 30 secondi")
        
        # Crea primo overlay
        overlay_path = self.create_overlay_image()
        print(f"✅ Overlay creato: {overlay_path}")
        
        # Upload al server
        try:
            subprocess.run([
                'scp', overlay_path, 
                'root@159.89.106.38:/tmp/aqua_time_overlay.png'
            ], check=True)
            print("✅ Overlay uploadato al server")
        except Exception as e:
            print(f"❌ Errore upload: {e}")
        
        # Avvia thread aggiornamento
        overlay_thread = threading.Thread(target=self.update_overlay_loop)
        overlay_thread.daemon = True
        overlay_thread.start()
        
        print("📊 Servizio overlay attivo")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n🛑 Servizio overlay fermato")
    
    def get_ffmpeg_overlay_command(self):
        """Restituisce comando FFmpeg per integrare overlay"""
        return f"""
# Comando FFmpeg con overlay temporale:
ffmpeg -i video.mp4 -i /tmp/aqua_time_overlay.png \\
  -filter_complex "overlay={self.margin_left}:H-h-{self.margin_bottom}" \\
  -c:v libx264 -c:a copy output_with_overlay.mp4

# Per streaming live:
ffmpeg -i video.mp4 -i /tmp/aqua_time_overlay.png \\
  -filter_complex "overlay={self.margin_left}:H-h-{self.margin_bottom}" \\
  -c:v libx264 -preset ultrafast -b:v 6800k \\
  -c:a aac -b:a 128k -f flv rtmp://...
"""

def main():
    """Main function"""
    print("⏰ AQUA TIME OVERLAY")
    print("=" * 25)
    
    overlay = AquaTimeOverlay()
    
    if len(sys.argv) > 1 and sys.argv[1] == "command":
        print(overlay.get_ffmpeg_overlay_command())
    else:
        overlay.start_overlay_service()

if __name__ == "__main__":
    main() 