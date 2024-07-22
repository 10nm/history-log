import os.path
import requests

import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def get_bash_history():
    command = ""
    timestamp = ""
    with open(os.path.expanduser('~/.bash_history'), 'r') as file:
        result = file.read()
    result = result.splitlines()
    result = result[-2:]

    command = result[1]
    timestamp = datetime.datetime.fromtimestamp(int(result[0][1:]))

    print(command)
    print(timestamp)
    return command , timestamp

def main():
    command, timestamp = get_bash_history()
    data = {
        'command': command,
        'timestamp': str(timestamp)
    }
    url = 'http://localhost:5000/history'
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        print('送信成功')
    else:
        print('送信失敗')
global flag
flag = True
class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global flag
        if event.src_path == os.path.expanduser('~/.bash_history'):
            if flag:
                flag = False
                pass
            else:
                main()
                flag = True
                pass

if __name__ == '__main__':
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.expanduser('~'), recursive=False)
    observer.start()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()