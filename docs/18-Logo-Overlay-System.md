# Logo Overlay System

## Panoramica
Sistema per creare video overlay con logo animato e timing prestabilito, ottimizzato per l'uso in OBS Studio come sovrimpressione.

## File Generati

### 1. Meditative_Tide_Unscreen_Sequence_HD.mov ⭐ **RACCOMANDATO**
- **Formato**: ProRes 4444 (canale alpha perfetto)
- **Durata**: 35 secondi  
- **Risoluzione**: 1430x1080 px (risoluzione originale)
- **Frame Rate**: 24 fps
- **Peso**: ~35 MB
- **Qualità**: AI-processed con Unscreen per rimozione sfondo perfetta
- **Timing**: 4 apparizioni logo (0s, 8.2s, 16.4s, 24.6s)

### 2. Meditative_Tide_Unscreen_Sequence.mov
- **Formato**: ProRes 4444 
- **Durata**: 35 secondi
- **Risoluzione**: 476x360 px (risoluzione Unscreen)
- **Peso**: ~8 MB
- **Qualità**: Versione compatta AI-processed

### 3. Meditative_Tide_Overlay_Sequence.mov (Legacy)
- **Formato**: ProRes 4444 (FFmpeg colorkey)
- **Durata**: 35 secondi
- **Risoluzione**: 1430x1080 px
- **Peso**: ~21 MB
- **Nota**: Rimozione sfondo limitata, problemi con particelle blu dinamiche

## Struttura Temporale

Il video è strutturato con timing prestabilito per 4 apparizioni del logo:

```
Timeline (35 secondi totali):
┌─────────────┬─────────────┬─────────────┬─────────────┬─────────────┐
│  0-5.2s     │  5.2-8.2s   │ 8.2-13.4s   │ 13.4-16.4s  │ 16.4-21.6s  │
│ Logo+Fade   │   Pausa     │ Logo+Fade   │   Pausa     │ Logo+Fade   │
└─────────────┴─────────────┴─────────────┴─────────────┴─────────────┘
┌─────────────┬─────────────┬─────────────┐
│ 21.6-24.6s  │ 24.6-29.8s  │ 29.8-35s    │
│   Pausa     │ Logo+Fade   │ Pausa Finale │
└─────────────┴─────────────┴─────────────┘
```

### Dettaglio Sequenze:
1. **0-5.2s**: Animazione logo completa + fade out (0.5s)
2. **5.2-8.2s**: Pausa trasparente (3s)
3. **8.2-13.4s**: Animazione logo + fade out (0.5s)
4. **13.4-16.4s**: Pausa trasparente (3s)  
5. **16.4-21.6s**: Animazione logo + fade out (0.5s)
6. **21.6-24.6s**: Pausa trasparente (3s)
7. **24.6-29.8s**: Animazione logo + fade out (0.5s)
8. **29.8-35s**: Pausa finale estesa (5.2s)

## Configurazione OBS Studio

### 1. Aggiunta Fonte Video
```
Sources → Add → Media Source
- Name: "Meditative Tide Logo"
- Local File: Meditative_Tide_Overlay_Sequence.mov
- Loop: ✓ Enabled
- Restart playback when source becomes active: ✓ Enabled
```

### 2. Posizionamento
- **Layer**: Sopra tutti gli altri elementi
- **Posizione**: Personalizzabile (es. basso-destra)
- **Dimensioni**: Mantenere proporzioni originali o ridimensionare

### 3. Filtri Aggiuntivi (Opzionali)
```
Right-click → Filters → Add
- Chroma Key: Se necessario per ulteriore pulizia
- Color Correction: Per regolare luminosità/contrasto
- Scaling/Aspect Ratio: Per ridimensionamento preciso
```

## Confronto: Unscreen AI vs FFmpeg Colorkey

### 🤖 **Unscreen AI (VINCITORE)**

#### ✅ Vantaggi
- **Rimozione sfondo perfetta**: Gestisce automaticamente tutte le tonalità di blu
- **Particelle dinamiche**: Rimuove anche le "macchioline bluastre" che attraversano la scena
- **Bordi precisi**: Preserva perfettamente i dettagli del testo e delle onde
- **Qualità professionale**: Risultato equivalente a compositing manuale
- **Zero configurazione**: Nessun tuning parametri necessario

#### ❌ Svantaggi  
- **Servizio esterno**: Dipendenza da unscreen.com
- **Risoluzione ridotta**: Output a 476x360 (upscaling necessario)
- **Processo manuale**: Richiede upload/download
- **Limitazioni gratuite**: Possibili restrizioni su utilizzo

### ⚙️ **FFmpeg Colorkey (LIMITATO)**

#### ✅ Vantaggi
- **Controllo locale**: Nessuna dipendenza esterna
- **Automazione completa**: Scriptabile e ripetibile
- **Risoluzione nativa**: Mantiene 1430x1080 originale
- **Personalizzazione**: Parametri fine-tuning

#### ❌ Svantaggi
- **Sfondo complesso**: Fallisce con blu multi-tonalità
- **Particelle dinamiche**: Non gestisce elementi blu che cambiano
- **Tuning laborioso**: Richiede test multipli per parametri ottimali
- **Risultato incompleto**: Residui di sfondo visibili

### 🎯 **Raccomandazione**
**Usare Unscreen AI** per logo con sfondi complessi e elementi dinamici.  
FFmpeg colorkey è adeguato solo per sfondi uniformi e statici.

## Vantaggi Generali Sistema

### ✅ Timing Prestabilito
- Nessuna logica complessa in OBS
- Controllo preciso delle apparizioni  
- Sincronizzazione perfetta

### ✅ Performance Ottimizzate
- Nessun processing real-time
- Loop semplice e stabile
- Carico CPU minimo

### ✅ Flessibilità
- Facile spostamento/ridimensionamento
- Possibilità di aggiungere filtri
- Integrazione con altre scene

### ✅ Qualità Professionale
- Supporto canale alpha completo
- Transizioni fluide e precise
- Risoluzione ottimale per streaming

## Script di Generazione

### Script Principale (Unscreen) ⭐ **RACCOMANDATO**
```bash
scripts/create_logo_overlay_unscreen.py
```

**Prerequisiti**:
1. Processare il logo originale con [Unscreen.com](https://www.unscreen.com/)
2. Scaricare il GIF risultante
3. Convertire in MOV con: `ffmpeg -i logo.gif -c:v prores_ks -profile:v 4444 logo.mov`

**Esecuzione**:
```bash
python scripts/create_logo_overlay_unscreen.py
```

### Script Legacy (FFmpeg Colorkey)
```bash
scripts/create_logo_overlay_sequence.py
```

**Parametri Personalizzabili**:
```python
# Durata totale del video
total_duration = 35  # secondi

# Timing fade out  
fade_start = 4.7     # inizio fade (da fine animazione)
fade_duration = 0.5  # durata fade

# Parametri colorkey (problematici con sfondi complessi)
colorkey_tolerance = 0.3
colorkey_blend = 0.1
```

**Esecuzione**:
```bash
python scripts/create_logo_overlay_sequence.py
```

### Script Analisi Colori (Debug)
```bash
scripts/analyze_logo_colors.py
```

Crea test multipli per identificare parametri colorkey ottimali:
```bash
python scripts/analyze_logo_colors.py
# Genera 9 test video in /tmp/color_tests/
```

## Processo Tecnico

### 1. Pulizia Logo
- Rimozione sfondo nero con `colorkey`
- Conversione a formato con canale alpha
- Ottimizzazione qualità trasparenza

### 2. Timing Sequence
- Creazione background trasparente
- Posizionamento temporale preciso
- Gestione fade e transizioni

### 3. Output Optimization
- ProRes 4444 per qualità massima
- Supporto alpha channel nativo
- Compatibilità OBS completa

## Note Tecniche

### Formati Supportati
- **ProRes 4444**: Produzione (canale alpha)
- **H.264**: Anteprima (senza alpha)
- **MOV**: Container ottimale per OBS

### Requisiti Sistema
- FFmpeg con codec ProRes
- OBS Studio 27+ (supporto alpha migliorato)
- macOS/Windows/Linux compatibile

### File Size Considerations
- ProRes: ~21MB per 35s (qualità massima)
- H.264: ~32KB per 35s (anteprima only)
- Rapporto qualità/peso ottimale

## Troubleshooting

### Logo Non Visibile in OBS
1. Verificare ordine layer (deve essere sopra)
2. Controllare impostazioni loop
3. Verificare supporto formato ProRes

### Timing Non Sincronizzato
1. Riavviare playback in OBS
2. Verificare fps matching con scene
3. Controllare buffer settings

### Performance Issues
1. Ridurre risoluzione se necessario
2. Convertire a H.264 se alpha non necessario
3. Ottimizzare cache OBS

## Estensioni Future

### Varianti Timing
- Apparizioni più frequenti
- Fade più lunghi/corti
- Pattern diversi

### Multi-Logo Support
- Sequenze multiple
- Logo rotativi
- Animazioni sincronizzate

### Integration Avanzata
- Controllo via OBS Scripts
- Trigger esterni
- Sincronizzazione audio

---

**Creato**: 16 Luglio 2025  
**Versione**: 1.0  
**Compatibilità**: OBS Studio, FFmpeg 7.1+ 