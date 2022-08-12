#https://techtutorialsx.com/2017/05/02/python-opencv-face-detection-and-counting/
import cv2
import numpy as np
# import dlib #trying to donwload, need admin?

# CascadeClassifier object receives the classifier as input
face_cascade = cv2.CascadeClassifier('FaceDetection/haarcascade_frontalface_default.xml')

# img = cv2.imread('sample_media/goldie.jpg')
# img = cv2.imread('sample_media/Geography.jpg')
img = cv2.imread('sample_media/people.jpg')

# In order to apply classification, images must be greyscale
# RGB -> COLOR_BGR2GRAY
grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Pass greyscale and return detected objects as rectangles
# Can also add scaleFactor and minSize parameters
# when no match found, empty tuple is returned
faces = face_cascade.detectMultiScale(grayImg)

# Checking length of detectMultiScale return tuple
print(type(faces))
if len(faces) == 0:
    print("No faces found")
    
else:
    # Iterate results and draw rectangles onto the original image
    # Recieves the initial and final rectangles vertexes, RGB colour and thickness 
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h), (0,255,0),1)

    # Adding number of faces detected in the image

    cv2.imshow("Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # N rows means N faces detected 
    # Matrix of N rows and 4 columns for the rectangle dimensions of each face
    print(faces.shape)
    print("Number of faces detected:", str(faces.shape[0]))
