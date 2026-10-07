import cv2
import os
import csv

student_details_path = "StudentDetails"
student_csv = os.path.join(student_details_path, "StudentDetails.csv")

if not os.path.exists(student_details_path):
    os.makedirs(student_details_path)

# Create CSV if not exists
if not os.path.isfile(student_csv):
    with open(student_csv, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['SERIAL NO.', 'ID', 'NAME'])


def TakeImages(name, Id):
    serial = 1
    with open(student_csv, 'r') as f:
        serial = sum(1 for _ in f) - 1
    serial += 1


    dataset_path = "TrainingImage"

    if not os.path.exists(dataset_path):
        os.makedirs(dataset_path)

    cam = cv2.VideoCapture(0)
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    sampleNum = 0
    max_samples = 300

    print(f"[INFO] Capturing images for {name}... Press 'q' to quit early.")

    while True:
        ret, img = cam.read()
        if not ret:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            sampleNum += 1
            face_img = gray[y:y+h, x:x+w]

            face_img = cv2.resize(face_img, (200, 200))
            face_img = cv2.equalizeHist(face_img)

            cv2.imwrite(
                os.path.join(
                    dataset_path,
                    f"{name}.{serial}.{Id}.{sampleNum}.jpg"
                ),
                face_img
            )

        cv2.imshow("Taking Images", img)

        if cv2.waitKey(300) & 0xFF == ord('q'):
            break

        if sampleNum >= max_samples:
            break

    cam.release()
    with open(student_csv, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([serial, Id, name])

    cv2.destroyAllWindows()
    print(f"[INFO] Finished capturing {sampleNum} images for {name}.")
