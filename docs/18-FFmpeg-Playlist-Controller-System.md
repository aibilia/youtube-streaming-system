# 🎵 FFMPEG PLAYLIST CONTROLLER SYSTEM

**Data implementazione**: 22 Gennaio 2025  
**Status**: ✅ IMPLEMENTATO  
**Architettura**: FFmpeg Concat + Web UI + OBS Integration  

---

## 📋 **PANORAMICA SISTEMA**

Il **FFmpeg Playlist Controller** è un sistema avanzato per gestione playlist audio con controllo ordine live tramite Web UI, progettato per sostituire il sistema di rotazione manuale delle tracce.

### 🏗️ **ARCHITETTURA**

```
🎵 FFmpeg Concat Protocol          🌐 Web UI Controller
├── Normalizzazione audio          ├── Dashboard in tempo reale
├── File concat ottimizzato         ├── Controllo ordine live  
├── Stream continuo WAV             ├── Start/Stop stream
└── Loop infinito                   └── Monitoraggio log

                    ⬇️
            🎥 OBS Media Source
            ├── /tmp/obs_audio_stream.wav
            ├── Loop enabled
            └── Restart on activate
```

### ✅ **FUNZIONALITÀ PRINCIPALI**

- **🎵 Playlist Continua**: Stream audio senza interruzioni tra tracce
- **🎚️ Controllo Ordine Live**: Cambio ordine senza fermare stream
- **🌐 Web UI**: Interfaccia web moderna per controllo remoto
- **🔧 Normalizzazione Audio**: Processing automatico per compatibilità
- **📊 Monitoraggio**: Dashboard con stato real-time
- **🔄 Integrazione OBS**: Configurazione automatica source

---

## 🚀 **INSTALLAZIONE E SETUP**

### **1. 📦 Installazione Automatica**

```bash
# Sul server streaming
cd /home/lofi
./scripts/streaming/install_ffmpeg_playlist.sh
```

### **2. 🎯 Avvio Rapido**

```bash
# Sistema completo (Controller + UI)
./scripts/streaming/streaming_control.sh playlist-full

# Solo controller FFmpeg
./scripts/streaming/streaming_control.sh ffmpeg-start

# Solo Web UI
./scripts/streaming/streaming_control.sh ui-start
```

### **3. 🌐 Accesso Web UI**

- **Locale**: `http://localhost:5000`
- **Remoto**: `http://IP_SERVER:5000`
- **Mobile**: Responsive design

---

## 🎛️ **CONTROLLI DISPONIBILI**

### **🎚️ Ordini Playlist**

| Ordine | Descrizione | Comando CLI |
|--------|-------------|-------------|
| **📋 Sequenziale** | Ordine originale playlist | `sequential` |
| **🎲 Casuale** | Shuffle completo | `random` |
| **🌊 Abyss Prima** | Tutti Abyss Deep, poi Meditative | `abyss_first` |
| **🧘 Meditative Prima** | Tutti Meditative, poi Abyss | `meditative_first` |
| **🔄 Alternato** | Abyss/Meditative alternati | `alternate` |

### **📋 Comandi CLI**

```bash
# Controller FFmpeg
./streaming_control.sh ffmpeg-start       # Avvia controller
./streaming_control.sh ffmpeg-stop        # Ferma controller  
./streaming_control.sh ffmpeg-status      # Stato controller
./streaming_control.sh ffmpeg-order random # Cambia ordine

# Web UI
./streaming_control.sh ui-start           # Avvia UI
./streaming_control.sh ui-stop            # Ferma UI

# Sistema completo
./streaming_control.sh playlist-full      # Avvia tutto
```

---

## 🔧 **COMPONENTI TECNICI**

### **1. 🎵 FFmpeg Playlist Controller**
**File**: `scripts/streaming/ffmpeg_playlist_controller.py`

**Funzionalità:**
- ✅ **Normalizzazione Audio**: Sample rate 44.1kHz, bitrate 128k, stereo
- ✅ **File Concat**: Gestione lista file FFmpeg ottimizzata  
- ✅ **Stream Continuo**: Output WAV per OBS
- ✅ **Controllo Ordine**: 5 modalità di ordinamento
- ✅ **Persistenza Stato**: JSON state file
- ✅ **Logging Avanzato**: Log dettagliati per debugging

**Comando FFmpeg Generato:**
```bash
ffmpeg -f concat -safe 0 -stream_loop -1 \
  -i /home/lofi/media/aqua/playlists/ffmpeg_concat.txt \
  -acodec pcm_s16le -ar 44100 -ac 2 \
  -af 'pan=stereo|c0=0.5*c0+0.5*c1|c1=0.5*c0+0.5*c1' \
  -f wav -y /tmp/obs_audio_stream.wav
```

### **2. 🌐 Web UI Server**
**File**: `scripts/streaming/playlist_ui_server.py`

**API Endpoints:**
- `GET /api/status` - Stato sistema
- `POST /api/change_order` - Cambio ordine
- `POST /api/start_stream` - Avvia stream
- `POST /api/stop_stream` - Ferma stream  
- `GET /api/playlist_files` - Lista file
- `GET /api/logs` - Log recenti

**Tecnologie:**
- **Framework**: Flask
- **Frontend**: HTML5 + CSS3 + Vanilla JS
- **Design**: Responsive, gradients moderni
- **Update**: Real-time ogni 5 secondi

### **3. 🎨 Web UI Template**
**File**: `scripts/streaming/templates/playlist_ui.html`

**Sezioni:**
- **📊 Dashboard**: Stato streaming in tempo reale
- **🎛️ Controlli Stream**: Start/Stop con feedback
- **🎚️ Controllo Ordine**: 5 bottoni per ordinamento
- **📁 Lista File**: Visualizzazione tracce per categoria
- **📋 Log Sistema**: Monitoring live degli eventi

---

## 🎯 **CONFIGURAZIONE OBS**

### **📋 Setup Media Source**

1. **Aggiungi Source**: Media Source
2. **Nome**: "FFmpeg Audio Stream"  
3. **Local File**: `/tmp/obs_audio_stream.wav`
4. **Configurazione**:
   - ✅ **Loop**: Enabled
   - ✅ **Restart when source becomes active**: Enabled
   - ❌ **Close file when inactive**: Disabled
   - ✅ **Show nothing when playback ends**: Disabled

### **🔧 Impostazioni Avanzate**

```json
{
  "local_file": "/tmp/obs_audio_stream.wav",
  "is_local_file": true,
  "looping": true,
  "restart_on_activate": true,
  "close_when_inactive": false,
  "show_nothing_when_playback_ends": false,
  "speed_percent": 100,
  "hw_decode": false
}
```

---

## 📊 **VANTAGGI vs SISTEMA PRECEDENTE**

| Aspetto | Sistema Precedente | FFmpeg Controller |
|---------|-------------------|-------------------|
| **Continuità Audio** | ❌ Gap tra tracce | ✅ Stream continuo |
| **Controllo Ordine** | ❌ Solo sequenziale | ✅ 5 modalità ordine |
| **Controllo Live** | ❌ Restart richiesto | ✅ Cambio live |
| **Interface** | ❌ Solo CLI | ✅ Web UI moderna |
| **Normalizzazione** | ❌ Manuale | ✅ Automatica |
| **Monitoraggio** | ❌ Log file only | ✅ Dashboard real-time |
| **Scalabilità** | ❌ Script singolo | ✅ Architettura modulare |

---

## 🗂️ **FILE STRUCTURE**

```
scripts/streaming/
├── ffmpeg_playlist_controller.py     # Controller principale
├── playlist_ui_server.py             # Server Web UI
├── templates/
│   └── playlist_ui.html              # Template UI
├── install_ffmpeg_playlist.sh        # Script installazione
└── streaming_control.sh              # Comandi integrati

/home/lofi/media/aqua/
├── playlists/
│   ├── unified_playlist.txt          # Playlist originale
│   ├── ffmpeg_concat.txt             # File concat generato
│   └── playlist_state.json           # Stato sistema
└── audio/
    └── normalized/                   # File normalizzati
        ├── norm_abyss_deep_01.mp3
        └── norm_meditative_tide_01.mp3

/tmp/
└── obs_audio_stream.wav              # Output per OBS
```

---

## 📋 **MONITORING E LOG**

### **🗂️ File di Log**

| File | Contenuto | Posizione |
|------|-----------|-----------|
| `ffmpeg_playlist.log` | Controller principale | `/home/lofi/` |
| `playlist_ui.log` | Web UI server | `/home/lofi/` |
| `playlist_controller.log` | Log dettagliato | `/home/lofi/media/aqua/` |

### **📊 Stato Sistema**

**Comando CLI:**
```bash
./streaming_control.sh ffmpeg-status
```

**Output Esempio:**
```
📊 STATO FFMPEG PLAYLIST
========================
✅ Controller: ATTIVO (PID: 12345)
✅ Stream: ATTIVO (PID: 12346)  
✅ Output file: /tmp/obs_audio_stream.wav (45MB)

📋 Stato playlist:
   Ordine: random
   Tracce: 56
   Ultimo aggiornamento: 2025-01-22 15:30:45
```

---

## 🚨 **TROUBLESHOOTING**

### **❌ Problemi Comuni**

#### **1. Stream Non Si Avvia**
```bash
# Check dipendenze
ffmpeg -version
python3 --version

# Check file playlist
cat /home/lofi/media/aqua/playlists/unified_playlist.txt

# Check log errori
tail -f /home/lofi/ffmpeg_playlist.log
```

#### **2. Audio Distorto o Rumoroso**
```bash
# Re-normalizza audio files
rm -rf /home/lofi/media/aqua/audio/normalized/*
./streaming_control.sh ffmpeg-start
```

#### **3. Web UI Non Accessibile**
```bash
# Check porta 5000
netstat -tuln | grep :5000

# Check Flask installation
python3 -c "import flask; print(flask.__version__)"

# Restart UI
./streaming_control.sh ui-stop
./streaming_control.sh ui-start
```

#### **4. OBS Non Riceve Audio**
```bash
# Check output file
ls -la /tmp/obs_audio_stream.wav

# Test audio file
ffplay /tmp/obs_audio_stream.wav

# Restart OBS source
# In OBS: Right-click source → Restart
```

### **🔧 Reset Completo**

```bash
# Ferma tutto
./streaming_control.sh ffmpeg-stop
./streaming_control.sh ui-stop

# Pulisci file temporanei
rm -f /tmp/obs_audio_stream.wav
rm -rf /home/lofi/media/aqua/audio/normalized/*
rm -f /home/lofi/media/aqua/playlists/playlist_state.json

# Riavvia sistema
./streaming_control.sh playlist-full
```

---

## 🎯 **UTILIZZO OPERATIVO**

### **📅 Workflow Giornaliero**

1. **🚀 Avvio Sistema**:
   ```bash
   ./streaming_control.sh playlist-full
   ```

2. **🌐 Accesso UI**: Apri browser su `http://IP_SERVER:5000`

3. **🎚️ Controllo Ordine**: Clicca bottoni per cambiare ordine playlist

4. **📊 Monitoraggio**: Dashboard mostra stato in tempo reale

5. **⏹️ Spegnimento**:
   ```bash
   ./streaming_control.sh ffmpeg-stop
   ./streaming_control.sh ui-stop
   ```

### **🎵 Gestione Playlist**

- **Sequenziale**: Ordine originale per streaming normale
- **Casuale**: Shuffle per varietà  
- **Abyss Prima**: Focus su musica deep
- **Meditative Prima**: Focus su musica meditativa
- **Alternato**: Mix bilanciato tra categorie

---

## 🎉 **CONCLUSIONI**

Il **FFmpeg Playlist Controller** rappresenta un'evoluzione significativa del sistema di gestione audio per streaming, offrendo:

- ✅ **Controllo Completo**: Ordine playlist modificabile live
- ✅ **Stream Continuo**: Eliminazione gap tra tracce
- ✅ **Interface Moderna**: Web UI responsive e intuitiva  
- ✅ **Architettura Robusta**: Sistema modulare e scalabile
- ✅ **Integrazione OBS**: Setup semplificato e automatico

Il sistema è **production-ready** e pronto per sostituire completamente il sistema di rotazione manuale precedente.

**🎵 Buon streaming con Aqua Lofi Chill!** 

## 🎉 **IMPLEMENTATION SUCCESS REPORT**

### **✅ DATA IMPLEMENTAZIONE: 20 Gennaio 2025**
**Server**: Ubuntu 159.89.106.38 (DigitalOcean)  
**Status**: ✅ **OPERATIVO AL 100%**

#### **🚨 Problema Identificato e Risolto**

**Sintomi Iniziali:**
- ❌ UI web non accessibile su porta 5000
- ❌ Flask installato ma non funzionante  
- ❌ Errori di installazione dipendenze

**🔍 Diagnosi:**
```bash
# CAUSA ROOT: Disco pieno
tmpfs    2.0G  2.0G     0 100% /tmp  ← 100% PIENO!
/home/lofi/obs_audio_stream.wav: 5.8GB  ← COLPEVOLE PRINCIPALE
```

**🛠️ Soluzione Implementata:**
1. **Pulizia Spazio Disco**: Rimosso `obs_audio_stream.wav` (5.8GB)
2. **Pulizia /tmp**: Liberato spazio temporaneo da 100% a 1%
3. **Attivazione Sistema**: `./scripts/streaming/streaming_control.sh playlist-full`

#### **✅ Risultato Finale**

**Sistema Operativo:**
- ✅ **FFmpeg Controller**: PID 412542 - ATTIVO
- ✅ **Web UI Server**: PID 412556 - ATTIVO  
- ✅ **Porta 5000**: 0.0.0.0:5000 - ASCOLTA
- ✅ **Accesso UI**: http://159.89.106.38:5000 - FUNZIONANTE

**Test di Verifica:**
```bash
# Test accessibilità
curl -s http://localhost:5000 | head -5
# ✅ Risultato: HTML valido ricevuto

curl -s http://159.89.106.38:5000 | head -5  
# ✅ Risultato: HTML valido ricevuto
```

### **🔧 Maintenance Recommendations**

#### **Monitoraggio Spazio Disco:**
```bash
# Check quotidiano spazio /tmp
df -h /tmp | grep -v Filesystem

# Rimozione automatica file grandi in /tmp
find /tmp -name "obs_audio_stream.wav" -size +1G -delete
```

#### **Health Check Script:**
```bash
#!/bin/bash
# /home/lofi/health_check_ui.sh
echo "🔍 UI Health Check - $(date)"
echo "================================"

# Check processi
ps aux | grep -E "(ffmpeg_playlist_controller|playlist_ui_server)" | grep -v grep

# Check porta 5000
ss -tuln | grep :5000

# Test accessibilità
curl -s http://localhost:5000/api/status || echo "❌ UI non raggiungibile"
```

---

## 🚨 **CRITICAL ISSUE: YouTube Buffering Problem**

### **⚠️ Problema Identificato**
```
Errore YouTube: "YouTube is not receiving enough video to maintain smooth streaming. 
As such, viewers will experience buffering."
```

**Caratteristiche:**
- ❌ Buffering lato YouTube nonostante stream locale stabile
- ❌ Problema intermittente ma persistente
- ✅ Nessun buffering locale o errori client-side

### **🔍 Possibili Cause Tecniche**

#### **1. Bitrate Inconsistency**
- **Stream variabile**: FFmpeg output bitrate non consistente
- **Target YouTube**: 1500-2500 kbps stabili richiesti
- **Buffer YouTube**: Richiede flusso costante senza drop

#### **2. Keyframe Intervals**
- **Problema**: Keyframe spacing irregolare
- **YouTube requirement**: Keyframe ogni 2-4 secondi max
- **FFmpeg setting**: `-g 60` (per 30fps = 2s keyframe interval)

#### **3. Network Quality Issues**
- **Upload instability**: Connessione server → YouTube instabile
- **Packet loss**: Perdita pacchetti durante upload
- **Latency spikes**: Picchi latenza che causano buffer starvation

---

## 🎯 **NEXT STEPS: Alternative Playlist Solutions**

Il problema YouTube buffering suggerisce la necessità di **soluzioni playlist alternative** più robuste per streaming production.

**🎵 Buon streaming con Aqua Lofi Chill!** 