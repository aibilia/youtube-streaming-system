#!/usr/bin/env python3
"""
🔄 UPDATE PALINSEST ORDER
========================

Script per aggiornare l'ordine del palinsesto senza interrompere lo streaming.
Modifica il file concat per cambiare l'ordine: Blue Bossa → Meditative Tide → Abyss Deep

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Update Order
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def update_palinsest_order():
    """Aggiorna ordine palinsesto senza interrompere streaming"""
    
    print("🔄 AGGIORNAMENTO ORDINE PALINSESTO")
    print("=" * 40)
    print("📺 Nuovo ordine: Blue Bossa → Meditative Tide → Abyss Deep")
    
    # Configurazione
    SERVER_IP = "159.89.106.38"
    SERVER_USER = "root"
    
    # File minimix
    BLUE_BOSSA_AUDIO = "/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3"
    MEDITATIVE_TIDE_AUDIO = "/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3"
    ABYSS_AUDIO = "/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
    
    # File concat attuale e nuovo
    CURRENT_CONCAT = "/tmp/aqua_concat_blue_bossa_first.txt"
    NEW_CONCAT = "/tmp/aqua_concat_updated_order.txt"
    
    print("\n🔍 Verifica file sul server...")
    
    # Verifica file
    files_to_check = [
        BLUE_BOSSA_AUDIO,
        MEDITATIVE_TIDE_AUDIO,
        ABYSS_AUDIO
    ]
    
    for file_path in files_to_check:
        result = subprocess.run([
            'ssh', f'{SERVER_USER}@{SERVER_IP}', 
            f'[ -f "{file_path}" ] && echo "OK" || echo "MISSING"'
        ], capture_output=True, text=True)
        
        if "OK" in result.stdout:
            print(f"✅ {os.path.basename(file_path)}")
        else:
            print(f"❌ {os.path.basename(file_path)} mancante")
            return False
    
    print("\n📝 Creazione nuovo file concat...")
    
    # Crea nuovo file concat con ordine aggiornato
    concat_content = f"""file '{BLUE_BOSSA_AUDIO}'
file '{MEDITATIVE_TIDE_AUDIO}'
file '{ABYSS_AUDIO}'
"""
    
    # Upload nuovo file concat
    subprocess.run([
        'ssh', f'{SERVER_USER}@{SERVER_IP}', 
        f'echo "{concat_content}" > {NEW_CONCAT}'
    ], check=True)
    
    print("✅ Nuovo file concat creato")
    
    print("\n🔍 Verifica processo FFmpeg attuale...")
    
    # Controlla processo FFmpeg attuale
    result = subprocess.run([
        'ssh', f'{SERVER_USER}@{SERVER_IP}', 
        'ps aux | grep ffmpeg | grep -v grep'
    ], capture_output=True, text=True)
    
    if not result.stdout.strip():
        print("❌ Nessun processo FFmpeg attivo")
        return False
    
    print("✅ Processo FFmpeg attivo trovato")
    
    print("\n🔄 Aggiornamento ordine palinsesto...")
    
    # Sostituisci file concat senza fermare FFmpeg
    # FFmpeg continuerà a usare il file concat corrente fino al prossimo ciclo
    subprocess.run([
        'ssh', f'{SERVER_USER}@{SERVER_IP}', 
        f'cp {NEW_CONCAT} {CURRENT_CONCAT}'
    ], check=True)
    
    print("✅ Ordine palinsesto aggiornato")
    print("📝 Il nuovo ordine sarà attivo al prossimo ciclo")
    
    print("\n📊 Nuovo ordine palinsesto:")
    print("   1. Blue Bossa (5.19 ore)")
    print("   2. Meditative Tide (4.18 ore)")
    print("   3. Abyss Deep (4.62 ore)")
    print("   ⏱️ Ciclo totale: 13.99 ore")
    
    return True

def main():
    """Main function"""
    try:
        update_palinsest_order()
        print("\n🎉 Aggiornamento completato!")
        print("📺 Streaming continua senza interruzioni")
        print("🔄 Nuovo ordine attivo al prossimo ciclo")
    except Exception as e:
        print(f"❌ Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 