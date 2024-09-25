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
    stream.start()  # Começa a capturar áudio
    while True:
        time.sleep(1)

@app.route('/')
def index():
    devices = sd.query_devices()
    unique_input_devices = []
    added_device_names = set()

    for i, device in enumerate(devices):
        if device['max_input_channels'] > 0:  # Somente dispositivos de entrada
            device_name = device['name']
            
            # Filtro mais restrito: pega apenas o primeiro "Microfone (Realtek)" e "Mixagem estéreo"
            if ("Microfone (Realtek" in device_name or 
                "Mixagem estéreo" in device_name) and device_name not in added_device_names:
                
                unique_input_devices.append({'id': i, 'name': device_name})
                added_device_names.add(device_name)  # Marca como adicionado para evitar duplicatas

    return render_template('main.html', devices=unique_input_devices, selected_device=selected_device if selected_device is not None else "Nenhum")



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
