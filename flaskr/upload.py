from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, send_from_directory
)
from werkzeug.utils import secure_filename
from . import auth
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

bp = Blueprint('uploads', __name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_files():
    import os
    path = os.getcwd() + "/uploads"
    list_of_files = []

    for filename in os.listdir(path):
        list_of_files.append(filename)

    return list_of_files


@bp.route('/upload', methods=['GET', 'POST'])
@auth.login_required
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(request.url)
        else:
            flash('Not allowed file type.')
            return redirect(request.url)
    return render_template('upload/upload.html', files=get_files())


@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
