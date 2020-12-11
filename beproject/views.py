from django.http import HttpResponse
from django.shortcuts import render
import ee
import numpy as np 
from . import handleEEstuff 

def homepage(request):
	return render(request, 'map.html')

def analysis(request):
	if (request.method=='POST'):
		fromDate = request.POST['fromDate']
		toDate = request.POST['toDate']
		allLatLng = request.POST['allLatLng']

		allLatLng = allLatLng.split(",")

		N = len(allLatLng)
		latLongPairs = []
		for i in range(0, N, 2):
			if i == N - 1:
				break
			latLongPairs.append([float(allLatLng[i]), float(allLatLng[i + 1])])

		(image1, n1), (image2, n2) = handleEEstuff.getData(fromDate, toDate, latLongPairs)

		print(image1.shape, image2.shape)

		return HttpResponse("analysis")













