""" Experiment with face detection and image filtering using OpenCV """

import numpy as np
import cv2


face_cascade = cv2.CascadeClassifier(
    '/home/charles/OpenCV/opencv-2.4.11/data/haarcascades/haarcascade_frontalface_alt.xml')
kernel = np.ones((21, 21), 'uint8')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.2, minSize=(20, 20))
    for (x, y, w, h) in faces:
        frame[y:y + h, x:x + w, :] = cv2.dilate(frame[y:y + h, x:x + w, :], kernel)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255))

    # Display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()