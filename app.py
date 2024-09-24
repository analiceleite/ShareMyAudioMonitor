from flask import Flask, render_template, jsonify, request
import sounddevice as sd
import numpy as np
import threading
import time

app = Flask(__name__)
volume_level = 0
selected_device = None


def audio_callback(indata, frames, time, status):
    global volume_level
    if status:
        print(status)
    volume_level = np.linalg.norm(indata) * 10


def audio_stream():
    global selected_device
    with sd.InputStream(device=selected_device, callback=audio_callback):
        while True:
            time.sleep(1)


@app.route('/')
def index():
    devices = sd.query_devices()
    input_devices = [i for i, device in enumerate(
        devices) if device['max_input_channels'] > 0]
    return render_template('index.html', devices=input_devices, selected_device=selected_device)


@app.route('/set_device/<int:device_id>')
def set_device(device_id):
    global selected_device
    selected_device = device_id
    threading.Thread(target=audio_stream, daemon=True).start()
    return jsonify(success=True)


@app.route('/get_volume')
def get_volume():
    return jsonify(volume=volume_level)


@app.route('/get_selected_device')
def get_selected_device():
    return jsonify(device=selected_device)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Remova ssl_context
