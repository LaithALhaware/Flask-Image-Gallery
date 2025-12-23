from flask import Flask, render_template, request, redirect, url_for, send_file, session, flash
from functools import wraps
import os
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename
import shutil  # <-- needed for moving files
from urllib.parse import unquote
import subprocess


import base64


app = Flask(__name__)

BASE_UPLOAD_FOLDER = 'static/Uploads'
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = BASE_UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp', 'mp4', 'avif'}

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
    
VIDEO_EXTENSIONS = ['mp4', 'mov', 'avi', 'webm', 'mkv']



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


THUMBNAIL_FOLDER = os.path.join('static', 'Thumbnails')  # new folder for thumbnails

def generate_video_thumbnail(video_path, thumb_path):
    """Generate a thumbnail for a video using ffmpeg."""
    os.makedirs(os.path.dirname(thumb_path), exist_ok=True)
    if not os.path.exists(thumb_path):
        subprocess.run([
            'ffmpeg', '-y', '-i', video_path, '-ss', '00:00:01.000', '-vframes', '1', thumb_path
        ])



def get_folder_size(path):
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            fp = os.path.join(root, f)
            if os.path.exists(fp):
                total += os.path.getsize(fp)
    return total
    
def human_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024


@login_required
@app.route('/', methods=['GET', 'POST'])
def index():
    album = request.args.get('album', '')  # optional album filter

    os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(THUMBNAIL_FOLDER, exist_ok=True)  # ensure thumbnail folder exists

    albums_info = {}

    for d in os.listdir(BASE_UPLOAD_FOLDER):
        album_path = os.path.join(BASE_UPLOAD_FOLDER, d)
        if os.path.isdir(album_path):
            count = 0
            size_bytes = 0
            for f in os.listdir(album_path):
                file_path = os.path.join(album_path, f)
                ext = f.rsplit('.', 1)[-1].lower()
                if allowed_file(f) or ext in VIDEO_EXTENSIONS:
                    count += 1
                    size_bytes += os.path.getsize(file_path)
            albums_info[d] = {
                'file_count': count,
                'size_bytes': size_bytes,
                'size_human': human_size(size_bytes)
            }

    # Handle file uploads
    if request.method == 'POST' and 'file' in request.files:
        files = request.files.getlist('file')
        target_album = album or 'Default'
        album_path = os.path.join(BASE_UPLOAD_FOLDER, target_album)
        os.makedirs(album_path, exist_ok=True)
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(album_path, filename))
        return redirect(url_for('index', album=album))

    # Ensure selected album folder exists
    if album:
        album_path = os.path.join(BASE_UPLOAD_FOLDER, album)
        os.makedirs(album_path, exist_ok=True)

    # Collect images/videos
    images = []
    selected_albums = [album] if album else albums_info
    for alb in selected_albums:
        alb_path = os.path.join(BASE_UPLOAD_FOLDER, alb)
        for f in os.listdir(alb_path):
            ext = f.split('.')[-1].lower()
            if allowed_file(f) or ext in VIDEO_EXTENSIONS:
                file_data = {'album': alb, 'filename': f}

                if ext in VIDEO_EXTENSIONS:
                    # Thumbnail in separate folder
                    thumb_filename = f"{alb}_{f.rsplit('.', 1)[0]}_thumb.jpg"
                    thumb_path = os.path.join(THUMBNAIL_FOLDER, thumb_filename)
                    generate_video_thumbnail(os.path.join(alb_path, f), thumb_path)
                    file_data['thumbnail'] = os.path.join('Thumbnails', thumb_filename)
                    file_data['is_video'] = True
                else:
                    file_data['thumbnail'] = f
                    file_data['is_video'] = False

                images.append(file_data)

    # Sort by modification time (newest first)
    images.sort(
        key=lambda x: os.path.getmtime(os.path.join(BASE_UPLOAD_FOLDER, x['album'], x['filename'])),
        reverse=True
    )
    
    

    size_bytes = get_folder_size('static')
    size_human = human_size(size_bytes)
        
    return render_template(
        'index.html',
        images=images,
        albums=albums_info,
        current_album=album,
        total_images=len(images),
        size_gb=size_human
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

    delet_folder = os.path.join('static', 'Delet')  # preserve album structure
    os.makedirs(delet_folder, exist_ok=True)

    selected_images = request.form.getlist('selected_images')
    for img in selected_images:
        img_path = os.path.join(BASE_UPLOAD_FOLDER, img)  # full path from static/Uploads/...
        print('------------------------------------')
        print(img_path)
        if os.path.exists(img_path):
            dest_subfolder = os.path.join('static', 'Delet')
            os.makedirs(dest_subfolder, exist_ok=True)
            dest_path = os.path.join(dest_subfolder, os.path.basename(img))
            shutil.move(img_path, dest_path)  # move file

    return redirect(url_for('index', album=album))




@app.route('/MoveSelected', methods=['POST'])
@login_required
def MoveSelected():
    target_album = request.form.get('target_album')
    if not target_album:
        return redirect(url_for('index'))

    target_path = os.path.join(BASE_UPLOAD_FOLDER, target_album)
    os.makedirs(target_path, exist_ok=True)

    selected_files = request.form.getlist('selected_images')

    for file_rel_path in selected_files:
        # file_rel_path example: "Default/2.mp4"
        src_file = os.path.join(BASE_UPLOAD_FOLDER, file_rel_path)

        filename = os.path.basename(file_rel_path)
        dst_file = os.path.join(target_path, filename)

        print('--------------------------')
        print(f'{target_album} From {src_file} To {dst_file}')

        if os.path.exists(src_file):
            shutil.move(src_file, dst_file)

    return redirect(url_for('index', album=target_album))






@app.route('/DeletImage', methods=['POST'])
@login_required
def DeletImage():
    imagName = request.form.get('imagName')
    imagName = unquote(imagName)

    
    # Full source path
    src_path = os.path.join(os.getcwd(), imagName)
    
    if not os.path.exists(src_path):
        return "File does not exist : " + src_path, 404

    # Destination folder
    delet_folder = os.path.join(os.getcwd(), "static/Delet")
    os.makedirs(delet_folder, exist_ok=True)
    
    # Move the file to Delet folder
    dest_path = os.path.join(delet_folder, os.path.basename(src_path))
    shutil.move(src_path, dest_path)
    
    return redirect(url_for('index'))


@app.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')
    album = request.form.get('album', 'Default')
        
    if not file:
        return "No file", 400
    # Sanitize filename
    filename = secure_filename(file.filename)

    # Ensure album folder exists
    album_path = os.path.join(BASE_UPLOAD_FOLDER, str(album))
    os.makedirs(album_path, exist_ok=True)

    # Save the file
    file_path = os.path.join(album_path, filename)
    file.save(file_path)
    return "OK"
    
    

if __name__ == '__main__':
    app.run(debug=True, port=5002)
