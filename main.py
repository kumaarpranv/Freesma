import warnings
warnings.filterwarnings("ignore")
import os
from flask import Flask, flash, request, redirect, url_for,render_template
from werkzeug.utils import secure_filename
from neural_style_transfer import *
import cv2
import random
import string

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html',imgurl=None)

@app.route('/img')
def img():
    return render_template('post.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        
        file=request.files['file']
        print(file.filename)
        
        if 'file' not in request.files:
            return "hello1"
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            imgpath=os.path.join(UPLOAD_FOLDER, filename)
            file.save(imgpath)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #modelpath="models/instance_norm/candy.t7"
            modelpath=str(request.form.get('model'))
            ext=randomString(10)+"-output.png"
            generate_output(imgpath,modelpath,ext)
            imgname, imgext = os.path.splitext(imgpath)
            
            print(imgname)
            return render_template('index.html',imgurl=imgname+ext) #redirect(url_for('uploaded_file',filename=filename))
        
    else:
        return redirect(url_for('/'))

@app.route('/img')
def showimg():
    return render_template('post.html')


if __name__ == '__main__':
   app.run(debug = True)