import os

from flask import Flask

import time
import random

app = Flask(__name__)

@app.route('/')
def root():
    name = os.environ.get('SERVICE_NAME', 'Unknown')
    exec_time = int(os.environ.get('EXEC_TIME', 5))
    time.sleep(exec_time)
    return f'{random.random()}\n'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))