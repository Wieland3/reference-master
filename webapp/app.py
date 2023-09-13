from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import os
from concurrent.futures import ThreadPoolExecutor
from reference_master.mastering.master import master
from reference_master import constants

executor = ThreadPoolExecutor(1)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = constants.PATH_TO_RAW_SONGS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods = ['POST'])
def upload_file():
    # Get request inputs
    file = request.files['file']

    # Save the file to disk
    filename = file.filename
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
  exists = os.path.isfile(os.path.join(constants.PATH_TO_MASTERED_SONGS, filename))
  return jsonify(exists=exists)

@app.route("/download/<filename>")
def download(filename):
  filename = os.path.join(constants.PATH_TO_MASTERED_SONGS, filename)
  return send_file(filename, as_attachment=True)

def process_file(filename):
    print("STARTING MASTERING")
    master(filename, "11 - Circle With Me.mp3")
    print("MASTERING DONE")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
