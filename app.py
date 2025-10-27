import numpy as np
from PIL import Image
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image as keras_image
from tensorflow.keras import models



app = FastAPI(title="Plant Water Prediction API")
IMG_SIZE = 224

def load_model():
    """Loadsthe VGG16 model."""
    return models.load_model("models/modelvgg16ver2.keras")

print("Loading model...")
model = load_model()
print("Model loaded successfully.")
model.summary()

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()

    img = Image.open(BytesIO(contents))

    if img.mode != "RGB":
        img = img.convert("RGB")

    img = img.resize((IMG_SIZE, IMG_SIZE))

    img_array = keras_image.img_to_array(img)
    img_array_expanded = np.expand_dims(img_array, axis=0)
    preprocessed_img = preprocess_input(img_array_expanded)

    prediction = float(model.predict(preprocessed_img, verbose=0)[0][0])

    if prediction < 0.3:
        label = "Withered"
    elif prediction < 0.7:
        label = "Struggling"
    else:
        label = "Healthy"

    confidence = prediction if prediction >= 0.5 else 1 - prediction
    return {"prediction": label, "confidence": round(confidence, 2)}
