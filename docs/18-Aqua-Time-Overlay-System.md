# 🎨 AQUA TIME OVERLAY SYSTEM

## 📋 PANORAMICA

Il **Sistema Overlay Temporale Aqua Lofi** fornisce informazioni live sul palinsesto direttamente nel video streaming, mostrando:
- **Programma corrente** in riproduzione
- **Tempo rimanente** nel programma corrente
- **Prossimo programma** in coda
- **Orario corrente**

## 🎯 CARATTERISTICHE

### **📍 Posizionamento**
- **Posizione**: Basso a sinistra (allineato con il logo)
- **Margini**: 30px dal bordo sinistro, 30px dal bordo inferiore
- **Dimensione**: 280x80 pixel

### **🎨 Design**
- **Font**: Open Sans / Noto Sans (fallback a Helvetica)
- **Sfondo**: Nero semi-trasparente (160/255 alpha)
- **Testo**: Bianco per programma corrente, grigio chiaro per dettagli
- **Formato**: Compatto e leggibile

### **⏰ Aggiornamento**
- **Frequenza**: Ogni 30 secondi
- **Metodo**: Generazione PNG + upload al server
- **Integrazione**: FFmpeg overlay filter

## 🛠️ ARCHITETTURA

### **📁 File Principali**

```
scripts/
├── aqua_time_overlay.py          # Generatore overlay principale
├── control_aqua_overlay.sh       # Controllo servizio overlay
├── aqua_streaming_with_overlay.sh # Streaming con overlay integrato
└── calculate_remaining_time.py   # Calcolo tempo rimanente
```

### **🔄 Flusso di Funzionamento**

1. **Calcolo Posizione**: Determina programma corrente e tempo rimanente
2. **Generazione Immagine**: Crea PNG con informazioni temporali
3. **Upload Server**: Trasferisce overlay al server streaming
4. **Integrazione FFmpeg**: Combina overlay con video streaming
5. **Aggiornamento**: Ripete ogni 30 secondi

## 🚀 UTILIZZO

### **📊 Controllo Tempo Rimanente**

```bash
# Calcolo immediato
python3 scripts/calculate_remaining_time.py

# Output:
⏰ STATUS PALINSESTO AQUA LOFI
========================================
🎵 Programma Corrente: Abyss Deep
⏳ Tempo Rimanente: 03:37:44
🔄 Prossimo Programma: Blue Bossa
🔄 Cicli Completati: 0
⏱️ Tempo Totale Trascorso: 01:00:00
```

### **⏰ Gestione Servizio Overlay**

```bash
# Avvia servizio overlay
./scripts/control_aqua_overlay.sh start

# Controlla status
./scripts/control_aqua_overlay.sh status

# Testa generazione
./scripts/control_aqua_overlay.sh test

# Preview overlay
./scripts/control_aqua_overlay.sh preview

# Ferma servizio
./scripts/control_aqua_overlay.sh stop

# Riavvia servizio
./scripts/control_aqua_overlay.sh restart
```

### **🎬 Streaming con Overlay**

```bash
# Streaming completo con overlay integrato
./scripts/aqua_streaming_with_overlay.sh
```

## 🔧 CONFIGURAZIONE

### **📏 Parametri Overlay**

```python
# Configurazione posizionamento
overlay_width = 280      # Larghezza overlay
overlay_height = 80      # Altezza overlay
margin_left = 30         # Margine sinistro
margin_bottom = 30       # Margine inferiore
```

### **⏱️ Durate Palinsesto**

```python
minimix_durations = {
    'abyss': 16665,           # 4.62 ore
    'blue_bossa': 18688,      # 5.19 ore  
    'meditative_tide': 15083  # 4.18 ore
}
```

### **🎵 Ordine Palinsesto**

```python
palinsest_order = ['abyss', 'blue_bossa', 'meditative_tide']
friendly_names = {
    'abyss': 'Abyss Deep',
    'blue_bossa': 'Blue Bossa', 
    'meditative_tide': 'Meditative Tide'
}
```

## 🎨 INTEGRAZIONE FFMPEG

### **🔧 Comando Base**

```bash
ffmpeg -i video.mp4 -i /tmp/aqua_time_overlay.png \
  -filter_complex "overlay=30:H-h-30" \
  -c:v libx264 -c:a copy output_with_overlay.mp4
```

### **📡 Streaming Live**

```bash
ffmpeg -i video.mp4 -i /tmp/aqua_time_overlay.png \
  -filter_complex "overlay=30:H-h-30" \
  -c:v libx264 -preset ultrafast -b:v 6800k \
  -c:a aac -b:a 128k -f flv rtmp://...
```

## 📊 MONITORAGGIO

### **📝 Log Files**

```
/tmp/aqua_overlay.pid      # PID del servizio overlay
/tmp/aqua_overlay.log      # Log del servizio
/tmp/aqua_time_overlay.png # File overlay corrente
```

### **🔍 Status Check**

```bash
# Verifica servizio attivo
ps aux | grep aqua_time_overlay

# Controlla file overlay
ls -la /tmp/aqua_time_overlay.png

# Monitora log in tempo reale
tail -f /tmp/aqua_overlay.log
```

## 🎯 VANTAGGI

### **✅ FFmpeg Direct vs OBS**

| Aspetto | FFmpeg Direct | OBS |
|---------|---------------|-----|
| **Overlay** | ✅ Possibile | ✅ Possibile |
| **Complessità** | Media | Alta |
| **Performance** | Ottima | Buona |
| **Affidabilità** | Alta | Media |
| **Controllo** | CLI | GUI |
| **Risorse** | Basse | Medie |

### **🚀 Benefici**

1. **Informazioni Live**: Spettatori vedono programma e tempo rimanente
2. **Trasparenza**: Chiarezza su cosa sta suonando e cosa verrà dopo
3. **Engagement**: Migliora esperienza utente
4. **Automazione**: Nessun intervento manuale richiesto
5. **Affidabilità**: Sistema robusto e testato

## 🔧 TROUBLESHOOTING

### **❌ Problemi Comuni**

#### **Overlay non si aggiorna**
```bash
# Riavvia servizio
./scripts/control_aqua_overlay.sh restart

# Verifica log
tail -f /tmp/aqua_overlay.log
```

#### **File overlay mancante**
```bash
# Testa generazione
./scripts/control_aqua_overlay.sh test

# Verifica permessi
ls -la /tmp/aqua_time_overlay.png
```

#### **Font non trovato**
```python
# Il sistema usa fallback automatico:
# 1. Open Sans / Noto Sans
# 2. Helvetica (macOS)
# 3. Font di default
```

### **🔍 Debug**

```bash
# Debug completo
./scripts/control_aqua_overlay.sh status
python3 scripts/calculate_remaining_time.py
ls -la /tmp/aqua_time_overlay.png
```

## 📈 ROADMAP FUTURA

### **🎨 Miglioramenti UI**
- [ ] Animazioni smooth per transizioni
- [ ] Barra progresso visiva
- [ ] Colori personalizzabili per tema
- [ ] Posizionamento dinamico

### **⚡ Ottimizzazioni**
- [ ] Cache overlay per performance
- [ ] Compressione PNG ottimizzata
- [ ] Aggiornamento differenziale
- [ ] Monitoraggio risorse

### **🌐 Integrazioni**
- [ ] API REST per controllo remoto
- [ ] Dashboard web per monitoraggio
- [ ] Notifiche Discord/Telegram
- [ ] Analytics overlay usage

## 📚 RIFERIMENTI

### **🔗 Documentazione Correlata**
- [Aqua Lofi Streaming System](17-Aqua-Lofi-Streaming-System-PRODUCTION.md)
- [FFmpeg Advanced Features](ffmpeg-advanced-features.md)
- [Database System](02-Database-System.md)

### **📖 Risorse Esterne**
- [FFmpeg Overlay Filter](https://ffmpeg.org/ffmpeg-filters.html#overlay-1)
- [PIL ImageDraw](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html)
- [Open Sans Font](https://fonts.google.com/specimen/Open+Sans)

---

**🎨 Sistema Overlay Temporale Aqua Lofi** - Implementazione completa per informazioni live nel palinsesto streaming. 