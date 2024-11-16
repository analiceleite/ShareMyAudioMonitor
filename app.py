from flask import Flask, render_template, jsonify, request
import sounddevice as sd
import numpy as np
import threading
import time
import os
import sys

app = Flask(__name__)
paused = True
volume_level = -200
selected_device = None
stream = None
SAMPLING_RATE = 48000.0
DISPOSITIVOS_PERMITIDOS = ['Share']

def calcular_db(audio_data):
    rms = np.sqrt(np.mean(np.square(audio_data)))  # Root Mean Square (RMS)
    if rms > 0:
        db = 20 * np.log10(rms)
    else:
        db = -np.inf  # Valor mínimo possível para silêncio
    return db

def audio_callback(indata, frames, time, status):
    global volume_level
    if status:
        print(status)
    volume_level = calcular_db(indata)

def audio_stream():
    global selected_device, stream
    while True:
        try:
            stream = sd.InputStream(samplerate=SAMPLING_RATE, channels=1, dtype='float32', callback=audio_callback, device=selected_device)
            stream.start()
            while True:
                time.sleep(1)  # Ajuste o tempo de sono conforme necessário
        except Exception as e:
            print(f"Erro no stream: {e}")
            if stream is not None:
                stream.stop()
                stream.close()
                stream = None
            time.sleep(1)  # Aguarde um segundo antes de tentar novamente

@app.route('/')
def index():
    dispositivos_api = sd.query_hostapis()
    dispositivos_array = sd.query_devices()
    
    for entry in dispositivos_api:
        if entry['name'] == 'Windows DirectSound':
            dispositivos_id = entry['devices']
    
    dispositivos_entrada = [
        d for d in dispositivos_array if d['max_input_channels'] > 0]

    dispositivos_filtrados = []
    for dispositivo_entrada in dispositivos_entrada:
        if any(termo.lower() in dispositivo_entrada['name'].lower() for termo in DISPOSITIVOS_PERMITIDOS) \
                and dispositivo_entrada['index'] in dispositivos_id:
            dispositivos_filtrados.append({
                'id': dispositivo_entrada['index'],
                'name': dispositivo_entrada['name'],
            })
    print(dispositivos_filtrados)
    return render_template('main.html', devices=dispositivos_filtrados, selected_device=selected_device if selected_device is not None else "Nenhum")

@app.route('/set_device/<int:device_id>')
def set_device(device_id):
    global selected_device, paused
    paused = False
    if not device_id == selected_device:
        selected_device = device_id
        threading.Thread(target=audio_stream, daemon=True).start()
    return jsonify(success=True)

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    global stream, selected_device
    global paused
    paused = True
    if stream is not None:
        print("Parando a captação...")
        stream.stop()
        stream.close()  
        print("Captação parada.")
        stream = None
        selected_device = None 
    return jsonify(success=True)

@app.route('/get_volume')
def get_volume():
    global paused, volume_level
    if paused is True:
        volume_level = -200
    return jsonify(volume=float(volume_level))

@app.route('/get_selected_device')
def get_selected_device():
    return jsonify(device=selected_device)

@app.route('/restart')
def restart_server():
    os.execv(sys.executable, ['python'] + sys.argv)
    return jsonify(success=True)

if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', port=5000, debug=True)
        except SystemExit:
            print("O servidor Flask foi encerrado. Tentando reiniciar...")
            time.sleep(1) 
        except Exception as e:
            print(f"Erro na execução da aplicação: {e}")
            time.sleep(1)