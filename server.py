from flask import Flask, request, jsonify
from ml import YoloModel
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

yolo_model = YoloModel()


@app.route('/', methods=['POST'])
def home_post():
    return '/'


@app.route('/api/upload', methods=['POST'])
def upload_file():
    print('[POST]')

    files = []
    for i in request.files.items():
        files.append(list(i))

    print({"files": files})

    answers = yolo_model.multi_process(files)
    return jsonify({'answers': answers})


if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
