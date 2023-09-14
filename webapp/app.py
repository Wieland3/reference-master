from flask import Flask, request, render_template, redirect, url_for, jsonify, send_file
import os
from concurrent.futures import ThreadPoolExecutor
from reference_master.mastering.master import master
from reference_master import constants

executor = ThreadPoolExecutor(1)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = constants.PATH_TO_RAW_SONGS
app.config['UPLOAD_REF_FOLDER'] = constants.PATH_TO_REFERENCE_SONGS


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods = ['POST'])
def upload_file():
    # Get request inputs
    raw_file = request.files['raw_file']
    ref_file = request.files['ref_file']

    # Save the file to disk
    raw_filename = raw_file.filename
    raw_file.save(os.path.join(app.config['UPLOAD_FOLDER'], raw_filename))

    ref_filename = ref_file.filename
    ref_file.save(os.path.join(app.config['UPLOAD_REF_FOLDER'], ref_filename))

    # Process file in background thread
    executor.submit(process_file, raw_filename, ref_filename)

    # Return a response to the user
    return redirect(url_for('upload_done', filename=raw_filename))

@app.route('/uploaded/<filename>')
def upload_done(filename):
    return render_template('upload_done.html', filename=filename)

@app.route("/check_file/<filename>")
def check_file(filename):
    print(filename)
    exists = os.path.isfile(os.path.join(constants.PATH_TO_MASTERED_SONGS, filename))
    return jsonify(exists=exists)

@app.route("/download/<filename>")
def download(filename):
  filename = os.path.join(constants.PATH_TO_MASTERED_SONGS, filename)
  return send_file(filename, as_attachment=True)

def process_file(filename, ref_filename):
    master(filename, ref_filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
