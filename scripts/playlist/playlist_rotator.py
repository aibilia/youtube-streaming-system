#!/usr/bin/env python3
# Script di rotazione playlist per OBS
import json
import time
from datetime import datetime, timedelta

CONFIG_FILE = "/home/lofi/media/aqua/obs_streaming_config.json"
ROTATION_INTERVAL = 60  # minuti

def rotate_playlist():
    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        current = config['streaming_setup']['current_program']
        programs = config['streaming_setup']['rotation_programs']
        
        # Trova prossimo programma
        current_index = programs.index(current)
        next_index = (current_index + 1) % len(programs)
        next_program = programs[next_index]
        
        # Aggiorna configurazione
        config['streaming_setup']['current_program'] = next_program
        config['streaming_setup']['last_rotation'] = datetime.now().isoformat()
        
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"🔄 Rotazione: {current} -> {next_program}")
        return next_program
        
    except Exception as e:
        print(f"❌ Errore rotazione: {e}")
        return None

if __name__ == "__main__":
    rotate_playlist()
