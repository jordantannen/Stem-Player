import os

# Import necessary functions from Flask and Spleeter
from flask import Flask, redirect, render_template, request,  url_for, send_file, send_from_directory
from werkzeug.utils import secure_filename
from spleeter.separator import Separator

# Set current file as Flask app
app = Flask(__name__)

# Configure upload location
UPLOAD_FOLDER = '/home/jordan/CS50/stem-player/uploads/'
STEM_FOLDER = ''
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'wav', 'mp3'}

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensures file is correct type
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Stop cache
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Index function
@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":

        # Ensure proper file was uploaded
        if 'file' not in request.files:
            return render_template("index.html", error_message=True)

        # Save song to variable
        song = request.files["file"]

        # Ensure file was uploaded
        if song.filename == "":
            return render_template("index.html", error_message=True)

        if song and allowed_file(song.filename):
            # Create new spleeter object
            separator = Separator('spleeter:4stems')

            # Save create secure filename
            filename = secure_filename(song.filename)

            # Set save path and save file
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            song.save(audio_path)

            # Split song and save to path
            separator.separate_to_file(audio_path, UPLOAD_FOLDER)

            # Set location for stems
            global STEM_FOLDER
            STEM_FOLDER = UPLOAD_FOLDER + str(filename).replace(".mp3", "")

            # File list for stem output 
            file_list = ["bass.wav", "drums.wav", "other.wav", "vocals.wav"]

            return render_template("player.html", file_list=file_list)

    else:
        return render_template("index.html")

@app.route('/uploads/<filename>')
def send_file(filename):

    # Stem folder
    global STEM_FOLDER

    return send_from_directory(STEM_FOLDER, filename)