import numpy as np
import cv2


def calculate_px_per_cm_using_perimeter(corners,reference_perimeter_cm):

    #calculate the perimeter (from pixels) of the aruco marker
    aruco_perimeter = cv2.arcLength(corners[0], True) 
    print('aruco perimeter:', aruco_perimeter)

    #calculate the pixel per centimeter ratio
    px_per_cm = aruco_perimeter / reference_perimeter_cm

    print('pixel per centimeter: ', px_per_cm)

    return px_per_cm


def calculate_px_per_cm_using_reference(reference_width_cm, reference_height_cm, corners):

    marker = corners[0][0]

    # Marker corners
    top_left = marker[0]
    top_right = marker[1]
    bottom_right = marker[2]
    bottom_left = marker[3]

    # Width in pixels
    top_width = np.linalg.norm(top_right - top_left)
    bottom_width = np.linalg.norm(bottom_right - bottom_left)

    marker_width_pixels = (top_width + bottom_width) / 2

    # Height in pixels
    left_height = np.linalg.norm(bottom_left - top_left)
    right_height = np.linalg.norm(bottom_right - top_right)

    marker_height_pixels = (left_height + right_height) / 2

    # Pixels per cm
    px_per_cm_x = marker_width_pixels / reference_width_cm
    px_per_cm_y = marker_height_pixels / reference_height_cm

    return px_per_cm_x, px_per_cm_y