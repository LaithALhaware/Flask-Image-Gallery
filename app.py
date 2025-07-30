from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import zipfile
from io import BytesIO
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/Uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'file' in request.files:
        files = request.files.getlist('file')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('index'))

    folder = app.config['UPLOAD_FOLDER']
    images = [
        f for f in os.listdir(folder)
        if allowed_file(f) and os.path.isfile(os.path.join(folder, f))
    ]
    # Sort by last modified time (newest first)
    images.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)

    total_images = len(images)
    return render_template('index.html', images=images, total_images=total_images)

@app.route('/download', methods=['POST'])
def download():
    selected_images = request.form.getlist('selected_images')
    if not selected_images:
        return redirect(url_for('index'))

    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w') as zf:
        for img in selected_images:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], img)
            if os.path.exists(img_path):
                zf.write(img_path, img)
    zip_buffer.seek(0)

    return send_file(zip_buffer, as_attachment=True, download_name='selected_images.zip', mimetype='application/zip')



@app.route('/DeletSelected', methods=['POST'])
def DeletSelected():
    selected_images = request.form.getlist('selected_images')
    if not selected_images:
        return redirect(url_for('index'))

    for img in selected_images:
        img_path = os.path.join(app.config['UPLOAD_FOLDER'], img)
        if os.path.exists(img_path):
            os.remove(img_path)  # Delete the file

    return redirect('/test/' + url_for('index'))  # Redirect back to the main page




if __name__ == '__main__':
    app.run(debug=True, port=5002)
