#!/bin/bash
# 🧪 TEST CBR CONFIGURATION - SIMPLIFIED VERSION
# ==============================================
# Test focalizzato sui parametri CBR using existing audio stream

echo "🧪 TEST CBR SIMPLIFIED - PARAMETERS VALIDATION"
echo "=============================================="
echo "🎯 Target: Testare stabilità encoding CBR vs VBR"
echo "⏰ Durata: 3 minuti"
echo ""

# Configurazione
TEST_DURATION=180  # 3 minuti
LOG_FILE="/home/lofi/cbr_simple_test_$(date +%Y%m%d_%H%M%S).log"
OUTPUT_FILE="/home/lofi/cbr_test_$(date +%Y%m%d_%H%M%S).mp4"

echo "📊 PARAMETRI TEST CBR:"
echo "- Bitrate: 2500k (CBR) vs 1500k (VBR attuale)"
echo "- Preset: fast vs ultrafast"
echo "- Rate Control: CBR vs VBR"
echo "- Buffer: 5000k vs default"
echo "- Output: $OUTPUT_FILE"
echo "- Log: $LOG_FILE"
echo ""

# Test usando video di test generato + audio esistente se disponibile
echo "🎬 Generazione video test con parametri CBR..."

# Comando FFmpeg CBR ottimizzato per test
ffmpeg \
    -f lavfi -i testsrc2=duration=${TEST_DURATION}:size=1280x720:rate=24 \
    -f lavfi -i sine=frequency=440:duration=${TEST_DURATION} \
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
    -movflags +faststart \
    -y "$OUTPUT_FILE" \
    -loglevel info \
    -stats \
    2>&1 | tee "$LOG_FILE" &

TEST_PID=$!
echo "🎬 Test CBR avviato (PID: $TEST_PID)"

# Monitoring semplificato
{
    echo "⏰ START: $(date) - Test CBR Parameters"
    echo "📊 TARGET: Bitrate 2500k CBR, Preset fast, Buffer 5000k"
    
    # Monitor ogni 30 secondi per 3 minuti
    for i in {1..6}; do
        sleep 30
        
        # CPU usage del processo test
        if kill -0 $TEST_PID 2>/dev/null; then
            CPU_USAGE=$(ps -p $TEST_PID -o %cpu --no-headers)
            MEM_USAGE=$(ps -p $TEST_PID -o %mem --no-headers)
            echo "⏰ $(date): Check $i/6 - CPU: ${CPU_USAGE}% - MEM: ${MEM_USAGE}%"
        else
            echo "❌ $(date): Test process terminato"
            break
        fi
    done
    
} >> "$LOG_FILE" &

MONITOR_PID=$!

echo ""
echo "📈 MONITORING LIVE:"
echo "tail -f $LOG_FILE"
echo ""
echo "⚠️  Per fermare: kill $TEST_PID"

# Aspetta completamento
wait $TEST_PID
EXIT_CODE=$?

wait $MONITOR_PID

echo ""
echo "✅ TEST CBR COMPLETATO!"
echo "📊 Exit Code: $EXIT_CODE"
echo "📁 Output File: $OUTPUT_FILE"
echo "📋 Log File: $LOG_FILE"

# Analisi rapida risultati
if [ -f "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "📊 File generato: $FILE_SIZE"
    
    # Verifica bitrate effettivo con ffprobe se disponibile
    if command -v ffprobe >/dev/null 2>&1; then
        echo "🔍 Analisi bitrate effettivo:"
        ffprobe -v quiet -select_streams v:0 -show_entries stream=bit_rate -of csv=p=0 "$OUTPUT_FILE" 2>/dev/null || echo "Analisi non disponibile"
    fi
else
    echo "❌ File output non generato"
fi

echo ""
echo "🎯 PROSSIMO STEP: Analizzare $LOG_FILE per stabilità encoding" 