# Guía de Despliegue: NeuroBeats en bitware.site

Esta guía te llevará paso a paso para desplegar tu proyecto en tu VPS de Hostinger y conectarlo con tu dominio `bitware.site`.

## 0. Variables de Entorno (Seguridad)
El proyecto ahora usa variables de entorno. En el VPS, crea el archivo `.env`:
```bash
nano /var/www/NeuroBeats/.env
```
Pega el contenido del archivo `.env.example` de tu proyecto y RELLENA los datos reales (contraseña DB, Secret Key nueva).

## 1. Configuración de DNS (Hostinger)

Antes de tocar el servidor, apunta tu dominio a la IP de tu VPS.
1.  Ve al panel de **Hostinger > Dominios > bitware.site > DNS / Nameservers**.
2.  Agrega (o edita) los registros **A**:
    *   **Tipo**: A | **Nombre**: @ | **Apunta a**: `TU_IP_VPS` | **TTL**: 3600
    *   **Tipo**: A | **Nombre**: www | **Apunta a**: `TU_IP_VPS` | **TTL**: 3600

## 2. Acceso al VPS
Conéctate por SSH:
```bash
ssh root@TU_IP_VPS
```

## 3. Preparación del Sistema
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-dev libmysqlclient-dev pkg-config nginx git ffmpeg -y
```

## 4. Base de Datos (MySQL)
```bash
sudo apt install mysql-server -y
sudo mysql_secure_installation
```
Crear DB y Usuario:
```sql
sudo mysql -u root -p

CREATE DATABASE neurobeats_db CHARACTER SET utf8mb4;
CREATE USER 'neuro_user'@'localhost' IDENTIFIED BY 'tu_contraseña_segura';
GRANT ALL PRIVILEGES ON neurobeats_db.* TO 'neuro_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 5. Configuración del Proyecto

### Clonar y Entorno Virtual
```bash
cd /var/www
git clone https://github.com/TobbenTT/NeuroBeats.git
cd NeuroBeats

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Configuración Final
Asegúrate de configurar tus variables o editar `settings.py` (si no usas variables de entorno aún) para conectar a la DB que creaste.
```bash
python manage.py migrate
python manage.py collectstatic
```
*(Si tienes problemas de permisos con la carpeta media)*:
```bash
sudo chmod -R 777 /var/www/NeuroBeats/media
```

## 6. Configuración de Gunicorn
```bash
sudo nano /etc/systemd/system/gunicorn.service
```
Contenido:
```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/var/www/NeuroBeats
ExecStart=/var/www/NeuroBeats/venv/bin/gunicorn --access-logfile - --workers 3 --timeout 120 --bind unix:/var/www/NeuroBeats/neurobeats.sock config.wsgi:application

[Install]
WantedBy=multi-user.target
```
Activar:
```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

## 7. Configuración de Nginx para bitware.site
```bash
sudo nano /etc/nginx/sites-available/neurobeats
```
Contenido para tu dominio (¡Nota el cambio en client_max_body_size!):
```nginx
server {
    listen 80;
    server_name bitware.site www.bitware.site TU_IP_VPS;

    # Permitir subida de archivos grandes (50MB)
    client_max_body_size 50M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/NeuroBeats/staticfiles/;
    }

    location /media/ {
        root /var/www/NeuroBeats;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/NeuroBeats/neurobeats.sock;
    }
}
```
Activar:
```bash
sudo ln -s /etc/nginx/sites-available/neurobeats /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## 8. HTTPS (Candado de Seguridad)
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d bitware.site -d www.bitware.site
```

## 9. Cómo Actualizar tu Proyecto
Cada vez que hagas cambios en tu PC y los subas a GitHub, corre esto en el VPS:

```bash
cd /var/www/NeuroBeats
git pull
source venv/bin/activate
pip install -r requirements.txt  # Solo si instalaste nuevas librerías
python manage.py migrate         # Solo si cambiaste la base de datos
python manage.py collectstatic   # Solo si cambiaste estilos/JS
sudo systemctl restart gunicorn  # ¡OBLIGATORIO para ver los cambios!
```

## 10. Tareas en Segundo Plano (Celery + Redis)

Para que las subidas de audio no congelen la pantalla, necesitamos esto.

### A. Instalar Redis
```bash
sudo apt install redis-server -y
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

### B. Servicio Systemd para Celery
```bash
sudo nano /etc/systemd/system/neurobeats-celery.service
```
Contenido (Copia y pega):
```ini
[Unit]
Description=Celery Service for NeuroBeats
After=network.target

[Service]
Type=forking
User=root
Group=www-data
WorkingDirectory=/var/www/NeuroBeats
ExecStart=/var/www/NeuroBeats/venv/bin/celery -A config worker --loglevel=info --detach --pidfile=/var/www/NeuroBeats/celery_worker.pid
Restart=always

[Install]
WantedBy=multi-user.target
```
Activar:
```bash
sudo systemctl start neurobeats-celery
sudo systemctl enable neurobeats-celery
```

### C. Reiniciar todo tras actualizar
Cuando hagas cambios en el código de tareas (`tasks.py`), corre:
```bash
sudo systemctl restart neurobeats-celery
```

