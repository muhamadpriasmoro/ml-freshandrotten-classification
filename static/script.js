document.getElementById('imageInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const preview = document.getElementById('imagePreview');
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
        reader.readAsDataURL(file);
    }
});

document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            const prediction = document.getElementById('predictionResult');
            const confidence = document.getElementById('confidenceResult');
            const preview = document.getElementById('imagePreview');

            preview.src = 'data:image/png;base64,' + data.image;
            prediction.textContent = 'Prediction: ' + data.prediction;
            confidence.textContent = 'Confidence: ' + data.confidence;
            
            prediction.style.display = 'block';
            confidence.style.display = 'block';
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
