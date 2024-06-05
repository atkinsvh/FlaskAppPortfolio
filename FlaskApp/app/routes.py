from flask import render_template, request, redirect, url_for, send_from_directory
import os
from app import app
from werkzeug.utils import secure_filename
import logging
from process_data import process_data, generate_heatmap

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        # Check if the POST request has the file part
        if 'file' not in request.files:
            logging.error("No file part in request")
            return redirect(request.url)
        
        file = request.files['file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            logging.error("No selected file")
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            logging.debug(f"File saved to {file_path}")

            try:
                # Process the uploaded file and generate graph
                graph_path = process_data(file_path)
                return render_template('projects.html', graph_path=graph_path, map_path=None)
            except KeyError as e:
                error = str(e)
    
    return render_template('projects.html', graph_path=None, map_path=None, error=error)

@app.route('/heatmap', methods=['GET', 'POST'])
def heatmap():
    error = None
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                generate_heatmap(file_path)
                map_path = os.path.join(app.config['UPLOAD_FOLDER'], 'heatmap.html')
                return render_template('projects.html', graph_path=None, map_path=map_path)
            except Exception as e:
                error = str(e)
    return render_template('projects.html', graph_path=None, map_path=None, error=error)

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_from_directory('app/static', filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Error in download_file route: {e}")
        return "File not found", 404
