import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "abc"  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print("A REQUEST")
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if "." not in file.filename:
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],"latest.pdf"))
            file_object = open('history.txt', 'w')
            file_object.write(f"{filename}\n")
            file_object.close()
            return redirect(url_for('upload_file', name=filename))
    with open('history.txt', 'r') as f:
        last_line = f.readlines()[-1]
 
    return f'''
    <!doctype html>
    <br>
    <hr>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload
      style='''+'''
      {width:100}
      >
    </form>
    <hr>
    <h1>Current Latest File : '''+f'''{last_line}</h1>
    '''
@app.route('/latest', methods=['GET'])
def get_latest():
    with open('history.txt', 'r') as f:
        last_line = f.readlines()[-1]
    return last_line