# Guía de Acceso Remoto a Base de Datos (MySQL)

Sigue estos pasos para poder conectarte a tu base de datos desde tu computadora (usando Workbench, DBeaver, etc.).

## 1. Permitir Conexiones Externas en MySQL
Por defecto, MySQL solo "escucha" peticiones desde el mismo servidor (`127.0.0.1`). Debemos cambiar esto.

1.  Edita la configuración de MySQL en tu VPS:
    ```bash
    sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
    ```
2.  Busca la línea que dice:
    ```ini
    bind-address = 127.0.0.1
    ```
3.  Cámbiala por:
    ```ini
    bind-address = 0.0.0.0
    ```
    *(Esto permite conexiones desde cualquier IP).*
4.  Guarda (`Ctrl+O`, `Enter`) y sal (`Ctrl+X`).
5.  Reinicia MySQL:
    ```bash
    sudo systemctl restart mysql
    ```

## 2. Crear un Usuario para Acceso Remoto
El usuario `root` a veces está bloqueado para acceso remoto por seguridad. Mejor creamos uno nuevo.

1.  Entra a MySQL:
    ```bash
    sudo mysql -u root -p
    ```
2.  Ejecuta estos comandos (cambia `tu_password_segura`):
    ```sql
    -- Crear usuario que puede conectarse desde cualquier IP (%)
    CREATE USER 'TobbenTT'@'%' IDENTIFIED BY 'Rocky26..';

    -- Darle permisos totales sobre tu base de datos
    GRANT ALL PRIVILEGES ON neurobeats_db.* TO 'TobbenTT'@'%';

    -- Aplicar cambios
    FLUSH PRIVILEGES;
    EXIT;
    ```

## 3. Configurar Firewall (Si está activo)
Si tienes un firewall en el VPS (como UFW), debes permitir el tráfico en el puerto 3306.

```bash
sudo ufw allow 3306/tcp
```

> **Nota:** En Hostinger, a veces también hay un "Firewall Externo" en el panel de control. Si lo anterior no funciona, ve al panel de Hostinger > VPS > Seguridad/Firewall y asegúrate de que no estén bloqueando el puerto 3306.

## 4. Conectar desde tu PC
Ahora abre tu programa favorito (DBeaver, MySQL Workbench, HeidiSQL) y usa:
*   **Host/IP**: `bitware.site` (o la IP de tu VPS)
*   **Puerto**: `3306`
*   **Usuario**: `TobbenTT`
*   **Password**: `Rocky26..`

¡Listo!
