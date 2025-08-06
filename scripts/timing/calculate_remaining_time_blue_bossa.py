#!/usr/bin/env python3
"""
⏰ CALCOLO TEMPO RIMANENTE - BLUE BOSSA FIRST
=============================================

Calcola il tempo rimanente nel palinsesto che parte da Blue Bossa.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Blue Bossa Calculator
"""

import os
import time
import subprocess
from datetime import datetime, timedelta

class BlueBossaPalinsestCalculator:
    """Calcolatore tempo palinsesto Blue Bossa First"""
    
    def __init__(self):
        # Durate reali dei minimix (in secondi)
        self.minimix_durations = {
            'blue_bossa': 18688, # 5.19 ore
            'abyss': 16665,      # 4.62 ore
            'meditative_tide': 15083  # 4.18 ore
        }
        
        # Ordine del palinsesto (Blue Bossa primo)
        self.palinsest_order = ['blue_bossa', 'abyss', 'meditative_tide']
        
        # Nomi amichevoli
        self.friendly_names = {
            'blue_bossa': 'Blue Bossa',
            'abyss': 'Abyss Deep', 
            'meditative_tide': 'Meditative Tide'
        }
    
    def get_stream_start_time(self):
        """Ottiene l'orario di inizio dello stream"""
        try:
            # Legge il timestamp di inizio dal file log del riavvio
            result = subprocess.run([
                'ssh', 'root@159.89.106.38', 
                'head -1 /home/lofi/ffmpeg_blue_bossa_restart.log | cut -d" " -f1-2'
            ], capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                start_time_str = result.stdout.strip()
                return datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        except:
            pass
        
        # Fallback: usa ora corrente meno 5 minuti (riavvio recente)
        return datetime.now() - timedelta(minutes=5)
    
    def calculate_current_position(self):
        """Calcola la posizione corrente nel palinsesto"""
        start_time = self.get_stream_start_time()
        elapsed_seconds = (datetime.now() - start_time).total_seconds()
        
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
            'cycles_completed': cycles_completed,
            'total_elapsed': elapsed_seconds
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
    
    def get_status(self):
        """Ottiene lo status completo"""
        position = self.calculate_current_position()
        
        return {
            'current_program': position['current_program_name'],
            'remaining_time': self.format_time(position['remaining_seconds']),
            'next_program': position['next_program_name'],
            'cycles_completed': position['cycles_completed'],
            'total_elapsed': self.format_time(position['total_elapsed'])
        }

def main():
    """Main function"""
    calculator = BlueBossaPalinsestCalculator()
    status = calculator.get_status()
    
    print("⏰ STATUS PALINSESTO AQUA LOFI - BLUE BOSSA FIRST")
    print("=" * 50)
    print(f"🎵 Programma Corrente: {status['current_program']}")
    print(f"⏳ Tempo Rimanente: {status['remaining_time']}")
    print(f"🔄 Prossimo Programma: {status['next_program']}")
    print(f"🔄 Cicli Completati: {status['cycles_completed']}")
    print(f"⏱️ Tempo Totale Trascorso: {status['total_elapsed']}")
    print(f"📺 Ordine Palinsesto: Blue Bossa → Abyss Deep → Meditative Tide")

if __name__ == "__main__":
    main() 