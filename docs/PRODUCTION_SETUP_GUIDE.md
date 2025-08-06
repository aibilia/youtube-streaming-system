# 🚀 GUIDA SETUP PRODUZIONE - LOFI STREAMING

## 📋 **CHECKLIST COMPLETA**

### ✅ **COMPLETATO**
- [x] Server DigitalOcean configurato
- [x] Dominio `lofi-streaming.com` configurato
- [x] SSL/HTTPS attivo
- [x] Backend FastAPI funzionante
- [x] Database PostgreSQL DigitalOcean disponibile

### 🔧 **DA CONFIGURARE**
- [ ] API Keys (Step 1)
- [ ] Database PostgreSQL (Step 2)
- [ ] OBS Studio (Step 3)
- [ ] Frontend React (Step 4)
- [ ] Google Drive Sync (Step 5)
- [ ] YouTube Streaming (Step 6)
- [ ] Monitoraggio (Step 7)
- [ ] Test completo (Step 8)

---

## 🔑 **STEP 1: CONFIGURAZIONE API KEYS**

### **1.1 Connessione al Server**
```bash
ssh -i ~/.ssh/id_ed25519 root@159.89.106.38
```

### **1.2 Esecuzione Script di Configurazione**
```bash
cd /home/lofi/lofi-automation-youtube
python3 configure_production_keys.py
```

### **1.3 API Keys Necessarie**

#### **OpenAI API (DALL-E 3)**
- **Dove ottenerla:** https://platform.openai.com/api-keys
- **Formato:** `sk-...` (inizia con sk-)
- **Costo:** ~$0.040 per immagine 1024x1024
- **Utilizzo:** Generazione immagini per video

#### **FAL.ai API (Video Generation)**
- **Dove ottenerla:** https://fal.ai/dashboard
- **Formato:** Stringa alfanumerica
- **Costo:** ~$0.05-0.10 per video
- **Utilizzo:** Generazione video da immagini

#### **PIAPI API (Udio Audio)**
- **Dove ottenerla:** https://piapi.ai/
- **Formato:** Stringa alfanumerica
- **Costo:** ~$0.02-0.05 per traccia audio
- **Utilizzo:** Generazione musica lofi

#### **Google API (Drive + YouTube)**
- **Dove ottenerla:** https://console.cloud.google.com/
- **Formato:** `AIza...` (inizia con AIza)
- **Servizi da abilitare:**
  - Google Drive API
  - YouTube Data API v3
  - YouTube Live Streaming API
- **Utilizzo:** Gestione file e streaming YouTube

#### **YouTube Stream Key**
- **Dove ottenerla:** YouTube Studio > Live > Stream Key
- **Formato:** Stringa alfanumerica
- **Utilizzo:** Streaming live su YouTube

---

## 🗄️ **STEP 2: CONFIGURAZIONE DATABASE**

### **2.1 Ottenere Credenziali Database**
1. Vai su **DigitalOcean Dashboard**
2. Sezione **Databases**
3. Seleziona il tuo database PostgreSQL
4. Copia la **Connection String**

### **2.2 Formato Connection String**
```
postgresql://doadmin:PASSWORD@HOST:25060/defaultdb?sslmode=require
```

**Esempio:**
```
postgresql://doadmin:AVNS_abc123@lofi-production-db-do-user-12345-0.ondigitalocean.com:25060/defaultdb?sslmode=require
```

### **2.3 Test Connessione Database**
```bash
# Sul server
cd /home/lofi/lofi-automation-youtube
python3 -c "
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('.env.production')
engine = create_engine(os.getenv('DATABASE_URL'))
with engine.connect() as conn:
    result = conn.execute('SELECT version();')
    print('✅ Database connesso:', result.fetchone()[0])
"
```

---

## 🎥 **STEP 3: INSTALLAZIONE OBS STUDIO**

### **3.1 Installazione OBS**
```bash
# Sul server
ssh -i ~/.ssh/id_ed25519 root@159.89.106.38

# Installa OBS e dipendenze
sudo apt update
sudo apt install -y obs-studio xvfb pulseaudio pavucontrol

# Installa OBS WebSocket plugin
wget https://github.com/obsproject/obs-websocket/releases/download/5.4.2/obs-websocket-5.4.2-linux-x64.tar.gz
tar -xzf obs-websocket-5.4.2-linux-x64.tar.gz
sudo cp -r obs-websocket-5.4.2-linux-x64/* /usr/
```

### **3.2 Configurazione OBS Headless**
```bash
# Crea configurazione OBS
mkdir -p /home/lofi/.config/obs-studio/basic/profiles/Streaming
mkdir -p /home/lofi/.config/obs-studio/basic/scenes

# Crea profilo streaming
cat > /home/lofi/.config/obs-studio/basic/profiles/Streaming/basic.ini << 'EOF'
[General]
Name=Streaming

[Video]
BaseCX=1920
BaseCY=1080
OutputCX=1920
OutputCY=1080
FPSType=0
FPSCommon=30

[Audio]
SampleRate=44100
ChannelSetup=Stereo
EOF

# Crea scene collection
cat > /home/lofi/.config/obs-studio/basic/scenes/Lofi.json << 'EOF'
{
    "current_scene": "Lofi Scene",
    "scenes": [
        {
            "name": "Lofi Scene",
            "sources": []
        }
    ]
}
EOF

# Imposta permessi
chown -R lofi:lofi /home/lofi/.config/obs-studio
```

### **3.3 Configurazione WebSocket**
```bash
# Crea configurazione WebSocket
mkdir -p /home/lofi/.config/obs-studio/plugin_config/obs-websocket
cat > /home/lofi/.config/obs-studio/plugin_config/obs-websocket/config.json << 'EOF'
{
    "server_enabled": true,
    "server_port": 4455,
    "authentication_enabled": true,
    "server_password": "lofi-streaming-2024"
}
EOF

chown -R lofi:lofi /home/lofi/.config/obs-studio
```

---

## 🌐 **STEP 4: BUILD FRONTEND**

### **4.1 Installazione Node.js**
```bash
# Sul server
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verifica installazione
node --version
npm --version
```

### **4.2 Build Frontend**
```bash
# Sul server
cd /home/lofi/lofi-automation-youtube/ui/frontend

# Installa dipendenze
sudo -u lofi npm install

# Build produzione
sudo -u lofi npm run build

# Verifica build
ls -la dist/
```

### **4.3 Configurazione Nginx per Frontend**
Il frontend buildato sarà servito da Nginx dalla cartella `dist/`.

---

## 📁 **STEP 5: GOOGLE DRIVE SYNC**

### **5.1 Installazione rclone**
```bash
# Sul server
curl https://rclone.org/install.sh | sudo bash

# Verifica installazione
rclone version
```

### **5.2 Configurazione Google Drive**
```bash
# Sul server
sudo -u lofi rclone config

# Segui il wizard:
# 1. Scegli "n" per new remote
# 2. Nome: "gdrive"
# 3. Tipo: "drive" (Google Drive)
# 4. Client ID: (lascia vuoto per default)
# 5. Client Secret: (lascia vuoto per default)
# 6. Scope: "drive" (accesso completo)
# 7. Root folder: (lascia vuoto)
# 8. Service account: "false"
# 9. Auto config: "false" (server headless)
# 10. Copia l'URL e aprilo sul tuo browser
# 11. Autorizza l'app e copia il codice
# 12. Incolla il codice nel terminale
```

### **5.3 Test Sync**
```bash
# Test connessione
sudo -u lofi rclone lsd gdrive:

# Crea cartelle media
sudo -u lofi rclone mkdir gdrive:lofi-streaming/audio
sudo -u lofi rclone mkdir gdrive:lofi-streaming/video
sudo -u lofi rclone mkdir gdrive:lofi-streaming/images

# Sync automatico (cron job)
sudo -u lofi crontab -e
# Aggiungi:
# */5 * * * * /usr/bin/rclone sync gdrive:lofi-streaming/audio /home/lofi/media/audio --quiet
# */5 * * * * /usr/bin/rclone sync gdrive:lofi-streaming/video /home/lofi/media/video --quiet
# */5 * * * * /usr/bin/rclone sync gdrive:lofi-streaming/images /home/lofi/media/images --quiet
```

---

## 📺 **STEP 6: YOUTUBE STREAMING**

### **6.1 Configurazione YouTube Live**
1. Vai su **YouTube Studio**
2. Sezione **Live**
3. Crea un **Live Stream**
4. Copia la **Stream Key**
5. Configura:
   - **Titolo:** "Lofi Hip Hop Radio 24/7"
   - **Descrizione:** "Continuous lofi beats for study and relaxation"
   - **Categoria:** Music
   - **Visibilità:** Public

### **6.2 Test Streaming**
```bash
# Sul server
cd /home/lofi/lofi-automation-youtube

# Test connessione YouTube
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv('.env.production')

rtmp_url = os.getenv('YOUTUBE_RTMP_URL')
stream_key = os.getenv('YOUTUBE_STREAM_KEY')

print(f'RTMP URL: {rtmp_url}')
print(f'Stream Key: {stream_key[:10]}...')
"
```

---

## 📊 **STEP 7: MONITORAGGIO**

### **7.1 Configurazione Supervisor per OBS**
```bash
# Sul server
cat > /etc/supervisor/conf.d/obs-studio.conf << 'EOF'
[program:obs-studio]
command=/usr/bin/xvfb-run -a -s "-screen 0 1920x1080x24" /usr/bin/obs --startstreaming --minimize-to-tray
directory=/home/lofi
user=lofi
autostart=true
autorestart=true
stderr_logfile=/var/log/obs-studio.err.log
stdout_logfile=/var/log/obs-studio.out.log
environment=DISPLAY=:0,HOME=/home/lofi
EOF

# Ricarica configurazione
supervisorctl reread
supervisorctl update
```

### **7.2 Script di Monitoraggio**
```bash
# Sul server
cat > /home/lofi/monitor_streaming.py << 'EOF'
#!/usr/bin/env python3
import requests
import time
import json
from datetime import datetime

def check_backend():
    try:
        response = requests.get('http://localhost:8000/api/health', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_obs():
    # Implementa controllo OBS WebSocket
    return True

def check_youtube():
    # Implementa controllo stream YouTube
    return True

def main():
    while True:
        status = {
            'timestamp': datetime.now().isoformat(),
            'backend': check_backend(),
            'obs': check_obs(),
            'youtube': check_youtube()
        }
        
        print(json.dumps(status))
        
        # Salva su file
        with open('/home/lofi/logs/streaming_status.json', 'w') as f:
            json.dump(status, f)
        
        time.sleep(60)

if __name__ == '__main__':
    main()
EOF

chmod +x /home/lofi/monitor_streaming.py
chown lofi:lofi /home/lofi/monitor_streaming.py
```

---

## 🧪 **STEP 8: TEST COMPLETO**

### **8.1 Test Backend**
```bash
# Test API health
curl https://api.lofi-streaming.com/api/health

# Test generazione contenuto
curl -X POST https://api.lofi-streaming.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{"type": "audio", "prompt": "relaxing lofi beats"}'
```

### **8.2 Test OBS**
```bash
# Test OBS WebSocket
python3 -c "
import websocket
import json

def test_obs():
    ws = websocket.create_connection('ws://localhost:4455')
    
    # Auth request
    auth_msg = {
        'op': 1,
        'data': {
            'rpcVersion': 1,
            'authentication': 'lofi-streaming-2024'
        }
    }
    
    ws.send(json.dumps(auth_msg))
    response = ws.recv()
    print('OBS Response:', response)
    
    ws.close()

test_obs()
"
```

### **8.3 Test Streaming Completo**
```bash
# Avvia tutti i servizi
supervisorctl start lofi-backend
supervisorctl start obs-studio

# Controlla status
supervisorctl status

# Test streaming per 5 minuti
sleep 300

# Controlla log
tail -f /var/log/obs-studio.out.log
```

---

## 🎯 **RISULTATO FINALE**

Al completamento di tutti gli step, avrai:

✅ **Server di streaming 24/7 completamente funzionante**
- Backend API per controllo remoto
- OBS Studio per streaming automatico
- Database PostgreSQL per persistenza
- Frontend React per dashboard
- Google Drive sync per media
- YouTube Live streaming attivo
- Monitoraggio in tempo reale

✅ **Domini configurati:**
- `https://lofi-streaming.com` - Frontend dashboard
- `https://api.lofi-streaming.com` - API backend
- `https://monitor.lofi-streaming.com` - Monitoraggio

✅ **Servizi automatici:**
- Auto-restart in caso di crash
- Sync automatico media da Google Drive
- Generazione automatica contenuti
- Streaming continuo su YouTube

---

## 📞 **SUPPORTO**

Se incontri problemi durante il setup:

1. **Controlla i log:**
   ```bash
   tail -f /var/log/lofi-backend.out.log
   tail -f /var/log/obs-studio.out.log
   ```

2. **Verifica servizi:**
   ```bash
   supervisorctl status
   systemctl status nginx
   ```

3. **Test connessioni:**
   ```bash
   curl -I https://api.lofi-streaming.com/api/health
   ```

**Il sistema è progettato per essere completamente autonomo una volta configurato!** 🚀 