from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from functools import wraps
import os
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename
import shutil  # <-- needed for moving files

app = Flask(__name__)

BASE_UPLOAD_FOLDER = 'static/Uploads'
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'mp4'}


app.secret_key = "102030405060708090100"

USERS = {
    "admin": "123456",
    "user": "0000"
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username in USERS and USERS[username] == password:
            session['user'] = username
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password")

    return render_template('Login.html')
    
    
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login')) 
    
    

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    album = request.args.get('album', None)  # optional album filter

    # List all albums (create BASE_UPLOAD_FOLDER if it doesn't exist)
    os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
    albums = [
        d for d in os.listdir(BASE_UPLOAD_FOLDER)
        if os.path.isdir(os.path.join(BASE_UPLOAD_FOLDER, d))
    ]

    # If user uploads files
    if request.method == 'POST' and 'file' in request.files:
        files = request.files.getlist('file')
        target_album = album or 'Default'
        album_path = os.path.join(BASE_UPLOAD_FOLDER, target_album)
        os.makedirs(album_path, exist_ok=True)  # create album if not exists
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(album_path, filename))
        return redirect(url_for('index', album=album))

    # Ensure the selected album folder exists even if empty
    if album:
        album_path = os.path.join(BASE_UPLOAD_FOLDER, album)
        os.makedirs(album_path, exist_ok=True)

    # Collect images
    images = []
    if album and album in os.listdir(BASE_UPLOAD_FOLDER):
        # If a specific album is selected, show only its images
        alb_path = os.path.join(BASE_UPLOAD_FOLDER, album)
        for f in os.listdir(alb_path):
            if allowed_file(f):
                images.append({'album': album, 'filename': f})
    else:
        # No album selected → show all images from all albums
        for alb in albums:
            alb_path = os.path.join(BASE_UPLOAD_FOLDER, alb)
            for f in os.listdir(alb_path):
                if allowed_file(f):
                    images.append({'album': alb, 'filename': f})

    # Sort by modification time (newest first)
    images.sort(
        key=lambda x: os.path.getmtime(os.path.join(BASE_UPLOAD_FOLDER, x['album'], x['filename'])),
        reverse=True
    )

    return render_template(
        'index.html',
        images=images,
        albums=albums,
        current_album=album,
        total_images=len(images)
    )


@app.route('/download', methods=['POST'])
@login_required
def download():
    album = request.form.get('album', 'Default')
    album_path = os.path.join(BASE_UPLOAD_FOLDER, album)

    selected_images = request.form.getlist('selected_images')
    if not selected_images:
        return redirect(url_for('index', album=album))

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for img in selected_images:
            img_path = os.path.join(album_path, img)
            if os.path.exists(img_path):
                zf.write(img_path, img)

    zip_buffer.seek(0)
    return send_file(
        zip_buffer,
        as_attachment=True,
        download_name=f'{album}.zip',
        mimetype='application/zip'
    )



@app.route('/DeletSelected', methods=['POST'])
@login_required
def DeletSelected():
    album = request.form.get('album', 'Default')
    album_path = os.path.join(BASE_UPLOAD_FOLDER, album)

    delet_folder = os.path.join('static', 'Delet')  # preserve album structure
    os.makedirs(delet_folder, exist_ok=True)

    selected_images = request.form.getlist('selected_images')
    for img in selected_images:
        img_path = os.path.join(BASE_UPLOAD_FOLDER, img)  # full path from static/Uploads/...
        if os.path.exists(img_path):
            dest_subfolder = os.path.join('static', 'Delet')
            os.makedirs(dest_subfolder, exist_ok=True)
            dest_path = os.path.join(dest_subfolder, os.path.basename(img))
            shutil.move(img_path, dest_path)  # move file

    return redirect(url_for('index', album=album))
    

@app.route('/DeletImage', methods=['POST'])
@login_required
def DeletImage():
    imagName = request.form.get('imagName')
    path_only = '/' + imagName.split('/', 3)[-1]
    
    # Remove the leading '/' and get the relative path
    relative_path = path_only.lstrip('/')
    
    # Full source path
    src_path = os.path.join(os.getcwd(), relative_path)
    
    if not os.path.exists(src_path):
        return "File does not exist", 404

    # Destination folder
    delet_folder = os.path.join(os.getcwd(), "static/Delet")
    os.makedirs(delet_folder, exist_ok=True)
    
    # Move the file to Delet folder
    dest_path = os.path.join(delet_folder, os.path.basename(src_path))
    shutil.move(src_path, dest_path)
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5002)
