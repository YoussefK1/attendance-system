import cv2
import os
import numpy as np
from PIL import Image

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []
    for imagePath in imagePaths:
        pilImage = Image.open(imagePath).convert('L')  # grayscale
        imageNp = np.array(pilImage, 'uint8')
        ID = int(os.path.split(imagePath)[-1].split(".")[1])  # read ID from filename
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

def trainImages():
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)

    faces, Ids = getImagesAndLabels("TrainingImage")
    if len(faces) == 0:
        print("No images found! Please add images to TrainingImage/")
        return

    recognizer.train(faces, np.array(Ids))
    recognizer.save("TrainingImageLabel/Trainner.yml")
    print(f"[INFO] Training complete. {len(set(Ids))} people trained.")

if __name__ == "__main__":
    trainImages()
