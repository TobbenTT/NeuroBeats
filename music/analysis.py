import librosa
import numpy as np

def analyze_audio(file_path):
    try:
        # 1. Cargar el audio
        y, sr = librosa.load(file_path, duration = 60)

        # 2 calcular BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        # 3 Calcular Energia
        rms = librosa.feature.rms(y=y)
        energy = np.mean(rms)

        #convertir a valores simples
        bpm_val = int(round(tempo)) if isinstance(tempo, float) else int(tempo[0])
        energy_val = round(float(energy), 4)

        print(f"Analisis IA Completado: BPM={bpm_val} | Energia={energy_val}")
        return bpm_val, energy_val

    except Exception as e:
        print(f"Error analizando audio: {e}")
        return None, None
