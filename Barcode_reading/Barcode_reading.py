import cv2 as cv
import numpy as np
import glob
import matplotlib.pyplot as plt
import skimage.io
import skimage.color
import skimage.filters
import numpy as np
#import argparse
import imutils
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from pyzbar.pyzbar import decode
from pyzbar import pyzbar
import cv2
import glob
from tqdm import tqdm

path = r'C:\Users\sendr\Documents\Proj_Massive_Barcode_Reading\Product_A\data_barcode\train\images\Source\*.jpg'
files = glob.glob(path)


i = 0

for file in tqdm(files):
    
    image = cv2.imread(file)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    t,bimage = cv2.threshold(gray,160,255,cv2.THRESH_BINARY)
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]], np.float32)
    #kernel = 1/3 * kernel
    image_sharp = cv2.filter2D(src=bimage, ddepth=-1, kernel=kernel)
    barcodes = pyzbar.decode(image_sharp)

    list_barcodeData = []
    list_barcodeType = []

    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), thickness=2)

        barcodeData = barcode.data.decode("utf-8")
        list_barcodeData.append(barcodeData)

        barcodeType = barcode.type
        list_barcodeType.append(barcodeType)

        #print (barcodeData+barcodeType)

        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
    i += 1 
        #print("Progress: ", i/len(files))
    source = file

    if (len(barcodes)!= 0):
        destination = source.replace('\\Product_A\\data_barcode\\train\\images\\Source\\','\\Product_A\\data_barcode\\train\\images\\Barcodes\\')
    else:
        destination = source.replace('\\Product_A\\data_barcode\\train\\images\\Source\\','\\Product_A\\data_barcode\\train\\images\\NoBarcodes\\')

    destination = destination.removesuffix('.jpg') + "_result.jpg"

    cv2.imwrite(destination, image)
    cv2.waitKey(0)