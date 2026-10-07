import cv2
import os
import csv
import pandas as pd
import datetime
import time
from tkinter import messagebox as mess

# ---------------- Helper Functions ----------------

def assure_path_exists(path):
    """Create folder if it doesn't exist."""
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def check_haarcascadefile():
    """Ensure the Haarcascade file exists."""
    if not os.path.isfile("haarcascade_frontalface_default.xml"):
        mess._show(title='File Missing', message='haarcascade_frontalface_default.xml is missing!')
        exit()

# ---------------- Attendance Tracking ----------------
def TrackImages():
    check_haarcascadefile()
    assure_path_exists("Attendance/")
    assure_path_exists("StudentDetails/")

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    trainer_path = "TrainingImageLabel/Trainner.yml"

    if not os.path.isfile(trainer_path):
        mess._show(title='Data Missing', message='Please train the model first!')
        return

    recognizer.read(trainer_path)
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    student_csv = "StudentDetails/StudentDetails.csv"
    if not os.path.isfile(student_csv):
        mess._show(title='Details Missing', message='Students details CSV is missing!')
        return

    df = pd.read_csv(student_csv)

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX

    date_str = datetime.datetime.now().strftime('%d-%m-%Y')
    attendance_file = f"Attendance/Attendance_{date_str}.csv"

    if not os.path.isfile(attendance_file):
        with open(attendance_file, 'w', newline='') as f:
            csv.writer(f).writerow(['Id', '', 'Name', '', 'Date', '', 'Time'])

    marked_this_session = set()

    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)

            serial, conf = recognizer.predict(gray[y:y+h, x:x+w])

            display_name = "Unknown"

            if conf < 50:
                row = df.loc[df['SERIAL NO.'] == serial]

                if not row.empty:
                    ID = str(row['ID'].values[0])
                    display_name = str(row['NAME'].values[0])

                    if ID not in marked_this_session:
                        ts = datetime.datetime.now()
                        attendance = [
                            ID, '',
                            display_name, '',
                            ts.strftime('%d-%m-%Y'), '',
                            ts.strftime('%H:%M:%S')
                        ]

                        with open(attendance_file, 'a', newline='') as f:
                            csv.writer(f).writerow(attendance)

                        marked_this_session.add(ID)

            cv2.putText(im, display_name, (x, y+h), font, 1, (255, 255, 255), 2)

        cv2.imshow('Taking Attendance', im)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


# ---------------- Main ----------------
if __name__ == "__main__":
    TrackImages()
