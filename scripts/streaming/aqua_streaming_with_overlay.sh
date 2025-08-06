#!/bin/bash
"""
🎨 AQUA STREAMING WITH OVERLAY
==============================

Script per avviare streaming Aqua Lofi con overlay temporale integrato.
L'overlay mostra programma corrente e tempo rimanente in basso a sinistra.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Aqua Overlay Streaming
"""

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurazione
SERVER_IP="159.89.106.38"
SERVER_USER="root"
OVERLAY_PATH="/tmp/aqua_time_overlay.png"
YOUTUBE_RTMP="rtmp://a.rtmp.youtube.com/live2/ghfr-q9tg-42fs-xmv7-1fjy"

# File minimix
ABYSS_AUDIO="/home/lofi/media/aqua/ffmpeg_direct/abyss/audio/Abyss_Deep_Minimix_20250722_220340.mp3"
BLUE_BOSSA_AUDIO="/home/lofi/media/aqua/ffmpeg_direct/blue_bossa/audio/Blue_Bossa_Minimix_20250721_175819.mp3"
MEDITATIVE_TIDE_AUDIO="/home/lofi/media/aqua/ffmpeg_direct/meditative_tide/audio/Meditative_Tide Minimix_20250723_113602.mp3"

# Video di base (usa Abyss come video loop)
BASE_VIDEO="/home/lofi/media/aqua/ffmpeg_direct/abyss/video/Abyss Deep_Submarine.mp4"

# File concat
CONCAT_FILE="/tmp/aqua_concat_overlay.txt"

echo -e "${BLUE}🎨 AQUA STREAMING WITH OVERLAY${NC}"
echo "=================================="

# Funzione per verificare connessione SSH
check_ssh_connection() {
    echo -e "${YELLOW}🔍 Verifica connessione SSH...${NC}"
    if ssh -o ConnectTimeout=5 -o BatchMode=yes ${SERVER_USER}@${SERVER_IP} exit 2>/dev/null; then
        echo -e "${GREEN}✅ Connessione SSH OK${NC}"
        return 0
    else
        echo -e "${RED}❌ Errore connessione SSH${NC}"
        return 1
    fi
}

# Funzione per verificare file
check_files() {
    echo -e "${YELLOW}🔍 Verifica file...${NC}"
    
    local files=("$ABYSS_AUDIO" "$BLUE_BOSSA_AUDIO" "$MEDITATIVE_TIDE_AUDIO" "$BASE_VIDEO")
    
    for file in "${files[@]}"; do
        if ssh ${SERVER_USER}@${SERVER_IP} "[ -f '$file' ]"; then
            echo -e "${GREEN}✅ $(basename "$file")${NC}"
        else
            echo -e "${RED}❌ $(basename "$file") mancante${NC}"
            return 1
        fi
    done
    
    return 0
}

# Funzione per creare file concat
create_concat_file() {
    echo -e "${YELLOW}📝 Creazione file concat...${NC}"
    
    local concat_content=""
    concat_content+="file '$ABYSS_AUDIO'\n"
    concat_content+="file '$BLUE_BOSSA_AUDIO'\n"
    concat_content+="file '$MEDITATIVE_TIDE_AUDIO'\n"
    
    ssh ${SERVER_USER}@${SERVER_IP} "echo -e '$concat_content' > $CONCAT_FILE"
    echo -e "${GREEN}✅ File concat creato${NC}"
}

# Funzione per avviare overlay service
start_overlay_service() {
    echo -e "${YELLOW}🚀 Avvio servizio overlay...${NC}"
    
    # Avvia overlay service in background
    python3 scripts/aqua_time_overlay.py &
    OVERLAY_PID=$!
    
    echo -e "${GREEN}✅ Servizio overlay avviato (PID: $OVERLAY_PID)${NC}"
    
    # Aspetta un po' per il primo overlay
    sleep 5
}

# Funzione per avviare streaming con overlay
start_streaming_with_overlay() {
    echo -e "${YELLOW}🎬 Avvio streaming con overlay...${NC}"
    
    # Comando FFmpeg con overlay
    local ffmpeg_cmd="ffmpeg -re -stream_loop -1 -i '$BASE_VIDEO' \
        -f concat -safe 0 -stream_loop -1 -i '$CONCAT_FILE' \
        -map 0:v:0 -map 1:a:0 \
        -c:v libx264 -preset ultrafast -b:v 6800k \
        -c:a aac -b:a 128k \
        -filter_complex 'overlay=30:H-h-30' \
        -f flv '$YOUTUBE_RTMP'"
    
    echo -e "${BLUE}🔧 Comando FFmpeg:${NC}"
    echo "$ffmpeg_cmd"
    echo ""
    
    # Esegui streaming
    ssh ${SERVER_USER}@${SERVER_IP} "$ffmpeg_cmd"
}

# Funzione per fermare tutto
cleanup() {
    echo -e "${YELLOW}🛑 Arresto servizi...${NC}"
    
    # Ferma overlay service
    if [ ! -z "$OVERLAY_PID" ]; then
        kill $OVERLAY_PID 2>/dev/null || true
        echo -e "${GREEN}✅ Servizio overlay fermato${NC}"
    fi
    
    # Ferma FFmpeg sul server
    ssh ${SERVER_USER}@${SERVER_IP} "pkill -f ffmpeg" 2>/dev/null || true
    echo -e "${GREEN}✅ Streaming fermato${NC}"
    
    exit 0
}

# Trap per cleanup
trap cleanup SIGINT SIGTERM

# Main execution
main() {
    echo -e "${BLUE}🚀 Inizializzazione streaming con overlay...${NC}"
    
    # Verifica connessione
    if ! check_ssh_connection; then
        echo -e "${RED}❌ Impossibile connettersi al server${NC}"
        exit 1
    fi
    
    # Verifica file
    if ! check_files; then
        echo -e "${RED}❌ File mancanti sul server${NC}"
        exit 1
    fi
    
    # Crea file concat
    create_concat_file
    
    # Avvia overlay service
    start_overlay_service
    
    echo -e "${GREEN}🎉 Tutto pronto! Avvio streaming...${NC}"
    echo -e "${YELLOW}   Premi Ctrl+C per fermare${NC}"
    echo ""
    
    # Avvia streaming
    start_streaming_with_overlay
}

# Esegui main
main "$@" 