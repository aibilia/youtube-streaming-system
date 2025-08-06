# 🎵 AQUA LOFI CHILL - ISTRUZIONI UPLOAD YOUTUBE
# ===============================================

## 📋 STATO ATTUALE
- ✅ **Video creati**: 3 video completati e pronti
- ✅ **Script preparato**: Script di upload configurato
- ✅ **Ambiente virtuale**: youtube-upload installato
- ❌ **Credenziali**: Mancano le credenziali YouTube

## 🎬 VIDEO PRONTI PER UPLOAD

### 1. Blue Bossa Session 1
- **File**: `Blue_Bossa_Session_1_2025-07-24.mp4` (41MB)
- **Titolo**: "Blue Bossa Lofi Jazz Session - Study Music & Relaxation Focus"
- **Descrizione**: Jazz lofi con chitarra acustica per studio e relax
- **Tag**: lofi, studymusic, relaxation, focus, jazz, chill, ambient, meditation, productivity

### 2. Meditative Tide Session 1
- **File**: `Meditative_Tide_Session_1_2025-07-24.mp4` (44MB)
- **Titolo**: "Meditative Tide Lofi Ocean Session - Meditation & Deep Focus Music"
- **Descrizione**: Ambient oceanico con onde per meditazione
- **Tag**: lofi, meditation, focus, ocean, ambient, relaxation, studymusic, chill, peace

### 3. Abyss Deep Session 1
- **File**: `Abyss_Deep_Session_1_2025-07-24.mp4` (20MB)
- **Titolo**: "Abyss Deep Lofi Ambient Session - Deep Focus & Contemplation Music"
- **Descrizione**: Deep ambient sottomarino per contemplazione
- **Tag**: lofi, deepfocus, ambient, meditation, relaxation, studymusic, chill, deep, ocean

## 📁 PLAYLIST DA CREARE

### 🎸 Blue Bossa Collection
- **Titolo**: "Blue Bossa Collection - Jazz Lofi Sessions"
- **Contenuto**: Sessioni jazz lofi con chitarra acustica

### 🌊 Meditative Tide Collection
- **Titolo**: "Meditative Tide Collection - Ocean Lofi Sessions"
- **Contenuto**: Sessioni ambient oceaniche per meditazione

### 🌌 Abyss Deep Collection
- **Titolo**: "Abyss Deep Collection - Deep Ambient Sessions"
- **Contenuto**: Sessioni deep ambient sottomarine per contemplazione

## 🔐 SETUP CREDENZIALI YOUTUBE

### Passo 1: Creare Progetto Google Cloud
1. Vai su [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuovo progetto o seleziona uno esistente
3. Abilita l'API YouTube Data v3

### Passo 2: Creare Credenziali OAuth2
1. Vai su "APIs & Services" > "Credentials"
2. Clicca "Create Credentials" > "OAuth 2.0 Client IDs"
3. Seleziona "Desktop application"
4. Scarica il file JSON delle credenziali

### Passo 3: Configurare sul Server
```bash
# Copia il file client_secrets.json sul server
scp client_secrets.json root@159.89.106.38:/root/.client_secrets.json

# Oppure crea il file direttamente sul server
ssh root@159.89.106.38
nano /root/.client_secrets.json
# Incolla il contenuto del file JSON scaricato
```

### Passo 4: Autenticazione Iniziale
```bash
# Prima volta: esegui l'autenticazione
ssh root@159.89.106.38
source /home/lofi/youtube_env/bin/activate
youtube-upload --title="Test" --description="Test" /tmp/test.mp4
# Segui le istruzioni per l'autenticazione nel browser
```

## 🚀 UPLOAD AUTOMATICO

Una volta configurate le credenziali:

```bash
# Esegui l'upload completo
python3 scripts/upload_to_aqua_lofi_chill.py
```

### Processo Automatico:
1. **Creazione Playlist**: Crea le 3 playlist sul canale
2. **Upload Video**: Carica i 3 video con metadati completi
3. **Assegnazione Playlist**: Ogni video viene aggiunto alla sua playlist

## 📊 RISULTATO FINALE

Il canale **Aqua Lofi Chill** avrà:
- ✅ 3 video di alta qualità
- ✅ 3 playlist organizzate per tema
- ✅ Contenuti ottimizzati per studio, lavoro e meditazione
- ✅ Branding coerente e professionale
- ✅ Tag SEO ottimizzati per visibilità

## 🎯 OBIETTIVI RAGGIUNTI

- ✅ **Popolamento canale**: Da vuoto a 3 video di qualità
- ✅ **Organizzazione**: Playlist tematiche per ogni programma
- ✅ **SEO**: Titoli e tag ottimizzati per studio, relax, focus
- ✅ **Branding**: Identità "Aqua Lofi Chill" coerente
- ✅ **Automazione**: Script pronto per futuri upload

## 📝 NOTE TECNICHE

### File di Credenziali
- **Posizione**: `/root/.client_secrets.json`
- **Formato**: JSON con credenziali OAuth2
- **Permessi**: 600 (solo root)

### Ambiente Virtuale
- **Posizione**: `/home/lofi/youtube_env/`
- **Attivazione**: `source /home/lofi/youtube_env/bin/activate`
- **Pacchetti**: youtube-upload, google-api-python-client, oauth2client

### Video Pronti
- **Posizione**: `/home/lofi/media/aqua/youtube_videos/`
- **Formato**: MP4 con audio AAC e video H.264
- **Qualità**: Alta qualità per YouTube

---
**Status**: Ready for Credentials Setup  
**Next Step**: Configure YouTube OAuth2 credentials  
**Estimated Time**: 15-30 minutes for setup 