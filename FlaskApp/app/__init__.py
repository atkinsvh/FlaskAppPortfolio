from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads'
app.config['MAX_CONTENT_PATH'] = 16 * 1024 * 1024  # Max upload size is 16MB

from app import routes

