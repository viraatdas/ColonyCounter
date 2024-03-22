from flask import Flask, request, jsonify
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from count import count_colonies_within_petri_dish
import os

app = Flask(__name__)

# Set the path for the uploads
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/count-colonies', methods=['POST'])
def count_colonies():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify(error="No selected file"), 400

    if file:
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        result_image, count = count_colonies_within_petri_dish(image_path)
        
        # [You will need to decide how you want to send the result image and count back to the client]
        # For example, you might save the result image and send the path:
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
        cv2.imwrite(result_path, result_image)
        
        return jsonify({
            'colony_count': count,
            'result_image_path': result_path
        })

if __name__ == '__main__':
    app.run(debug=True)
