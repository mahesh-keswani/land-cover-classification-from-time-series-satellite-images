from django.http import HttpResponse
from django.shortcuts import render
import ee
import numpy as np 
from . import handleEEstuff 
from . import getReunionIsland
from . import modelStuff
from plotly.offline import plot
import plotly.graph_objs as go
from collections import Counter 

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


def reunion(request):
	X = getReunionIsland.getReunionData()

	predictions = []
	for x in X:
		predictions.append(modelStuff.getPrediction(x))

	bars = []
	for i, pred in enumerate(predictions):
		_, ys = np.unique(pred, return_counts=True)

		ys = ( ys / np.sum(ys) ) * 100
		xs = ["urban areas", "other built-up surfaces", "forests", 
		           "sparse vegetation", "rocks and bare soil", "grassland", 
		           "sugarcane crops", "other crops", "water"]

		bar = go.Bar(x=xs, y=ys, name="Day {}".format(i + 1))
		bars.append(bar)

	fig = go.Figure(data=bars, layout=go.Layout(barmode='group', title='Reunion Island Data from Landsat-8 of the year 2014'))
	plot_div = plot(fig, output_type='div', include_plotlyjs=True, auto_open=True)
	return render(request, "reunion.html", context={'plot_div': plot_div})





















