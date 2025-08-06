#!/bin/bash
# YOUTUBE UPLOAD SCRIPT - 2025-07-24
# ======================================

echo "📤 UPLOAD VIDEO YOUTUBE"
echo "======================"

# Configurazione
VIDEO_DIR="/home/lofi/media/aqua/youtube_videos"
METADATA_DIR="/home/lofi/media/aqua/youtube_metadata"

# Upload Blue Bossa
echo "🎸 Upload Blue Bossa..."
youtube-upload \
    --title="Blue Bossa, Session 1, 2025-07-24" \
    --description="$(cat $METADATA_DIR/blue_bossa_metadata.txt)" \
    --category="Music" \
    --tags="jazzlofi,bluesbossa,chitarra,relax,studymusic,workmusic,lofi,jazz,chill,ambient,meditation,focus,productivity,calm,peaceful,instrumental,acoustic,guitar,beach,sunset,zen" \
    --playlist="Blue Bossa - Jazz Lofi Sessions" \
    "$VIDEO_DIR/Blue_Bossa_Session_1_2025-07-24.mp4"

# Upload Meditative Tide  
echo "🌊 Upload Meditative Tide..."
youtube-upload \
    --title="Meditative Tide, Session 1, 2025-07-24" \
    --description="$(cat $METADATA_DIR/meditative_tide_metadata.txt)" \
    --category="Music" \
    --tags="oceanlofi,meditativetide,waves,meditation,ambient,relax,studymusic,workmusic,lofi,chill,ocean,peace,calm,zen,meditationmusic,focus,productivity,nature,water,flow,tranquility,serenity,mindfulness" \
    --playlist="Meditative Tide - Ocean Lofi Sessions" \
    "$VIDEO_DIR/Meditative_Tide_Session_1_2025-07-24.mp4"

# Upload Abyss Deep
echo "🌌 Upload Abyss Deep..."
youtube-upload \
    --title="Abyss Deep, Session 1, 2025-07-24" \
    --description="$(cat $METADATA_DIR/abyss_deep_metadata.txt)" \
    --category="Music" \
    --tags="deepambient,abyssdeep,underwater,ambient,meditation,relax,studymusic,workmusic,lofi,chill,deep,ocean,peace,calm,zen,meditationmusic,focus,productivity,nature,water,depth,tranquility,serenity,mindfulness,submarine,abyss" \
    --playlist="Abyss Deep - Deep Ambient Sessions" \
    "$VIDEO_DIR/Abyss_Deep_Session_1_2025-07-24.mp4"

echo "✅ Upload completato!"
