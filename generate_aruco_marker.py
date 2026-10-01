import cv2

aruco_dict = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_5X5_50
)

marker = cv2.aruco.generateImageMarker(
    aruco_dict,
    23,
    1000
)

cv2.imwrite("resources/marker_23.png", marker)

print("Marker generated")