#!/usr/bin/env python3
"""
⏰ SIMPLE TIME OVERLAY
=====================

Sistema overlay temporale semplice che:
1. Calcola tempo rimanente
2. Genera immagine overlay
3. Combina con video streaming

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Simple Overlay
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

class SimpleTimeOverlay:
    """Overlay temporale semplice"""
    
    def __init__(self):
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
        
        # Stream start time (da log)
        self.stream_start_time = self.get_stream_start_time()
        
    def get_stream_start_time(self):
        """Ottiene orario inizio stream dal log"""
        try:
            result = subprocess.run([
                'ssh', 'root@159.89.106.38', 
                'head -1 /home/lofi/ffmpeg_concat_fixed.log | cut -d" " -f1-2'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                start_time_str = result.stdout.strip()
                return datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        except:
            pass
        
        # Fallback: ora corrente meno 1 ora
        return datetime.now() - timedelta(hours=1)
    
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
    
    def create_overlay_image(self):
        """Crea immagine overlay con informazioni temporali"""
        position = self.calculate_current_position()
        
        # Crea immagine 400x200 con sfondo semi-trasparente
        img = Image.new('RGBA', (400, 200), (0, 0, 0, 180))
        draw = ImageDraw.Draw(img)
        
        try:
            # Prova a usare font di sistema
            font_large = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
            font_small = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 18)
        except:
            # Fallback a font di default
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Testo overlay
        current_time = datetime.now().strftime("%H:%M")
        remaining_time = self.format_time(position['remaining_seconds'])
        
        lines = [
            f"🎵 {position['current_program_name']}",
            f"⏳ {remaining_time} rimanenti",
            f"🔄 Prossimo: {position['next_program_name']}",
            f"🕐 {current_time}"
        ]
        
        # Disegna testo
        y_offset = 20
        for i, line in enumerate(lines):
            color = (255, 255, 255) if i < 2 else (200, 200, 200)
            font = font_large if i < 2 else font_small
            
            # Centra testo
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (400 - text_width) // 2
            
            draw.text((x, y_offset), line, fill=color, font=font)
            y_offset += 35 if i < 2 else 30
        
        # Salva immagine
        overlay_path = "/tmp/time_overlay.png"
        img.save(overlay_path, "PNG")
        
        return overlay_path
    
    def update_overlay_loop(self):
        """Loop per aggiornare overlay ogni minuto"""
        while True:
            try:
                overlay_path = self.create_overlay_image()
                
                # Upload al server
                subprocess.run([
                    'scp', overlay_path, 
                    'root@159.89.106.38:/tmp/time_overlay.png'
                ], check=True)
                
                print(f"🔄 Overlay aggiornato: {datetime.now().strftime('%H:%M')}")
                
                time.sleep(60)  # Aggiorna ogni minuto
            except Exception as e:
                print(f"❌ Errore aggiornamento overlay: {e}")
                time.sleep(60)
    
    def start_overlay_service(self):
        """Avvia servizio overlay"""
        print("🚀 Avvio Servizio Overlay Temporale...")
        
        # Crea primo overlay
        overlay_path = self.create_overlay_image()
        print(f"✅ Overlay creato: {overlay_path}")
        
        # Upload al server
        try:
            subprocess.run([
                'scp', overlay_path, 
                'root@159.89.106.38:/tmp/time_overlay.png'
            ], check=True)
            print("✅ Overlay uploadato al server")
        except Exception as e:
            print(f"❌ Errore upload: {e}")
        
        # Avvia thread aggiornamento
        overlay_thread = threading.Thread(target=self.update_overlay_loop)
        overlay_thread.daemon = True
        overlay_thread.start()
        
        print("📊 Servizio overlay attivo - aggiornamento ogni minuto")
        print("   Premi Ctrl+C per fermare")
        
        try:
            while True:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n🛑 Servizio overlay fermato")

def main():
    """Main function"""
    print("⏰ SIMPLE TIME OVERLAY SERVICE")
    print("=" * 35)
    
    overlay = SimpleTimeOverlay()
    overlay.start_overlay_service()

if __name__ == "__main__":
    main() 