import ee
import numpy as np 
import pandas as pd 
from cv2 import convertScaleAbs
from . import save_img_to_drive


# def getNumpyImages(fromDate, toDate, geomtery, collection):
# 	n_images = np.random.randint(low = 4, high = 8)

# 	data = np.random.randn( np.random.randint(low = 10000, high = 30000), 10 )
# 	return data, 1
	

def getData(fromDate, toDate, geomtery):
	save_img_to_drive.getData(fromDate, toDate, geomtery)

	image1, image2 = 1, 1
	n1, n2 = 0, 0
	return (image1, n1), (image2, n2)














