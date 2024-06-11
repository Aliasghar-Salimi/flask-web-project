from flask import *
from pathlib import Path
import os
import connection
from werkzeug.utils import secure_filename
upload_blueprint = Blueprint('upload_blueprint', __name__,
                              template_folder='templates')

ALLOWED_EXTENSIONS = [ 'png', 'jpg', 'jpeg','txt', 'pdf', 'gif']
cwd = Path.cwd()
UPLOAD_FOLDER = Path.joinpath(cwd, 'media/images')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_blueprint.route('/upload/', methods = ['POST'])  
def upload():  
    # Connect to database
    cnx = connection.connect()
    cursor = cnx.cursor(buffered=True)
    
    file = request.files['file']
    user_id = request.form.get('user_id')


    if request.method == 'POST':  
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, file.filename))
            print(file.filename)

            # Insert filename and user_id into the files table
            query = "INSERT INTO files (filename, user_id) VALUES (%s, %s)"
            cursor.execute(query, (filename, user_id))
            cnx.commit()

            flash(f'file {file.filename} successfully uploaded') 
            return redirect(url_for('user_list'))  
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)
    
    cursor.close()
    cnx.close()