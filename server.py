from flask import Flask, request
import requests
import importlib
import json
import shutil
import os
import time
import zipfile
import io
from RoutineData import RoutineData

app = Flask(__name__)
METRICS_ENDPOINT = "http://127.0.0.1:9000/publishMetrics"
FILES_ENDPOINT = "http://127.0.0.1:9000/getFiles"


@app.route('/train', methods=["POST"])
def train():
    try:
        print("Starting")
        # Setup
        data = request.data.decode('utf8')
        data_json = json.loads(data)
        title = data_json['title']
        routine = data_json['routine']
        nextStatus = data_json['nextStatus']
        proj_dir = os.path.join(os.getcwd(), title)

        print("Fetching Files")
        r = requests.post(FILES_ENDPOINT, {"modelName": title, "subDir": ""})
        print("Extracting")
        bytes = io.BytesIO(r.content)
        z = zipfile.ZipFile(bytes)
        z.extractall(proj_dir)
        print("Importing Repo")
        repo = importlib.import_module(title+"."+routine)

        print("Mapping Objects")
        files = []
        for path in os.listdir(proj_dir+"/data"):
            # check if current path is a file
            if os.path.isfile(os.path.join(proj_dir, path)):
                f = open(os.path.join(proj_dir, path), 'w')
                files.append(f)
        params = {
            "config": data_json['config'],
            "files": files
        }

        routineObj = RoutineData(params)
        # Run
        start = time.time()
        print("Running Routine")
        repo.run(routineObj)
        end = time.time()

        # Cleanup
        print("Cleaning")
        for f in files:
            f.close()
        shutil.rmtree(title)
        routinePayload = routineObj.getPayload()
        response_payload = {"status": nextStatus,
                            "title": title,
                            "results": json.dumps(routinePayload['metrics']),
                            "duration": end-start,
                            "time": start}
        resp = requests.post(METRICS_ENDPOINT, response_payload)
        print('Done')
        return json.dumps(resp)
    except Exception as e:
        return {"error": str(e)}


@app.route('/live')
def live():
    return 'Hello, World!'
