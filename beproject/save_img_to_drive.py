# -*- coding: utf-8 -*-
"""Copy of SavingImageToDrive.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1evIWwKjHdGmb6LsNrpk5pLdfMAbqHweU
"""

import ee
import numpy as np
import matplotlib.pyplot as plt


# my_area = [[-4.368439,54.41893],[-4.368439,54.41893],[-4.696655,54.221088],[-4.696655,54.221088],[-4.515381,54.135087],[-4.515381,54.135087],[-4.328613,54.292485],[-4.328613,54.292485],[-4.368439,54.41893]]

def removeClouds(image):
    cloudShadowBitMask = ee.Number(2).pow(3).int()
    cloudsBitMask = ee.Number(2).pow(5).int()
    qa = image.select('pixel_qa')
    mask = qa.bitwiseAnd(cloudShadowBitMask).eq(0).And(qa.bitwiseAnd(cloudsBitMask).eq(0))
    return image.updateMask(mask)

def getMidDate(fromDate, toDate):

	from datetime import datetime
	d1 = datetime.strptime(fromDate,"%Y-%m-%d")
	d2 = datetime.strptime(toDate,"%Y-%m-%d")

	mid = str(d1.date() + (d2-d1) / 2) 
	print(mid)

	return mid

def filter_and_save(landsat, area, start, end, name):
    img_collection = landsat.filterBounds(area).filterDate(start, end)
    c1_removed = img_collection.map(removeClouds)
    img = ee.Image(c1_removed.median()).clip(area)

    bands = ee.List(["B1", "B2","B3","B4","B5","B6","B7"])
    img1_full = img.select(bands)

    task_config = {
        'scale': 30,  
        'region': area,
        'driveFolder':'Stuff'
        }

    task = ee.batch.Export.image(img1_full, name, task_config)

    task.start()
    print("Task executed!!!")


def getData(start, end, my_area):
    # ee.Authenticate()
    ee.Initialize()

    COLLECTION = "LANDSAT/LC08/C01/T1_SR"
    mid = getMidDate(start, end)

    print("Coords", my_area)

    area = ee.Geometry.Polygon(my_area)
    landsat = ee.ImageCollection(COLLECTION)

    print("collection loaded !!!")

    filter_and_save(landsat, area, start, mid, 'first_half_rahul')
    filter_and_save(landsat, area, mid, end, 'second_half_rahul')

    print("Both imgs saved to drive !!!")


# def getNumpyImages(fromDate, toDate, geomtery, collection):