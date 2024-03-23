from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
import numpy as np
from werkzeug.utils import secure_filename
from count import count_colonies_within_petri_dish
import os
import base64

app = Flask(__name__)
CORS(app)

# Set the path for the uploads
UPLOAD_FOLDER = '/Users/viraatd/Documents/Personal/ColonyCounter/backend/uploads'
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

        # Assuming this function returns an image array and a count
        result_image, count = count_colonies_within_petri_dish(image_path)
        
        # Convert the processed image to Base64
        _, buffer = cv2.imencode('.jpg', result_image)
        img_str = base64.b64encode(buffer).decode()

        # Instead of saving the result image, you encode and send it in the response
        return jsonify({
            'colony_count': count,
            'result_image_base64': img_str
        })
    
if __name__ == '__main__':
    app.run(debug=True)
