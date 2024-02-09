from flask import Flask, render_template
from flask_socketio import SocketIO
import RPi.GPIO as GPIO

app = Flask(__name__)
socketio = SocketIO(app)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pins = {'button1': 17, 'button2': 27, 'button3': 22, 'button4': 23}
#pins = {'UP': 17, 'DOWN': 27, 'LEFT': 22, 'RIGHT': 23}


for pin in pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

@app.route('/')
def index():
    return render_template('index.html')  # Serve the webpage

@socketio.on('relay_event')
def handle_relay_event(json):
    print(json)
    button_id = json['button_id']
    action = json['action']
    if button_id in pins:
        GPIO.output(pins[button_id], GPIO.HIGH if action == 'on' else GPIO.LOW)
        print(button_id)
    elif button_id == "recenter":
        if action == 'on':
            print(button_id)
            # Code here to use IMU to recenter dish to 0 position

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
