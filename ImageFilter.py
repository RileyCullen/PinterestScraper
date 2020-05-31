# Cullen, Riley
# ImageFilter.py
# Created on May 17, 2020

from PIL import Image
from io import BytesIO
import requests

# desc: Goes to url and checks the image size
# pre : The url must be a link to a picture. Not a link to a website with the 
#       picture on it, a link directly to the picture
# 
# Parameters:
# ----------------
# url : string
#       Link to the image we want to check the bounds
#
# hMin : int
#       The lower horizontal bound we want the image's horizontal value to be 
#       greater than
#
# vMin : int
#       The lower vertical bound we want the image's vertical value to be greater
#       than
# Return values:
# ----------------
# True: if image size is greater than the bounds specified by the user
# False: if the image size is less than the bounds specified by the user
def IsImageGreaterThanBounds(url, hMin, vMin):
    if (len(url) != 0):
        imageRequest = requests.get(url)
        try:
            imageRequest.raise_for_status
            image = Image.open(BytesIO(imageRequest.content))
            imageWidth, imageHeight = image.size
            if (imageWidth > hMin and imageHeight > vMin):
                return True
        except requests.exceptions.MissingSchema as exc:
            pass
        except Exception as exc:
            print(exc)
    
    return False