from transforamtion import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
import os
from convert_heic2png import convert_heic2png



#construction of the argument parser 
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", 
                required = True, 
                help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# convert heic images to png
png_image = convert_heic2png(args["image"])



# =============== Edge detection ===============

#Load the image and compute the ratio of the old height
# to the new height, clone it and resize it

new_height = 500 #The new height will be 500px

image = cv2.imread(png_image)
ratio = image.shape[0] / new_height
original_image = image.copy()
image = imutils.resize(image, height = new_height)

# Wee then need to perform the edge detection with a canny edge detector
# Before hand we need tpo convert the image to a grayscale image and use a
# Gaussian blur filter to smoth the image and cut the high frequency in order 
# to reduce the niose

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0) # Gaussian smoothing with a 5x5 kernel and 0 for the standard deviation
edges = cv2.Canny(gray, 75, 200) # Canny edge detection with a 75 and 200 for the min and max values

print("====== Edge Detection performed ======")

# =============== Finding the contours ===============

#In order to find the corners of the document we need to find the contours
# Hypotesis : The largest contour in the image with 4 points/edges is the document

# To find the contours, we use the cv2.findContours() function. 
# a contour is a curve joining all the continuous points 
# (along the boundary), having same color or intensity
# => for more precision, use a binary image (=threshold image or Canny edge detection)

contours = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#return the list of contours 2nd arg is the contour retrieval mode, 3rd arg is the contour approximation method
# cv2.RETR_LIST retrieves all of the contours without establishing any hierarchical relationships
# cv2.CHAIN_APPROX_SIMPLE removes all redundant points and compresses the contour, thereby saving memory

contours = imutils.grab_contours(contours) # grab the actual contours array from the tuple

contours = sorted(contours, key = cv2.contourArea, reverse=True)[:5] 
# sort the contours by area and keep the 5 largest ones (concording with the hypotesis)

#now that the contours are sorted by area, we need to aoorixmate the contour by a polygon
# with a precision of 0.02 * perimeter of the contour (2% of the perimeter precision)
pourcentage = 0.02 #wee want a 2% precision to the perimeterof our contour
the_contour = None

for contour in contours :
    perimeter = cv2.arcLength(contour, True) #True indicates that the contour is closed
    approximation = cv2.approxPolyDP(contour, pourcentage * perimeter, True)

    if len(approximation)==4: #test if the approximation of the contour has 4 points hence is a rectangle (=document)
        the_contour = approximation
        break
    
if the_contour is None:
    print("===================== No contour found =====================")

else:
    print("====== Contours found ======")

    # =============== Performing the transformation ===============

    # Now we need to perfomr the transfomation to our image.To do so, we use the foura_point_transform function
    # from the transformation.py file. Then we need to convert the image to grayscale, threshold it and apply
    # a thresholding to it

    warped_image = four_point_transform(original_image, the_contour.reshape(4, 2) * ratio)
    # the reshape is necessary because the contour is a 4x1 array and we need a 4x2 array for the function

    # Now lets convert it to a grayscale image and apply a thresholding to it
    warped_image = cv2.cvtColor(warped_image, cv2.COLOR_BGR2GRAY)
    threshold = threshold_local(warped_image, 11, offset = 10, method = "gaussian")
    warped_image = (warped_image > threshold).astype("uint8") * 255


    shortname = os.path.splitext(args["image"])[0]

    warped_image = imutils.resize(warped_image, height = 650)
    cv2.imwrite("./images/scanned_images/scanned_"+shortname+".png", warped_image)

    print("====== Transformation performed ======")
    #show the original imamge
    cv2.imshow("Original", imutils.resize(original_image, height = 650))

    #show the edges image
    cv2.imshow("Edged", edges)

    #show the contour image
    cv2.drawContours(image, [the_contour], -1, (0, 255, 0), 2)
    cv2.imshow("Outline", image)

    #show the final image 
    cv2.imshow("Scanned", imutils.resize(warped_image, height=650))
    cv2.waitKey(0)