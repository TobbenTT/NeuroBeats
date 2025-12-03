# 🧠 NeuroBeats - Streaming Social con Inteligencia Artificial

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTMX](https://img.shields.io/badge/HTMX-SPA_Feel-336699?style=for-the-badge&logo=htmx&logoColor=white)
![Librosa](https://img.shields.io/badge/AI-Librosa-orange?style=for-the-badge)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)

### 👋 ¡Bienvenido a NeuroBeats!

**NeuroBeats** es una plataforma de streaming de música de próxima generación que fusiona la experiencia de una red social con el poder de la **Inteligencia Artificial**.

A diferencia de los reproductores tradicionales, NeuroBeats analiza el **"Vibe"** (BPM y Energía) de las canciones utilizando la librería científica `Librosa` para ofrecer recomendaciones basadas en el estado de ánimo real del usuario, no solo en etiquetas de género.

El proyecto implementa una arquitectura moderna con **Django** en el backend y **HTMX** en el frontend, logrando una experiencia de **Single Page Application (SPA)** donde la música nunca se detiene mientras navegas.

---

## ✨ Características Principales

### 🤖 IA & DJ Anita (Core Tecnológico)
* **Análisis de Audio Real:** Al subir una canción, el sistema procesa el archivo con `Librosa` para extraer matemáticamente los **BPM (Velocidad)** y la **Energía**.
* **DJ Anita HUD:** Un asistente virtual lateral que muestra tus estadísticas de escucha en tiempo real y te recomienda "Tracks VIP" basados en tu *mood* actual.
* **Motor de Recomendación Híbrido:** Sugiere música cruzando datos de tus Likes con el análisis sónico de las pistas.

### 🎧 Experiencia de Usuario (UX)
* **Reproductor Persistente:** Navegación fluida sin cortes de audio gracias a la integración de **HTMX** (Boost Mode).
* **Interfaz Dark Mode Pro:** Diseño cuidado con estética neón/cyberpunk.
* **Vinilos Animados:** Las tarjetas de canciones giran como discos reales al reproducirse.
* **Editor de Ondas:** Recorte visual de audio (WaveSurfer.js) al momento de subir canciones.

### 👥 Funciones Sociales
* **Perfiles Públicos y Privados:** Control de privacidad estilo Instagram.
* **Interacciones:** Sistema de Seguidores, Likes y Comentarios en tiempo real.
* **Gamificación:** Sistema automático de insignias (Productor, Melómano, Rockstar) basado en el comportamiento del usuario.

### 🛠️ Administración Avanzada
* **Panel de Control (God Mode):** Herramientas para gestión de usuarios y moderación de contenido.
* **Gestión de Archivos:** Limpieza automática de archivos multimedia (`signals`) al eliminar registros de la base de datos.

---

## 📸 Capturas de Pantalla

| Home con IA | DJ Anita (HUD) | Perfil de Usuario |
|:---:|:---:|:---:|
| *[Inserta aquí tu imagen del Home]* | *[Inserta aquí tu imagen de DJ Anita]* | *[Inserta aquí tu imagen del Perfil]* |

---

## 🚀 Instalación y Despliegue

Sigue estos pasos para correr el proyecto en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/TU_USUARIO/NeuroBeats.git](https://github.com/TU_USUARIO/NeuroBeats.git)
    cd NeuroBeats
    ```

2.  **Crear entorno virtual:**
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    *Nota: Se requiere `ffmpeg` instalado en el sistema para el procesamiento de audio.*
    ```bash
    pip install -r requirements.txt
    ```

4.  **Migrar la Base de Datos:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Crear Superusuario:**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Ejecutar servidor:**
    ```bash
    python manage.py runserver
    ```

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python, Django Framework.
* **Frontend:** HTML5, CSS3, Bootstrap 5, FontAwesome.
* **JavaScript:** HTMX (para AJAX/SPA), WaveSurfer.js (visualización de audio).
* **Ciencia de Datos / IA:** Librosa, Numpy.
* **Procesamiento de Audio:** Pydub, FFmpeg.
* **Base de Datos:** SQLite (Dev) / MySQL (Prod).

---

Desarrollado con ❤️ y mucho ☕ por **[Tu Nombre / Tobben]**.