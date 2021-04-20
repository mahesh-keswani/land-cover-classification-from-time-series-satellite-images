import pandas as pd 
import pickle
import numpy as np 

from osgeo import gdal

def getReunionData():
	df = pd.read_csv('training.txt', header =None)

	arr = df.values.reshape(23 , 81714, 10)
	
	return arr

def getPreloadedX(name):
	raster = gdal.Open(name)
	imarray = np.array(raster.ReadAsArray())
	imarray = imarray.reshape((imarray.shape[0], -1)).T

	# (NIR - R) / (NIR + R)
	ndvi = (imarray[:, 4] - imarray[:, 3]) / ( imarray[:, 4] + imarray[:, 3] )


	# (G - NIR) / (G + NIR)			
	ndwi = (imarray[:, 2] - imarray[:, 4]) / ( imarray[:, 2] + imarray[:, 4] )			

	# Brightness Index = sqrt(((Red * Red)/ (Green* Green))/2)
	bi = np.sqrt( ( (imarray[:, 3]*imarray[:, 3]) / (imarray[:, 2]*imarray[:, 2]) ) / 2 )

	Arr_norm = np.concatenate(( imarray, ndvi.reshape(-1, 1), ndwi.reshape(-1, 1), bi.reshape(-1, 1) ), axis = 1)

	df = pd.DataFrame(Arr_norm)
	df.replace([np.inf, -np.inf], np.nan, inplace = True)
	df.fillna(df.median(), inplace = True)	
			
	return df.values
