from flask import Flask, jsonify, Response, request
from flask_cors import CORS
import logging
from typing import Dict, Tuple

dags = {}

# Create a Flask app instance
app = Flask(__name__)

# Enable CORS
CORS(app, origins=["*"], supports_credentials=True)

# Initialize logger
logging.basicConfig(filename="server.log", 
                    level=logging.INFO, 
                    format="%(asctime)s %(levelname)-9s %(message)s", 
                    datefmt="%Y-%m-%d %H:%M")
logger = logging.getLogger()
logging.getLogger().name = "server"

@app.route('/', methods=['GET'])
def read_root() -> Response:
    # return jsonify({'message': 'This is root!'})
    return jsonify(dags)

@app.route('/init', methods=['POST'])
def get_dag():
    try:
        data = request.json
        dag_id, dag_data = data['dag_id'], data['dag_data']
        dags[dag_id] = dag_data
    except Exception as err:
        logger.error(err)
        return jsonify({'message': f'Save dag "{dag_id}" failed!'})
    logger.info(f'Save {dag_id} successfully!')
    return jsonify({'message': f'Save dag "{dag_id}" successfully!'})

if __name__ == '__main__':
    app.run(port=8000)
