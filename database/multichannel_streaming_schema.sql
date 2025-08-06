-- =====================================================================
-- 🎵 MULTI-CHANNEL STREAMING DATABASE SCHEMA
-- =====================================================================
-- 
-- Schema completo per il sistema di streaming multi-channel:
-- - 5 Canali elementali (Aqua, Fuego, Aria, Tierra, Ether)
-- - 3 Programmi per canale con rotazione A→B→C
-- - Playlist versionate con rilascio manuale
-- - Tracce audio con nomenclatura programma_brano.mp3
-- 
-- Author: AI Assistant
-- Date: 17 Luglio 2025
-- Version: 1.0
-- Database: PostgreSQL Digital Ocean
-- =====================================================================

-- Tabella Canali di Streaming (5 canali elementali)
CREATE TABLE IF NOT EXISTS streaming_channels (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
    name VARCHAR NOT NULL,                    -- "Aqua Lofi Chill"
    emoji VARCHAR NOT NULL,                   -- "💦"
    element VARCHAR NOT NULL,                 -- "aqua", "fuego", "aria", "tierra", "ether"
    description TEXT,                         -- Descrizione del canale
    youtube_channel_id VARCHAR,              -- ID canale YouTube
    youtube_stream_key VARCHAR,              -- Chiave streaming YouTube
    is_active BOOLEAN DEFAULT TRUE,          -- Canale attivo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}'::json         -- Metadati aggiuntivi
);

-- Tabella Programmi di Streaming (3 per canale: A, B, C)
CREATE TABLE IF NOT EXISTS streaming_programs (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
    channel_id VARCHAR NOT NULL,             -- FK a streaming_channels
    name VARCHAR NOT NULL,                   -- "Abyss", "Blue Bossa", "Meditative Tide"
    code_name VARCHAR NOT NULL,              -- "abyss", "blue-bossa", "meditative-tide"
    program_letter VARCHAR NOT NULL,         -- "A", "B", "C"
    description TEXT,                        -- Descrizione programma
    order_in_rotation INTEGER NOT NULL,     -- 1, 2, 3
    is_active BOOLEAN DEFAULT TRUE,          -- Programma attivo
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}'::json         -- Metadati aggiuntivi
);

-- Tabella Playlist Versionate (una per program/version)
CREATE TABLE IF NOT EXISTS streaming_playlists (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
    program_id VARCHAR NOT NULL,             -- FK a streaming_programs
    version_name VARCHAR NOT NULL,           -- "20250720", "spring2025", "chillset1"
    folder_name VARCHAR NOT NULL,            -- Nome cartella filesystem
    is_active BOOLEAN DEFAULT FALSE,         -- Solo una attiva per programma
    video_path VARCHAR,                      -- "20250720/video/background.mp4"
    release_date TIMESTAMP,                 -- Data rilascio playlist
    total_tracks INTEGER DEFAULT 0,         -- Numero totale tracce
    total_duration INTEGER DEFAULT 0,       -- Durata totale in secondi
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}'::json         -- Metadati aggiuntivi
);

-- Tabella Tracce Audio (brani in playlist)
CREATE TABLE IF NOT EXISTS streaming_tracks (
    id VARCHAR PRIMARY KEY DEFAULT gen_random_uuid()::text,
    playlist_id VARCHAR NOT NULL,            -- FK a streaming_playlists
    filename VARCHAR NOT NULL,               -- "abyss_bluepulse.mp3"
    display_name VARCHAR,                    -- "Blue Pulse"
    order_in_playlist INTEGER NOT NULL,     -- Ordine nella playlist
    duration INTEGER,                       -- Durata in secondi
    file_path VARCHAR,                      -- Path completo nel server
    file_size INTEGER,                      -- Dimensione file in bytes
    is_active BOOLEAN DEFAULT TRUE,         -- Traccia attiva
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSON DEFAULT '{}'::json         -- Metadati aggiuntivi
);

-- =====================================================================
-- INDICI PER PERFORMANCE
-- =====================================================================

-- Indici per query veloci sui canali
CREATE INDEX IF NOT EXISTS idx_streaming_channels_element ON streaming_channels(element);
CREATE INDEX IF NOT EXISTS idx_streaming_channels_active ON streaming_channels(is_active);

-- Indici per programmi
CREATE INDEX IF NOT EXISTS idx_streaming_programs_channel ON streaming_programs(channel_id);
CREATE INDEX IF NOT EXISTS idx_streaming_programs_letter ON streaming_programs(program_letter);
CREATE INDEX IF NOT EXISTS idx_streaming_programs_rotation ON streaming_programs(order_in_rotation);
CREATE INDEX IF NOT EXISTS idx_streaming_programs_active ON streaming_programs(is_active);

-- Indici per playlist
CREATE INDEX IF NOT EXISTS idx_streaming_playlists_program ON streaming_playlists(program_id);
CREATE INDEX IF NOT EXISTS idx_streaming_playlists_active ON streaming_playlists(is_active);
CREATE INDEX IF NOT EXISTS idx_streaming_playlists_version ON streaming_playlists(version_name);

-- Indici per tracce
CREATE INDEX IF NOT EXISTS idx_streaming_tracks_playlist ON streaming_tracks(playlist_id);
CREATE INDEX IF NOT EXISTS idx_streaming_tracks_order ON streaming_tracks(order_in_playlist);
CREATE INDEX IF NOT EXISTS idx_streaming_tracks_active ON streaming_tracks(is_active);

-- =====================================================================
-- CONSTRAINTS E BUSINESS RULES
-- =====================================================================

-- Solo una playlist attiva per programma
CREATE UNIQUE INDEX IF NOT EXISTS idx_one_active_playlist_per_program 
ON streaming_playlists(program_id) 
WHERE is_active = TRUE;

-- Ogni programma deve avere lettera univoca per canale
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_program_letter_per_channel 
ON streaming_programs(channel_id, program_letter);

-- Ordine univoco nella rotazione per canale
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_rotation_order_per_channel 
ON streaming_programs(channel_id, order_in_rotation);

-- Elementi canale univoci
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_channel_element 
ON streaming_channels(element);

-- Filename univoco per playlist
CREATE UNIQUE INDEX IF NOT EXISTS idx_unique_filename_per_playlist 
ON streaming_tracks(playlist_id, filename);

-- =====================================================================
-- SETUP DATI INIZIALI - 5 CANALI ELEMENTALI
-- =====================================================================

-- Canale Aqua (Acqua)
INSERT INTO streaming_channels (name, emoji, element, description) VALUES 
('Aqua Lofi Chill', '💦', 'aqua', 'Water-themed lofi beats for deep meditation and flow states')
ON CONFLICT DO NOTHING;

-- Canale Fuego (Fuoco)
INSERT INTO streaming_channels (name, emoji, element, description) VALUES 
('Fuego Lofi Heat', '🔥', 'fuego', 'Fire-themed lofi beats with warm energy and passion')
ON CONFLICT DO NOTHING;

-- Canale Aria (Aria)
INSERT INTO streaming_channels (name, emoji, element, description) VALUES 
('Aria Lofi Flux', '🌬️', 'aria', 'Wind-themed lofi beats with airy lightness and movement')
ON CONFLICT DO NOTHING;

-- Canale Tierra (Terra)
INSERT INTO streaming_channels (name, emoji, element, description) VALUES 
('Tierra Lofi Grounding', '🌱', 'tierra', 'Earth-themed lofi beats for grounding and stability')
ON CONFLICT DO NOTHING;

-- Canale Ether (Etere)
INSERT INTO streaming_channels (name, emoji, element, description) VALUES 
('Ether Lofi Mind', '✨', 'ether', 'Meditative ethereal lofi for consciousness expansion')
ON CONFLICT DO NOTHING;

-- =====================================================================
-- SETUP PROGRAMMI PER OGNI CANALE (3 programmi ciascuno)
-- =====================================================================

-- Programmi Aqua (Acqua)
INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Abyss', 'abyss', 'A', 'Deep aquatic meditative soundscapes', 1
FROM streaming_channels WHERE element = 'aqua'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Blue Bossa', 'blue-bossa', 'B', 'Jazzy oceanic rhythms with smooth currents', 2
FROM streaming_channels WHERE element = 'aqua'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Meditative Tide', 'meditative-tide', 'C', 'Relaxed underwater mood for contemplation', 3
FROM streaming_channels WHERE element = 'aqua'
ON CONFLICT DO NOTHING;

-- Programmi Fuego (Fuoco)
INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Ember Glow', 'ember-glow', 'A', 'Warm crackling soundscapes with gentle fire', 1
FROM streaming_channels WHERE element = 'fuego'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Solar Flare', 'solar-flare', 'B', 'Energetic solar-powered rhythms', 2
FROM streaming_channels WHERE element = 'fuego'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Phoenix Rise', 'phoenix-rise', 'C', 'Transformative fire beats for renewal', 3
FROM streaming_channels WHERE element = 'fuego'
ON CONFLICT DO NOTHING;

-- Programmi Aria (Aria)
INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Zephyr Drift', 'zephyr-drift', 'A', 'Gentle wind currents and flowing melodies', 1
FROM streaming_channels WHERE element = 'aria'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Storm Breeze', 'storm-breeze', 'B', 'Dynamic air movements with atmospheric pressure', 2
FROM streaming_channels WHERE element = 'aria'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Cloud Walker', 'cloud-walker', 'C', 'Elevated soundscapes floating above the earth', 3
FROM streaming_channels WHERE element = 'aria'
ON CONFLICT DO NOTHING;

-- Programmi Tierra (Terra)
INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Root Deep', 'root-deep', 'A', 'Deep earth connections and foundational rhythms', 1
FROM streaming_channels WHERE element = 'tierra'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Forest Floor', 'forest-floor', 'B', 'Organic textures and natural growth patterns', 2
FROM streaming_channels WHERE element = 'tierra'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Mountain Stone', 'mountain-stone', 'C', 'Solid, enduring beats with mineral clarity', 3
FROM streaming_channels WHERE element = 'tierra'
ON CONFLICT DO NOTHING;

-- Programmi Ether (Etere)
INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Void Space', 'void-space', 'A', 'Spacious soundscapes beyond physical reality', 1
FROM streaming_channels WHERE element = 'ether'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Astral Shift', 'astral-shift', 'B', 'Consciousness-altering frequencies and dimensions', 2
FROM streaming_channels WHERE element = 'ether'
ON CONFLICT DO NOTHING;

INSERT INTO streaming_programs (channel_id, name, code_name, program_letter, description, order_in_rotation)
SELECT id, 'Divine Flow', 'divine-flow', 'C', 'Transcendent beats connecting to universal energy', 3
FROM streaming_channels WHERE element = 'ether'
ON CONFLICT DO NOTHING;

-- =====================================================================
-- QUERY UTILI PER GESTIONE STREAMING
-- =====================================================================

-- Query per ottenere tutti i canali con i loro programmi
/*
SELECT 
    c.name as channel_name,
    c.emoji,
    c.element,
    p.program_letter,
    p.name as program_name,
    p.code_name,
    p.order_in_rotation
FROM streaming_channels c
LEFT JOIN streaming_programs p ON c.id = p.channel_id
ORDER BY c.element, p.order_in_rotation;
*/

-- Query per ottenere le playlist attive per canale
/*
SELECT 
    c.name as channel_name,
    p.name as program_name,
    pl.version_name,
    pl.folder_name,
    pl.total_tracks,
    pl.total_duration
FROM streaming_channels c
JOIN streaming_programs p ON c.id = p.channel_id
JOIN streaming_playlists pl ON p.id = pl.program_id
WHERE pl.is_active = TRUE
ORDER BY c.element, p.order_in_rotation;
*/

-- Query per ottenere il prossimo programma nella rotazione
/*
SELECT 
    c.name as channel_name,
    p.name as current_program,
    p_next.name as next_program
FROM streaming_channels c
JOIN streaming_programs p ON c.id = p.channel_id
JOIN streaming_programs p_next ON c.id = p_next.channel_id
WHERE p.order_in_rotation = 1 -- Programma corrente
AND p_next.order_in_rotation = CASE 
    WHEN p.order_in_rotation = 3 THEN 1 
    ELSE p.order_in_rotation + 1 
END;
*/

-- =====================================================================
-- TRIGGERS PER BUSINESS LOGIC (Opzionali)
-- =====================================================================

-- Trigger per aggiornare total_tracks quando si aggiungono tracce
/*
CREATE OR REPLACE FUNCTION update_playlist_track_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE streaming_playlists 
    SET total_tracks = (
        SELECT COUNT(*) 
        FROM streaming_tracks 
        WHERE playlist_id = NEW.playlist_id 
        AND is_active = TRUE
    )
    WHERE id = NEW.playlist_id;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_track_count
    AFTER INSERT OR UPDATE OR DELETE ON streaming_tracks
    FOR EACH ROW
    EXECUTE FUNCTION update_playlist_track_count();
*/

-- =====================================================================
-- VIEWS UTILI PER L'APPLICAZIONE
-- =====================================================================

-- View per canali con conteggi
CREATE OR REPLACE VIEW v_channels_with_stats AS
SELECT 
    c.id,
    c.name,
    c.emoji,
    c.element,
    c.description,
    c.is_active,
    COUNT(p.id) as total_programs,
    COUNT(pl.id) as total_playlists,
    COUNT(CASE WHEN pl.is_active THEN 1 END) as active_playlists
FROM streaming_channels c
LEFT JOIN streaming_programs p ON c.id = p.channel_id
LEFT JOIN streaming_playlists pl ON p.id = pl.program_id
GROUP BY c.id, c.name, c.emoji, c.element, c.description, c.is_active;

-- View per rotazione programmi
CREATE OR REPLACE VIEW v_program_rotation AS
SELECT 
    c.element as channel_element,
    c.name as channel_name,
    p.program_letter,
    p.name as program_name,
    p.code_name,
    p.order_in_rotation,
    CASE 
        WHEN p.order_in_rotation = 3 THEN 1
        ELSE p.order_in_rotation + 1
    END as next_rotation_order
FROM streaming_channels c
JOIN streaming_programs p ON c.id = p.channel_id
WHERE c.is_active = TRUE AND p.is_active = TRUE
ORDER BY c.element, p.order_in_rotation;

-- =====================================================================
-- COMPLETED SCHEMA SETUP
-- =====================================================================

-- Riepilogo dello schema creato
SELECT 
    'SCHEMA SETUP COMPLETED' as status,
    (SELECT COUNT(*) FROM streaming_channels) as channels_created,
    (SELECT COUNT(*) FROM streaming_programs) as programs_created,
    NOW() as setup_timestamp; 