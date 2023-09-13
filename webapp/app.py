from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import webapp_constants
import os
from google.cloud import tasks_v2, storage
import uuid

import sys
sys.path.append('../')
from reference_master.mastering import master

# Set up Google Cloud Storage client
storage_client = storage.Client()
BUCKET_NAME = 'reference-master-bucket'

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
    blob = storage_client.bucket(BUCKET_NAME).blob(filename)
    blob.upload_from_file(file)

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
    blob = storage_client.bucket(BUCKET_NAME).get_blob('mastered' + filename)
    if blob is not None:
        return jsonify(exists=True)
    else:
        return jsonify(exists=False)


@app.route("/download/<filename>")
def download(filename):
    mastered_filename = 'mastered' + filename
    blob = storage_client.bucket(BUCKET_NAME).get_blob(mastered_filename)
    blob.download_to_filename(os.path.join("../mastered", mastered_filename))
    mastered_filepath = os.path.join("../mastered", mastered_filename)
    return send_file(mastered_filepath, as_attachment=True)


@app.route('/process/<filename>', methods=['POST'])
def process_file(filename):

    blob = storage_client.bucket(BUCKET_NAME).get_blob(filename)
    blob.download_to_filename(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    master.master(filename)

    # uploading the mastered file back to GCS
    blob = storage_client.bucket(BUCKET_NAME).blob('mastered' + filename)
    blob.upload_from_filename(os.path.join("../mastered", filename))

    return 'Mastering done', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
