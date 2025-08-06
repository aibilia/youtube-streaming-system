#!/bin/bash

# 🎵 Avvio Streaming Singolo e Stabile su Server DO
echo "🚀 Avvio streaming YouTube SINGOLO su server DO..."

# Connessione al server con pulizia completa
ssh -o ConnectTimeout=10 -o ServerAliveInterval=30 root@159.89.106.38 << 'EOSSH'
cd /home/lofi

echo "🧹 Pulizia processi esistenti..."
# Kill tutti i processi streaming esistenti
pkill -f "start_aqua_channel_streaming" || true
pkill -f ffmpeg || true
sleep 3

echo "🔍 Verifica pulizia..."
ps aux | grep -E "ffmpeg|start_aqua" | grep -v grep || echo "✅ Nessun processo attivo"

echo "🎬 Avvio streaming singolo..."
# Avvia UN SOLO streaming in background con log dettagliato
nohup python3 start_aqua_channel_streaming_optimized.py > streaming_single.log 2>&1 &
NEW_PID=$!

echo "✅ Streaming singolo avviato"
echo "📋 PID: $NEW_PID"
echo "📊 Log: tail -f /home/lofi/streaming_single.log"

# Aspetta 10 secondi e verifica
sleep 10
echo "🔍 Verifica stato dopo 10 secondi:"
ps aux | grep ffmpeg | grep -v grep | wc -l | xargs echo "FFmpeg processi attivi:"
lsof -i :1935 2>/dev/null | grep ffmpeg | wc -l | xargs echo "Connessioni RTMP:"

EOSSH

echo "🎬 Streaming singolo configurato sul server DO" 