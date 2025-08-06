#!/bin/bash
#
# 🎵 CONTROL AQUA STREAMING
# ==========================
#
# Script di controllo per lo streaming Aqua completo.
#
# Author: AI Assistant
# Date: 24 Luglio 2025
# Version: 1.0 Control Aqua
#

case "$1" in
    start)
        echo "🚀 Avvio Streaming Aqua Completo..."
        ssh root@159.89.106.38 "cd /home/lofi && nohup python3 ffmpeg_concat_fixed.py > ffmpeg_concat_fixed.log 2>&1 & echo 'Streaming Aqua avviato'"
        ;;
    stop)
        echo "🛑 Arresto Streaming Aqua..."
        ssh root@159.89.106.38 "pkill -f ffmpeg_concat_fixed.py && pkill -f 'ffmpeg.*youtube' && echo 'Streaming Aqua fermato'"
        ;;
    status)
        echo "📊 Status Streaming Aqua..."
        ssh root@159.89.106.38 "ps aux | grep ffmpeg | grep -v grep || echo 'Nessun processo FFmpeg attivo'"
        ;;
    logs)
        echo "📋 Log Streaming Aqua..."
        ssh root@159.89.106.38 "tail -20 /home/lofi/ffmpeg_concat_fixed.log"
        ;;
    restart)
        echo "🔄 Riavvio Streaming Aqua..."
        ssh root@159.89.106.38 "pkill -f ffmpeg_concat_fixed.py && pkill -f 'ffmpeg.*youtube' && sleep 2 && cd /home/lofi && nohup python3 ffmpeg_concat_fixed.py > ffmpeg_concat_fixed.log 2>&1 & echo 'Streaming Aqua riavviato'"
        ;;
    *)
        echo "🎵 Control Aqua Streaming"
        echo "========================="
        echo "Uso: $0 {start|stop|status|logs|restart}"
        echo ""
        echo "  start   - Avvia streaming Aqua completo"
        echo "  stop    - Ferma streaming Aqua"
        echo "  status  - Mostra status processi"
        echo "  logs    - Mostra log streaming"
        echo "  restart - Riavvia streaming Aqua"
        echo ""
        echo "🎵 Streaming Aqua: Abyss Deep + Blue Bossa + Meditative Tide"
        exit 1
        ;;
esac 