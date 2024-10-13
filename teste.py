import sounddevice as sd
import numpy as np
import time

# Listar dispositivos de entrada
print("Dispositivos de entrada:")
input_devices = sd.query_devices()
for i, device in enumerate(input_devices):
    if device['max_input_channels'] > 0:
        print(f"{i}: {device['name']}")

# Selecionar dispositivo de loopback
input_device_index = int(input("Selecione o índice do dispositivo de loopback: "))

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    volume_norm = np.linalg.norm(indata) * 10
    print(f'Nível de volume (saída): {volume_norm:.2f}')

# Iniciar o stream no dispositivo de loopback
with sd.InputStream(device=input_device_index, callback=audio_callback):
    try:
        while True:
            time.sleep(0.1)  # Espera 100ms
    except KeyboardInterrupt:
        print("\nEncerrando...")
