from flask import Flask, request, render_template, g, url_for
import sqlite3
import logging
app = Flask(__name__)

commands = []
timestamps = []
global kp_commands
global kp_timestamps
kp_commands = []
kp_timestamps = []
idx = []
global KEEP
KEEP= []

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
def get_db():
    if "db" not in g:
          g.db = sqlite3.connect('debe.db')
    return g.db  



@app.route('/')
def index():
    global commands
    global timestamps
    global KEEP
    send_this = zip(commands, timestamps)
    return render_template('index.html', send_this=send_this, KEEP=KEEP)

@app.route('/rcv', methods=['POST'])
def receive_id():
    global kp_commands
    global kp_timestamps
    global KEEP
    data = request.get_json()
    idx = data['index']
    idx = int(idx) -1
    logging.debug(idx)
    kp_commands.append(commands[idx])
    kp_commands = sorted(set(kp_commands), key=kp_commands.index)
    kp_timestamps.append(timestamps[idx])
    kp_timestamps = sorted(set(kp_timestamps), key=kp_timestamps.index)
    KEEP = list(zip(kp_commands, kp_timestamps))
    logging.debug(KEEP)
    return "ok"

@app.route('/receive_input', methods=['POST'])
def receive_input():
    data = request.get_json()
    index = data.get('index')
    text = data.get('text')
    logging.debug(text)
    logging.debug(index)
    logging.debug(kp_commands[int(index)-1])
    return "ok"

@app.route('/history', methods=['POST'])
def update():
    global commands
    global timestamps
    global KEEP
    data = request.json
    command = data.get('command', "")
    timestamp = data.get('timestamp', "")

    commands.append(command)
    if len(commands) > 5:
        commands.pop(0)

    timestamps.append(timestamp)
    if len(timestamps) > 5:
        timestamps.pop(0)


    return 'OK'

if __name__ == '__main__':
    app.run(port=5000, debug=True)