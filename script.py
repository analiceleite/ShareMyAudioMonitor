from flask import Flask, render_template, jsonify, request
import sounddevice as sd
import numpy as np
import threading
import time

app = Flask(__name__)
volume_level = 0
selected_device = None
stream = None  # Variável global para o stream

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
    input_devices = [
        {'id': i, 'name': device['name']}
        for i, device in enumerate(devices) if device['max_input_channels'] > 0
    ]
    return render_template('main.html', devices=input_devices, selected_device=selected_device if selected_device is not None else "Nenhum")

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
