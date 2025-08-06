#!/bin/bash
# 🧪 TEST CBR STREAMING CONFIGURATION
# ===================================
# Script per testare configurazione CBR ottimizzata in parallelo
# Durata test: 10 minuti
# Target: Validare stabilità bitrate e performance

echo "🧪 AVVIO TEST CBR STREAMING CONFIGURATION"
echo "========================================"
echo "⏰ Test Duration: 10 minuti"
echo "🎯 Target: Validare stabilità CBR vs VBR attuale"
echo ""

# Configurazione test
TEST_DURATION=600  # 10 minuti
LOG_FILE="/home/lofi/cbr_test_$(date +%Y%m%d_%H%M%S).log"
AUDIO_INPUT="/tmp/obs_audio_stream.wav"  # Audio dal sistema FFmpeg attuale

echo "📊 PARAMETRI TEST CBR:"
echo "- Bitrate: 2500k (CBR)"
echo "- Preset: fast"
echo "- Keyframe: 48 (2s @ 24fps)"
echo "- Buffer: 5000k"
echo "- Audio Input: $AUDIO_INPUT"
echo "- Log File: $LOG_FILE"
echo ""

# Verifica audio input disponibile
if [ ! -f "$AUDIO_INPUT" ]; then
    echo "❌ ERRORE: Audio input non trovato: $AUDIO_INPUT"
    echo "💡 Verifica che il sistema FFmpeg sia attivo"
    exit 1
fi

echo "✅ Audio input verificato"
echo "🚀 Avvio test streaming CBR..."
echo ""

# Comando FFmpeg CBR ottimizzato per test
# NOTA: Usa stream key di test o URL di test per non interferire con stream live
ffmpeg \
    -f pulse -i default \
    -f x11grab -s 1280x720 -r 24 -i :0.0 \
    \
    -c:v libx264 \
    -preset fast \
    -tune zerolatency \
    -profile:v high \
    -level 4.0 \
    \
    -b:v 2500k \
    -minrate 2500k \
    -maxrate 2500k \
    -bufsize 5000k \
    \
    -g 48 \
    -keyint_min 24 \
    -sc_threshold 0 \
    \
    -c:a aac \
    -b:a 128k \
    -ar 44100 \
    -ac 2 \
    \
    -f flv \
    -loglevel verbose \
    -stats \
    -t $TEST_DURATION \
    /home/lofi/cbr_test_output_$(date +%Y%m%d_%H%M%S).flv \
    2>&1 | tee "$LOG_FILE" &

TEST_PID=$!
echo "🎬 Test streaming avviato (PID: $TEST_PID)"
echo "📊 Monitoring per $TEST_DURATION secondi..."

# Monitoring script parallelo
{
    echo "⏰ $(date): Test CBR avviato"
    
    for i in $(seq 1 10); do
        sleep 60  # Ogni minuto
        
        # Statistiche CPU e memoria
        CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | awk -F'%' '{print $1}')
        MEMORY=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
        
        # Network usage
        NETWORK=$(ss -tuln | grep :1935 | wc -l)
        
        echo "⏰ $(date): Minuto $i/10 - CPU: ${CPU}% - RAM: ${MEMORY}% - Network: $NETWORK"
        
        # Verifica se il processo è ancora attivo
        if ! kill -0 $TEST_PID 2>/dev/null; then
            echo "❌ Test process terminato inaspettatamente"
            break
        fi
    done
    
    echo "⏰ $(date): Test completato"
} >> "$LOG_FILE" &

MONITOR_PID=$!

echo ""
echo "📈 COMANDI MONITORING LIVE:"
echo "- tail -f $LOG_FILE"
echo "- ps aux | grep $TEST_PID"
echo "- htop"
echo ""
echo "⚠️  Per fermare il test: kill $TEST_PID"
echo "📊 Al termine, analizzare $LOG_FILE per metriche"

# Attendi completamento test
wait $TEST_PID
wait $MONITOR_PID

echo ""
echo "✅ TEST CBR COMPLETATO!"
echo "📊 Log disponibile: $LOG_FILE"
echo "🔍 Analizzare stability metrics nel log file" 