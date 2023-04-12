from flask import Flask, request, render_template
import webapp_constants
import os
from concurrent.futures import ThreadPoolExecutor

import sys
sys.path.append('../')

from backend import master

executor = ThreadPoolExecutor(1)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = webapp_constants.UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods = ['POST'])
def upload_file():
    # Get request inputs
    file = request.files['file']
    email = request.form['email']


    # Save the file to disk
    filename = file.filename
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Process file in background thread
    executor.submit(process_file, filename)

    # Return a response to the user
    return render_template('upload_done.html')


def process_file(filename):
    print("STARTING MASTERING")
    master.master(filename)
    print("MASTERING DONE")


if __name__ == '__main__':
    app.run(debug=True)
