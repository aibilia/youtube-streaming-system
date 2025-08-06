#!/bin/bash

# 🎵 CONTROLLO FFMPEG DIRECT STREAMING
# =====================================

STREAMING_SCRIPT="/home/lofi/ffmpeg_direct_simple.py"
LOG_FILE="/home/lofi/ffmpeg_direct_simple.log"

case "$1" in
    "start")
        echo "🚀 Avvio FFmpeg Direct Streaming..."
        ssh root@159.89.106.38 "cd /home/lofi && nohup python3 ffmpeg_direct_audio_fixed.py > ffmpeg_direct_audio_fixed.log 2>&1 & echo 'Streaming audio corretto avviato'"
        ;;
    
    "stop")
        echo "🛑 Arresto FFmpeg Direct Streaming..."
        ssh root@159.89.106.38 "pkill -f ffmpeg_direct_audio_fixed.py && pkill -f 'ffmpeg.*youtube' && echo 'Streaming fermato'"
        ;;
    
    "status")
        echo "📊 Status FFmpeg Direct Streaming..."
        ssh root@159.89.106.38 "ps aux | grep ffmpeg | grep -v grep || echo 'Nessun processo FFmpeg attivo'"
        ;;
    
    "logs")
        echo "📋 Log FFmpeg Direct Streaming..."
        ssh root@159.89.106.38 "tail -20 /home/lofi/ffmpeg_direct_audio_fixed.log"
        ;;
    
    "restart")
        echo "🔄 Restart FFmpeg Direct Streaming..."
        ssh root@159.89.106.38 "pkill -f ffmpeg_direct_audio_fixed.py && pkill -f 'ffmpeg.*youtube' && sleep 2 && cd /home/lofi && nohup python3 ffmpeg_direct_audio_fixed.py > ffmpeg_direct_audio_fixed.log 2>&1 & echo 'Streaming audio corretto riavviato'"
        ;;
    
    *)
        echo "🎵 FFMPEG DIRECT STREAMING CONTROL"
        echo "=================================="
        echo "Uso: $0 {start|stop|status|logs|restart}"
        echo ""
        echo "Comandi:"
        echo "  start   - Avvia streaming"
        echo "  stop    - Ferma streaming"
        echo "  status  - Mostra status processi"
        echo "  logs    - Mostra log recenti"
        echo "  restart - Riavvia streaming"
        ;;
esac 