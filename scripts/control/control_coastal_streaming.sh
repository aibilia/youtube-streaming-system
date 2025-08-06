#!/bin/bash
#
# 🎵 Control Coastal Streaming
# ============================
#
# Script di controllo per il sistema di streaming FFmpeg Direct con Coastal.
#
# Author: AI Assistant
# Date: 3 Agosto 2025
# Version: 1.0 Coastal Edition
#

# Configurazione
SCRIPT_PATH="/home/lofi/ffmpeg_concat_fixed_coastal.py"
LOG_FILE="/home/lofi/ffmpeg_coastal_streaming.log"
PID_FILE="/home/lofi/ffmpeg_coastal_streaming.pid"

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funzioni di utilità
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

success() {
    echo -e "${GREEN}✅ $1${NC}" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}⚠️ $1${NC}" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}❌ $1${NC}" | tee -a "$LOG_FILE"
}

# Funzioni principali
check_status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            success "Streaming attivo (PID: $PID)"
            return 0
        else
            warning "PID file presente ma processo non attivo"
            rm -f "$PID_FILE"
            return 1
        fi
    else
        error "Streaming non attivo"
        return 1
    fi
}

start_streaming() {
    log "🎵 Avvio streaming Coastal..."
    
    if check_status > /dev/null 2>&1; then
        warning "Streaming già attivo!"
        return 1
    fi
    
    # Avvia streaming in background
    nohup python3 "$SCRIPT_PATH" > "$LOG_FILE" 2>&1 &
    PID=$!
    
    # Salva PID
    echo "$PID" > "$PID_FILE"
    
    # Aspetta un momento per verificare che sia partito
    sleep 3
    
    if check_status > /dev/null 2>&1; then
        success "Streaming avviato con successo (PID: $PID)"
        return 0
    else
        error "Errore nell'avvio dello streaming"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_streaming() {
    log "🛑 Fermando streaming Coastal..."
    
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        
        if ps -p "$PID" > /dev/null 2>&1; then
            kill "$PID"
            
            # Aspetta terminazione
            for i in {1..10}; do
                if ! ps -p "$PID" > /dev/null 2>&1; then
                    success "Streaming fermato"
                    rm -f "$PID_FILE"
                    return 0
                fi
                sleep 1
            done
            
            # Forza terminazione se necessario
            warning "Forzando terminazione..."
            kill -9 "$PID"
            success "Streaming forzatamente fermato"
            rm -f "$PID_FILE"
        else
            warning "Processo non trovato, rimuovo PID file"
            rm -f "$PID_FILE"
        fi
    else
        warning "Nessun PID file trovato"
    fi
}

restart_streaming() {
    log "🔄 Riavvio streaming Coastal..."
    stop_streaming
    sleep 2
    start_streaming
}

show_logs() {
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}📋 Ultimi 50 log:${NC}"
        tail -50 "$LOG_FILE"
    else
        error "File log non trovato"
    fi
}

show_help() {
    echo -e "${BLUE}🎵 Control Coastal Streaming${NC}"
    echo "================================"
    echo ""
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandi disponibili:"
    echo "  start     - Avvia streaming"
    echo "  stop      - Ferma streaming"
    echo "  restart   - Riavvia streaming"
    echo "  status    - Mostra status"
    echo "  logs      - Mostra log recenti"
    echo "  help      - Mostra questo aiuto"
    echo ""
}

# Controllo argomenti
case "$1" in
    start)
        start_streaming
        ;;
    stop)
        stop_streaming
        ;;
    restart)
        restart_streaming
        ;;
    status)
        check_status
        ;;
    logs)
        show_logs
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando non riconosciuto: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac 