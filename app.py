from fastapi import FastAPI, UploadFile, File
from tensorflow.keras.applications import VGG16
from tensorflow.keras import models, layers
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np
import os
from PIL import Image
from io import BytesIO
import functools
import tensorflow as tf
from tensorflow.keras.preprocessing import image as keras_image


app = FastAPI(title="Plant Water Prediction API")
IMG_SIZE = 224

def load_image(image_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, [IMG_SIZE, IMG_SIZE])
    return img

@functools.cache

def load_model():

    model = models.load_model('models/modelvgg16.keras')
    print(model.summary())
    return model


@app.post("/predict")


async def predict(file: UploadFile = File(...)):

    contents = await file.read()

    img = Image.open(BytesIO(contents))


    if img.mode != "RGB":
        img = img.convert("RGB")

    img = img.resize((224, 224))

    img_array = keras_image.img_to_array(img)

    img_array_expanded = np.expand_dims(img_array, axis=0)

    preprocessed_img = preprocess_input(img_array_expanded)
    #predictions = model.predict(preprocessed_img)[0][0]

    #with open("image.jpg", "wb") as buffer:

        #buffer.write(await file.read())
    #img= load_image('image.jpg')

    #img_array = np.expand_dims(np.array(img), axis=0)


    model=load_model()

    prediction = float(model.predict(preprocessed_img, verbose=0)[0][0])

    if prediction < 0.3:
        label = "Withered"
    elif prediction < 0.7:
        label = "Struggling"
    else:
        label = "Healthy"

    confidence = prediction if prediction >= 0.5 else 1 - prediction
    return {"prediction": label, "confidence": round(confidence, 2)}
