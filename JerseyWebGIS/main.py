from api.server import app
import os,webbrowser
from multiprocessing import Process

def ui_start():
    print("Start UI......")
    webbrowser.open("http://localhost:8099")
    os.system('python -m http.server 8099 --directory ./ui/config')

if __name__ == "__main__":
    ui_process = Process(target=ui_start)
    ui_process.start()
    app.run(host='0.0.0.0', port=1211)