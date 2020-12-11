import ee
import numpy as np 
import pandas as pd 
from cv2 import convertScaleAbs

def initializeEE():
	# ee.Authenticate()
	ee.Initialize()

def load_collection():
	initializeEE()
	COLLECTION = "LANDSAT/LC08/C01/T1_SR"
	landsat = ee.ImageCollection(COLLECTION)

	return landsat

def getMidDate(fromDate, toDate):

	from datetime import datetime
	d1 = datetime.strptime(fromDate,"%Y-%m-%d")
	d2 = datetime.strptime(toDate,"%Y-%m-%d")

	mid = str(d1.date() + (d2-d1) / 2) 
	print(mid)

	return mid

def removeClouds(image):
    cloudShadowBitMask = ee.Number(2).pow(3).int()
    cloudsBitMask = ee.Number(2).pow(5).int()
    qa = image.select('pixel_qa')
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    return image.updateMask(mask)

def getNumpyImages(fromDate, toDate, geomtery, collection):
	N_SUR_REFLECTANCE = 7
	area = ee.Geometry.Polygon(geomtery)
	collection_filter = collection.filterBounds(area).filterDate(fromDate, toDate)

	# n_images = collection_filter.size().getInfo()
	# if n_images == 0:
	# 	return 0

	print("Collection filtered!!!")
	c1_removed = collection_filter.map(removeClouds)
	img = ee.Image(c1_removed.median()).clip(area)
	
	bands = ee.List(["B1", "B2","B3","B4","B5","B6","B7"])
	img1_full = img.select(bands)

	latlon = ee.Image.pixelLonLat().addBands(img1_full)
	latlon_new1 = latlon.reduceRegion(
	  reducer=ee.Reducer.toList(),
	  geometry=area,
	  maxPixels=1e13,
	  scale=30)


	ultra_blue = np.array((ee.Array(latlon_new1.get("B1")).getInfo())).reshape(-1, 1)
	B = np.array((ee.Array(latlon_new1.get("B2")).getInfo())).reshape(-1, 1)
	G = np.array((ee.Array(latlon_new1.get("B3")).getInfo())).reshape(-1, 1)
	R = np.array((ee.Array(latlon_new1.get("B4")).getInfo())).reshape(-1, 1)
	N = np.array((ee.Array(latlon_new1.get("B5")).getInfo())).reshape(-1, 1)
	S1 = np.array((ee.Array(latlon_new1.get("B6")).getInfo())).reshape(-1, 1)
	S2 = np.array((ee.Array(latlon_new1.get("B7")).getInfo())).reshape(-1, 1)

	lats = np.array((ee.Array(latlon_new1.get("latitude")).getInfo()))
	lons = np.array((ee.Array(latlon_new1.get("longitude")).getInfo()))

	print("Bands loaded!!!")
	img_full = np.concatenate((ultra_blue, B, G, R, N, S1, S2), axis = 1)

	# (NIR - R) / (NIR + R)
	ndvi = (img_full[:, 4] - img_full[:, 3]) / ( img_full[:, 4] + img_full[:, 3] )

	# (G - NIR) / (G + NIR)
	ndwi = (img_full[:, 2] - img_full[:, 4]) / ( img_full[:, 2] + img_full[:, 4] )

	# Brightness Index = sqrt(((Red * Red)/ (Green* Green))/2)
	bi = np.sqrt( ( (img_full[:, 3]*img_full[:, 3]) / (img_full[:, 2]*img_full[:, 2]) ) / 2 )
	print("Calcuated indexes done!!!")

	Arr_norm = np.concatenate(( img_full, ndvi.reshape(-1, 1), ndwi.reshape(-1, 1), bi.reshape(-1, 1) ), axis = 1)
	
	df = pd.DataFrame(Arr_norm)
	df.replace([np.inf, -np.inf], np.nan, inplace = True)
	df.fillna(df.median(), inplace = True)

	return df.values, 1	

def getData(fromDate, toDate, geomtery):
	landsat = load_collection()
	print("Collection loaded!!!")

	mid_date = getMidDate(fromDate, toDate)

	image1, n1 = getNumpyImages(fromDate, mid_date, geomtery, landsat)
	image2, n2 = getNumpyImages(mid_date, toDate, geomtery, landsat)

	return (image1, n1), (image2, n2)














