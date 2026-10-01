import cv2
from object_detector import *
from measurement_utils import *
import numpy as np

REFERENCE_WIDTH_CM = 5
REFERENCE_HEIGHT_CM = 5
REFERENCE_PERIMETER_CM = 20

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50) #load the predefined dictionary
parameters = cv2.aruco.DetectorParameters() #create detector parameters

#Load the object detector
detector = HomogeneousBgDetector()

#capture video from webcam
cap = cv2.VideoCapture(0) 
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #set the width of the video frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #set the height of the video frame

while True: 
    _, img = cap.read() #read the first frame from the webcam

    #detect aruco markers in the image
    detector_aruco = cv2.aruco.ArucoDetector(aruco_dict,parameters) 
    corners, ids, _ = detector_aruco.detectMarkers(img)

    if corners:

        intCorners = np.int32(corners) #convert the float values to integer
        cv2.polylines(img, intCorners, True, (0, 255, 0), 5) #draw polygon lines in green color

        print('aruco ids:', ids)
        # print(corners[0][0][0])

        ############calulate the pixel per centimeter ratio using the perimeter of the aruco marker############
        #px_per_cm = calculate_px_per_cm_using_perimeter(corners, REFERENCE_PERIMETER_CM)

        ############calulate the pixel per centimeter ratio using the reference width and height of the aruco marker############
        px_per_cm_x, px_per_cm_y = calculate_px_per_cm_using_reference(REFERENCE_WIDTH_CM, REFERENCE_HEIGHT_CM, corners)


        contours = detector.detect_objects(img)

        #draw object boundaries
        for cnt in contours:

            #draw the polygon on the original image
            cv2.polylines(img, [cnt], True, (255, 0, 155), 2) #draw polygon lines in pink color

            #get the bounding box of the object
            rect = cv2.minAreaRect(cnt)
            (x, y) , (w, h), angle = rect

            #calculate the width and height of the object in centimeters
            object_width = w / px_per_cm_x  
            object_height = h / px_per_cm_y

            # cv2.boxPoints(rect) for OpenCV 3.x
            box = cv2.boxPoints(rect)  
            box = np.int32(box) #convert to integer

            cv2.circle(img, (int(x), int(y)), 3, (0, 0, 255), -1) #mark the center of the object as red dot 
            cv2.polylines(img, [box], True, (255, 0, 0), 2) #draw box lines in blue color

            #display width and height of the object in green color   
            cv2.putText(img, "W: {:.2f} cm".format(object_width), (int(x), int(y+20)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (50, 80, 250), 2) 
            cv2.putText(img, "H: {:.2f} cm".format(object_height), (int(x), int(y+40)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (50, 80, 250), 2)

            #print(box)

            # print("X: ", x, "Y: ", y)
            # print("Width: ", w, "Height: ", h)
            # print("Angle: ", angle)

    cv2.imshow('Original Image', img)
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break

cap.release()
cv2.destroyAllWindows()
