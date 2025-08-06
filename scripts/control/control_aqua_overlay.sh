#!/bin/bash
"""
⏰ CONTROL AQUA OVERLAY
=======================

Script per controllare il servizio overlay temporale Aqua Lofi.
Gestisce avvio, stop, status e aggiornamento dell'overlay.

Author: AI Assistant
Date: 24 Luglio 2025
Version: 1.0 Overlay Control
"""

set -e

# Colori per output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configurazione
OVERLAY_SCRIPT="scripts/aqua_time_overlay.py"
OVERLAY_PID_FILE="/tmp/aqua_overlay.pid"
OVERLAY_LOG_FILE="/tmp/aqua_overlay.log"

echo -e "${BLUE}⏰ CONTROL AQUA OVERLAY${NC}"
echo "=========================="

# Funzione per mostrare help
show_help() {
    echo "Uso: $0 [comando]"
    echo ""
    echo "Comandi disponibili:"
    echo "  start     - Avvia servizio overlay"
    echo "  stop      - Ferma servizio overlay"
    echo "  restart   - Riavvia servizio overlay"
    echo "  status    - Mostra status servizio"
    echo "  test      - Testa generazione overlay"
    echo "  preview   - Mostra preview overlay"
    echo "  help      - Mostra questo help"
    echo ""
    echo "Esempi:"
    echo "  $0 start"
    echo "  $0 status"
    echo "  $0 stop"
}

# Funzione per verificare se overlay è attivo
is_overlay_running() {
    if [ -f "$OVERLAY_PID_FILE" ]; then
        local pid=$(cat "$OVERLAY_PID_FILE")
        if ps -p "$pid" > /dev/null 2>&1; then
            return 0
        else
            rm -f "$OVERLAY_PID_FILE"
            return 1
        fi
    fi
    return 1
}

# Funzione per avviare overlay
start_overlay() {
    echo -e "${YELLOW}🚀 Avvio servizio overlay...${NC}"
    
    if is_overlay_running; then
        echo -e "${YELLOW}⚠️  Servizio overlay già attivo${NC}"
        return 0
    fi
    
    # Avvia overlay service in background
    nohup python3 "$OVERLAY_SCRIPT" > "$OVERLAY_LOG_FILE" 2>&1 &
    local pid=$!
    
    # Salva PID
    echo "$pid" > "$OVERLAY_PID_FILE"
    
    # Aspetta un po' per verificare avvio
    sleep 2
    
    if is_overlay_running; then
        echo -e "${GREEN}✅ Servizio overlay avviato (PID: $pid)${NC}"
        echo -e "${BLUE}📝 Log: $OVERLAY_LOG_FILE${NC}"
    else
        echo -e "${RED}❌ Errore avvio servizio overlay${NC}"
        rm -f "$OVERLAY_PID_FILE"
        return 1
    fi
}

# Funzione per fermare overlay
stop_overlay() {
    echo -e "${YELLOW}🛑 Arresto servizio overlay...${NC}"
    
    if ! is_overlay_running; then
        echo -e "${YELLOW}⚠️  Servizio overlay non attivo${NC}"
        return 0
    fi
    
    local pid=$(cat "$OVERLAY_PID_FILE")
    kill "$pid" 2>/dev/null || true
    
    # Aspetta arresto
    sleep 2
    
    if ! is_overlay_running; then
        echo -e "${GREEN}✅ Servizio overlay fermato${NC}"
        rm -f "$OVERLAY_PID_FILE"
    else
        echo -e "${RED}❌ Errore arresto servizio overlay${NC}"
        return 1
    fi
}

# Funzione per riavviare overlay
restart_overlay() {
    echo -e "${YELLOW}🔄 Riavvio servizio overlay...${NC}"
    stop_overlay
    sleep 1
    start_overlay
}

# Funzione per status overlay
status_overlay() {
    echo -e "${BLUE}📊 Status Servizio Overlay${NC}"
    echo "========================"
    
    if is_overlay_running; then
        local pid=$(cat "$OVERLAY_PID_FILE")
        echo -e "${GREEN}✅ Servizio overlay ATTIVO${NC}"
        echo "   PID: $pid"
        echo "   Log: $OVERLAY_LOG_FILE"
        
        # Mostra ultime righe del log
        if [ -f "$OVERLAY_LOG_FILE" ]; then
            echo ""
            echo -e "${BLUE}📝 Ultime righe log:${NC}"
            tail -5 "$OVERLAY_LOG_FILE" 2>/dev/null || echo "   Nessun log disponibile"
        fi
    else
        echo -e "${RED}❌ Servizio overlay NON ATTIVO${NC}"
    fi
    
    # Mostra file overlay
    if [ -f "/tmp/aqua_time_overlay.png" ]; then
        echo ""
        echo -e "${GREEN}📁 File overlay: /tmp/aqua_time_overlay.png${NC}"
        ls -la "/tmp/aqua_time_overlay.png"
    else
        echo ""
        echo -e "${RED}📁 File overlay: NON TROVATO${NC}"
    fi
}

# Funzione per test overlay
test_overlay() {
    echo -e "${YELLOW}🧪 Test generazione overlay...${NC}"
    
    if python3 -c "from scripts.aqua_time_overlay import AquaTimeOverlay; overlay = AquaTimeOverlay(); path = overlay.create_overlay_image(); print(f'✅ Overlay creato: {path}')"; then
        echo -e "${GREEN}✅ Test overlay completato${NC}"
        
        if [ -f "/tmp/aqua_time_overlay.png" ]; then
            echo -e "${BLUE}📁 File: /tmp/aqua_time_overlay.png${NC}"
            ls -la "/tmp/aqua_time_overlay.png"
        fi
    else
        echo -e "${RED}❌ Errore test overlay${NC}"
        return 1
    fi
}

# Funzione per preview overlay
preview_overlay() {
    echo -e "${YELLOW}👁️  Preview overlay...${NC}"
    
    # Genera overlay
    if python3 -c "from scripts.aqua_time_overlay import AquaTimeOverlay; overlay = AquaTimeOverlay(); overlay.create_overlay_image()"; then
        echo -e "${GREEN}✅ Overlay generato${NC}"
        
        # Prova ad aprire con preview (macOS)
        if command -v open >/dev/null 2>&1; then
            open "/tmp/aqua_time_overlay.png"
            echo -e "${BLUE}👁️  Preview aperto${NC}"
        else
            echo -e "${BLUE}📁 File: /tmp/aqua_time_overlay.png${NC}"
            echo "   Apri manualmente per vedere il preview"
        fi
    else
        echo -e "${RED}❌ Errore generazione overlay${NC}"
        return 1
    fi
}

# Main execution
case "${1:-help}" in
    start)
        start_overlay
        ;;
    stop)
        stop_overlay
        ;;
    restart)
        restart_overlay
        ;;
    status)
        status_overlay
        ;;
    test)
        test_overlay
        ;;
    preview)
        preview_overlay
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}❌ Comando sconosciuto: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac 