# Guida alla Gestione Canali - Frontend

## Panoramica

La nuova funzionalità di gestione canali permette di visualizzare e modificare i canali streaming direttamente dal frontend web. Ogni canale può essere configurato con nome, descrizione e stream key.

## Accesso alla Pagina

1. Apri il frontend all'indirizzo: `http://localhost:5173`
2. Clicca su "Canali" nella barra di navigazione (icona radio)
3. Verrai reindirizzato alla pagina `/channels`

## Funzionalità Disponibili

### Visualizzazione Canali

La pagina mostra tutti i canali in una griglia con:

- **Nome del canale** - Titolo principale
- **Slug** - Identificatore univoco
- **Descrizione** - Descrizione del contenuto
- **Status** - Attivo/Inattivo (con badge colorato)
- **Statistiche** - Numero di brani audio e video
- **Stream Key Status** - Indicatore se la stream key è configurata

### Modifica Canale

1. **Avvia Modifica**: Clicca sul pulsante "Modifica" (icona matita)
2. **Campi Editabili**:
   - **Nome**: Campo di testo per il nome del canale
   - **Descrizione**: Area di testo per la descrizione
3. **Salva**: Clicca "Salva" per confermare le modifiche
4. **Annulla**: Clicca "Annulla" per scartare le modifiche

### Controllo Streaming

- **Avvia Streaming**: Pulsante verde "Avvia" per canali inattivi
- **Ferma Streaming**: Pulsante rosso "Ferma" per canali attivi
- **Status in Tempo Reale**: Il badge di status si aggiorna automaticamente

## Struttura Dati

Ogni canale contiene:

```json
{
  "id": 1,
  "name": "Lofi Chill",
  "slug": "lofi-chill", 
  "description": "Musica lofi rilassante per studiare e lavorare",
  "status": "inactive",
  "stream_key": "test-key-123",
  "audio_count": 20,
  "video_count": 2,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

## API Endpoints

### GET /api/channels
Lista tutti i canali disponibili

### GET /api/channels/{id}
Ottiene i dettagli di un canale specifico

### PUT /api/channels/{id}
Aggiorna nome e descrizione di un canale

**Body:**
```json
{
  "name": "Nuovo Nome",
  "description": "Nuova descrizione"
}
```

### POST /api/channels/{slug}/start
Avvia lo streaming per un canale

### POST /api/channels/{slug}/stop
Ferma lo streaming per un canale

## Stati del Canale

- **🟢 Attivo**: Canale in streaming
- **🔴 Inattivo**: Canale fermo
- **🔑 Stream Key configurata**: Stream key presente
- **❌ Stream Key mancante**: Stream key non configurata

## Responsive Design

La pagina è completamente responsive:
- **Desktop**: Griglia 3 colonne
- **Tablet**: Griglia 2 colonne  
- **Mobile**: Griglia 1 colonna

## Prossimi Sviluppi

- [ ] Integrazione con database reale
- [ ] Upload media per canale
- [ ] Configurazione stream key dal frontend
- [ ] Statistiche streaming in tempo reale
- [ ] Notifiche per cambi di status

## Troubleshooting

### Problemi Comuni

1. **Canali non caricati**: Verifica che il backend sia in esecuzione su porta 8000
2. **Modifiche non salvate**: Controlla la console del browser per errori
3. **Streaming non avviato**: Verifica che la stream key sia configurata

### Log di Debug

Apri la console del browser (F12) per vedere:
- Richieste API
- Errori di rete
- Aggiornamenti di stato

## Note Tecniche

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: FastAPI + Python
- **Stato**: Gestito localmente con React hooks
- **API**: RESTful con JSON
- **CORS**: Configurato per sviluppo locale 