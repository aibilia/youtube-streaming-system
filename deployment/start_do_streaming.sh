#!/bin/bash

# 🎵 Avvio Streaming su Server Digital Ocean
echo "🚀 Avvio streaming YouTube 24/7 su server DO..."

# Connessione al server e avvio streaming in background
ssh -o ConnectTimeout=10 -o ServerAliveInterval=30 root@159.89.106.38 << 'EOSSH'
cd /home/lofi

# Termina eventuali processi FFmpeg esistenti
pkill -f ffmpeg || true
sleep 2

# Avvia streaming in background con nohup
nohup python3 start_aqua_channel_streaming_optimized.py > streaming.log 2>&1 &

echo "✅ Streaming avviato in background"
echo "📋 PID del processo: $!"
echo "📊 Per monitorare: tail -f /home/lofi/streaming.log"

# Aspetta qualche secondo e mostra status
sleep 5
ps aux | grep ffmpeg | grep -v grep || echo "⏳ FFmpeg non ancora avviato..."

EOSSH

echo "🎬 Comando streaming inviato al server DO"
echo "🔍 Verifica stato tra 10 secondi..." 