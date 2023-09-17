import os 
import glob
from heic2png import HEIC2PNG


def convert_heic2png(image_path):

    list_images = glob.glob("images/*")

    path = os.path.splitext(image_path)[0]

    if image_path in list_images:

        print('Converting HEIC images to PNG...')
        png_image = HEIC2PNG(image_path)
        png_image.save()
        os.remove(image_path)
        new_pathname = os.path.splitext(image_path)[0] + '.png'
        return new_pathname
    
    elif (path + '.png') in list_images:
        print('No HEIC images found but a png image found in stead.')
        new_pathname = path + '.png'
        return new_pathname
    
    else:
        print('Canot perform the scan. Please provide a PNG or HEIC image.')
