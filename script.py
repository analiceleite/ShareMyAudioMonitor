from flask import Flask, render_template, jsonify, request
import sounddevice as sd
import numpy as np
import threading
import time

app = Flask(__name__)
volume_level = 0
selected_device = None
stream = None 

def audio_callback(indata, frames, time, status):
    global volume_level
    if status:
        print(status)
    volume_level = np.linalg.norm(indata) * 10

def audio_stream():
    global selected_device, stream
    stream = sd.InputStream(device=selected_device, callback=audio_callback)
    stream.start() 
    while True:
        time.sleep(1)

@app.route('/')
def index():
    try:
        devices = sd.query_devices()
        unique_input_devices = []
        added_device_names = set()

        principais_dispositivos = ["Conjunto de Microfones", "External Mic", "Mistura", "Microfone"]

        default_device_id = sd.default.device[0]  
        default_device_name = devices[default_device_id]['name']

        print(f"Dispositivo padrão: {default_device_name}")

        for i, device in enumerate(devices):
            if device['max_input_channels'] > 0: 
                device_name = device['name']

                if (any(termo.lower() in device_name.lower() for termo in principais_dispositivos) or
                    device_name == default_device_name) and device_name not in added_device_names:

                    unique_input_devices.append({'id': i, 'name': device_name})
                    added_device_names.add(device_name) 

                print(f"Dispositivo {i}: {device_name}")

        if not unique_input_devices:
            print("Nenhum dispositivo de entrada relevante encontrado.")
        else:
            print(f"Dispositivos encontrados: {unique_input_devices}")

        return render_template('main.html', devices=unique_input_devices, selected_device=selected_device if selected_device is not None else "Nenhum")
    except Exception as e:
        print(f"Erro ao listar dispositivos: {e}")
        return "Erro ao listar dispositivos"


@app.route('/set_device/<int:device_id>')
def set_device(device_id):
    global selected_device
    selected_device = device_id
    threading.Thread(target=audio_stream, daemon=True).start()
    return jsonify(success=True)

@app.route('/stop_capture', methods=['POST'])
def stop_capture():
    global stream, selected_device
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
    return jsonify(volume=volume_level)

@app.route('/get_selected_device')
def get_selected_device():
    return jsonify(device=selected_device)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug= True)
