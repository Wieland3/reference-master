from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import webapp_constants
import os
from google.cloud import tasks_v2
import uuid

import sys
sys.path.append('../')
from mastering import master

# Set up Google Cloud Tasks client
client = tasks_v2.CloudTasksClient()
parent = client.queue_path('reference-master-392511', 'europe-west1', 'master-bg-process')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = webapp_constants.UPLOAD_FOLDER


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods = ['POST'])
def upload_file():
    # Get request inputs
    file = request.files['file']

    id = str(uuid.uuid4())

    # Save the file to disk
    filename = id + '.wav'
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Create a task
    task = {
        'http_request': {
            'http_method': 'POST',
            'url': 'https://reference-master-xeb4mvg7na-lz.a.run.app/process/' + filename
        }
    }
    client.create_task(request={"parent": parent, "task": task})

    # Return a response to the user
    return redirect(url_for('upload_done', filename=filename))

@app.route('/uploaded/<filename>')
def upload_done(filename):
    return render_template('upload_done.html', filename=filename)

@app.route("/check_file/<filename>")
def check_file(filename):
  exists = os.path.isfile(os.path.join("../mastered", filename))
  return jsonify(exists=exists)

@app.route("/download/<filename>")
def download(filename):
  filename = os.path.join("../mastered", filename)
  return send_file(filename, as_attachment=True)

@app.route('/process/<filename>', methods=['POST'])
def process_file(filename):
    print("STARTING MASTERING")
    master.master(filename)
    print("MASTERING DONE")
    return 'Mastering done', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
