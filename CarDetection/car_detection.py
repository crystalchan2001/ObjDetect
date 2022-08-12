import cv2
# Example with cars on motorway
cap = cv2.VideoCapture('sample_media/motorway.avi')
# Example with no cars which still detects some light as cars
# cap = cv2.VideoCapture('sample_media/world.mp4')
# Trained XML classifiers 
car_cascade = cv2.CascadeClassifier('CarDetection/cars.xml')

while True:
    ret, frames = cap.read()

    grey = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY) #convert frames to grey scale
    cars = car_cascade.detectMultiScale(grey, 1.1, 1) #detect different sized cars in input image

    # draw rectangle around each car
    for (x,y,w,h) in cars:
        cv2.rectangle(frames, (x,y), (x+w, y+h), (0,255,255), 2)

    cv2.imshow('Detection Video', frames)

    if cv2.waitKey(30) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()