import threading
import time
from app import app

def start_server():
    def run():
        app.run(port=5000)

    thread = threading.Thread(target=run)
    thread.daemon = True
    thread.start()
    time.sleep(1)