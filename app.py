from flask import Flask, request, render_template, jsonify
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image as img_preprocessing
import numpy as np
import base64
import os

app = Flask(__name__)

# Load the model
model = load_model('my_model.h5')

# Define the class labels
class_labels = ['Fresh Apple', 'Fresh Banana', 'Fresh Cucumber', 'Fresh Okra', 'Fresh Orange', 
                'Fresh Potato', 'Fresh Tomato', 'Rotten Apple', 'Rotten Banana', 'Rotten Cucumber', 
                'Rotten Okra', 'Rotten Orange', 'Rotten Potato', 'Rotten Tomato']

def prepare_image(file):
    # Save the uploaded file temporarily
    temp_filepath = f"uploads/{file.filename}"  # Define a temporary path
    file.save(temp_filepath)

    img = img_preprocessing.load_img(temp_filepath, target_size=(224, 224))
    # Convert the image to a numpy array
    img_array = img_preprocessing.img_to_array(img)
    # Expand the dimensions to match the input shape of the model
    img_array = np.expand_dims(img_array, axis=0)
    # Normalize the image
    img_array = img_array / 255.0
    return img_array, temp_filepath

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Ensure an image was properly uploaded to our endpoint
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No file name provided'})

    try:
        # Prepare the image
        image, temp_filepath = prepare_image(file)

        # Make predictions
        preds = model.predict(image)

        # Get the index of the class with highest probability
        pred_class_idx = np.argmax(preds, axis=1)[0]

        # Get the class label
        pred_class_label = class_labels[pred_class_idx]

        # Get the confidence score
        confidence = preds[0][pred_class_idx] * 100

        # Encode image to base64
        with open(temp_filepath, "rb") as img_file:
            encoded_img = base64.b64encode(img_file.read()).decode('utf-8')

        # Clean up the temporary file
        os.remove(temp_filepath)

        return jsonify({
            'prediction': pred_class_label,
            'confidence': f'{confidence:.2f}%',
            'image': encoded_img
        })

    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'})

if __name__ == '__main__':
    app.run(debug=True)
