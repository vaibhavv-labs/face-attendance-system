import cv2
import os
import numpy as np
from datetime import datetime

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []
label_map = {}
current_label = 0

base_path = "known_faces"

all_names = []

# Load data
for person_name in os.listdir(base_path):
    person_folder = os.path.join(base_path, person_name)

    label_map[current_label] = person_name
    all_names.append(person_name)

    for image_name in os.listdir(person_folder):
        image_path = os.path.join(person_folder, image_name)

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            continue

        detected_faces = face_cascade.detectMultiScale(img, 1.1, 3)

        for (x, y, w, h) in detected_faces:
            face = img[y:y+h, x:x+w]
            face = cv2.resize(face, (100, 100))

            faces.append(face)
            labels.append(current_label)

    current_label += 1

recognizer.train(faces, np.array(labels))
print("Training Done ✅")

attendance = {name: {"status": "Absent", "time": "--"} for name in all_names}

video = cv2.VideoCapture(0)

print("Press ESC to stop...")

while True:
    ret, frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detected_faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in detected_faces:
        face = gray[y:y+h, x:x+w]
        face = cv2.resize(face, (100, 100))

        label, confidence = recognizer.predict(face)

        name = "Unknown"

        if confidence < 100:
            name = label_map[label]

            if attendance[name]["status"] == "Absent":
                now = datetime.now()
                time_string = now.strftime("%H:%M:%S")

                attendance[name]["status"] = "Present"
                attendance[name]["time"] = time_string

                print(f"{name} marked present at {time_string}")

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, name, (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) == 27:
        break

video.release()
cv2.destroyAllWindows()

# 🔥 PRINT TABLE
print("\nAttendance Summary\n")
print("{:<12} {:<10} {:<10}".format("Name", "Status", "Time"))
print("-"*32)

for name, info in attendance.items():
    print("{:<12} {:<10} {:<10}".format(name, info["status"], info["time"]))

# 🔥 SAVE CSV FILE
file_name = "attendance.csv"

with open(file_name, "w") as f:
    f.write("Name,Status,Time\n")

    for name, info in attendance.items():
        f.write(f"{name},{info['status']},{info['time']}\n")

print(f"\nAttendance saved to {file_name} ✅")