from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import webapp_constants
import os
from concurrent.futures import ThreadPoolExecutor
import uuid
import time

import sys
sys.path.append('../')
from mastering import master

executor = ThreadPoolExecutor(1)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = webapp_constants.UPLOAD_FOLDER

'''
embeddings = index_embeddings.IndexEmbeddings(38)
embeddings.create_index()

'''

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

    # Process file in background thread
    executor.submit(process_file, filename)

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

def process_file(filename):
    print("STARTING MASTERING")
    master.master(filename)
    print("MASTERING DONE")


if __name__ == '__main__':
    app.run(debug=True)
