#!/bin/bash

# 🚀 Setup Lofi Streaming Server
# Dominio: lofi-streaming.com
# Droplet: DigitalOcean Ubuntu 22.04

set -e

echo "🎵 Setup Lofi Streaming Server"
echo "================================"

# Aggiorna sistema
echo "📦 Aggiornamento sistema..."
sudo apt update && sudo apt upgrade -y

# Installa dipendenze
echo "🔧 Installazione dipendenze..."
sudo apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    certbot \
    python3-certbot-nginx \
    ffmpeg \
    obs-studio \
    git \
    curl \
    wget \
    unzip \
    supervisor \
    htop \
    ufw

# Configura firewall
echo "🔥 Configurazione firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw --force enable

# Crea utente per l'applicazione
echo "👤 Creazione utente applicazione..."
sudo useradd -m -s /bin/bash lofi || true
sudo usermod -aG sudo lofi

# Clona repository
echo "📥 Clonazione repository..."
cd /home/lofi
sudo -u lofi git clone https://github.com/tuo-username/lofi-automation-youtube.git || true
cd lofi-automation-youtube

# Setup Python environment
echo "🐍 Setup Python environment..."
sudo -u lofi python3 -m venv venv
sudo -u lofi ./venv/bin/pip install -r requirements.txt

# Configura OBS Studio (headless)
echo "🎥 Configurazione OBS Studio..."
sudo -u lofi mkdir -p /home/lofi/.config/obs-studio
sudo -u lofi mkdir -p /home/lofi/.config/obs-studio/basic/profiles

# Configura Nginx
echo "🌐 Configurazione Nginx..."
sudo tee /etc/nginx/sites-available/lofi-streaming.com << EOF
server {
    listen 80;
    server_name lofi-streaming.com www.lofi-streaming.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name lofi-streaming.com www.lofi-streaming.com;
    
    # SSL configuration will be added by certbot
    
    # API Backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Frontend Dashboard
    location / {
        root /home/lofi/lofi-automation-youtube/ui/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
    
    # WebSocket support
    location /ws/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
    }
}

# Subdomain: api.lofi-streaming.com
server {
    listen 80;
    server_name api.lofi-streaming.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name api.lofi-streaming.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Subdomain: dashboard.lofi-streaming.com
server {
    listen 80;
    server_name dashboard.lofi-streaming.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name dashboard.lofi-streaming.com;
    
    location / {
        root /home/lofi/lofi-automation-youtube/ui/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
EOF

# Abilita sito
sudo ln -sf /etc/nginx/sites-available/lofi-streaming.com /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL con Let's Encrypt
echo "🔒 Setup SSL con Let's Encrypt..."
sudo certbot --nginx -d lofi-streaming.com -d www.lofi-streaming.com -d api.lofi-streaming.com -d dashboard.lofi-streaming.com --non-interactive --agree-tos --email tuo-email@gmail.com

# Configura renewal automatico
echo "0 12 * * * /usr/bin/certbot renew --quiet" | sudo crontab -

# Setup Supervisor per servizi
echo "⚙️ Configurazione Supervisor..."
sudo tee /etc/supervisor/conf.d/lofi-backend.conf << EOF
[program:lofi-backend]
command=/home/lofi/lofi-automation-youtube/venv/bin/python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
directory=/home/lofi/lofi-automation-youtube/ui/backend
user=lofi
autostart=true
autorestart=true
stderr_logfile=/var/log/lofi-backend.err.log
stdout_logfile=/var/log/lofi-backend.out.log
EOF

sudo tee /etc/supervisor/conf.d/lofi-streaming.conf << EOF
[program:lofi-streaming]
command=/home/lofi/lofi-automation-youtube/venv/bin/python streaming_manager.py
directory=/home/lofi/lofi-automation-youtube/ui/backend
user=lofi
autostart=true
autorestart=true
stderr_logfile=/var/log/lofi-streaming.err.log
stdout_logfile=/var/log/lofi-streaming.out.log
EOF

# Riavvia supervisor
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start lofi-backend
sudo supervisorctl start lofi-streaming

echo "✅ Setup completato!"
echo "🌐 Dashboard: https://dashboard.lofi-streaming.com"
echo "🌐 API: https://api.lofi-streaming.com"
echo "📊 Monitor: https://monitor.lofi-streaming.com" 