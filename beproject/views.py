from django.http import HttpResponse
from django.shortcuts import render
import ee
import numpy as np 
from . import handleEEstuff 
from . import getReunionIsland
from . import modelStuff
from plotly.offline import plot
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import reverse_geocoder as rg 
import os
import pandas as pd

def homepage(request):
	preloaded = [
		"National_park_2019.tif", "National_park_2020.tif",
		"Aus_fire_2019.tif", "Aus_fire_2020.tif"
	]

	return render(request, 'map1.html', context={'preloaded': preloaded } )

def analysis(request):
	if (request.method=='POST'):
		fromDate = request.POST['fromDate']
		toDate = request.POST['toDate']
		allLatLng = request.POST['test']
		allLatLng = allLatLng[:-5]
		allLatLng = eval(allLatLng)

		N = len(allLatLng)
		latLongPairs = []
		for i in range(0, N, 2):
			if i == N - 1:
				break
			latLongPairs.append([float(allLatLng[i]), float(allLatLng[i + 1])])

		# area =  [ [ -86.88194274902344, 21.030673628606102],
  #                [-86.73431396484375, 21.030673628606102],
  #                [-86.73431396484375, 21.197216077387107],
  #                [-86.88194274902344, 21.197216077387107]
  #         		]
		images, n = handleEEstuff.getData(fromDate, toDate, latLongPairs)

		if n == 1:
			# print(len())
			# plot_div = plot_graphs(image1, image2)
				
			# reverse_latlon = rg.search(latLongPairs)[0]['name']
			# print(reverse_latlon)

			# return render(request, 'reunion.html', context={'plot_div': plot_div})
			return render(HttpResponse('Done!!!'))

		return HttpResponse("Server Error: " + str(images) + "\n" + str(images) )

def plot_graphs(image1, image2):

	pred1 = modelStuff.getPrediction(image1)
	pred2 = modelStuff.getPrediction(image2)

	predictions = [pred1, pred2]
	plot_div = plot_bars(predictions, "reunion.html", "Graphs for the real time data !!!")
	return plot_div

def reunion(request):

	X = getReunionIsland.getReunionData()
	plot_div, a = plotGraph(X, "Reunion Island Land Cover predictions")

	return render(request, 'reunion.html', context={'plot_div': plot_div, 'a':a})

def plotGraph(X, title):
	fig = go.Figure()
	classes = ["urban areas", "other built-up surfaces", "forests", 
		           "sparse vegetation", "rocks and bare soil", "grassland", 
		           "sugarcane crops", "other crops", "water"]

	colors = ['green', 'red', 'blue', 'orange', 'cyan', 'yellow', 'black', 'magenta', 'brown', 'lightgreen'] 
	bars = []
	classes_to_per_day = []
	a = []

	for i, x in enumerate(X):
		scaled_X = modelStuff.scale_data(x)                        
		predictions = modelStuff.getPrediction(scaled_X)
	   
		unique_ys, counts = np.unique(predictions, return_counts=True)
		ys = ( counts / np.sum(counts) ) * 100
		print(unique_ys, counts)

		classes_to_per_day.append( [unique_ys, ys] )

	for unique_ys, percentages in classes_to_per_day:
		xs = []
		for y in unique_ys:
			xs.append(classes[y - 1])

		a.append( [xs, percentages] )
		bar = go.Bar(x=xs, y=percentages)
		bars.append(bar)

	# print("Array T", np.array(a).T)
	# print("My shape", np.array(a).T.shape)
	# print("First element", np.array(a).T[0])

	b = []
	for element in np.array(a).T:
		print(element[1], element[1][0])
		diff = abs(float(element[1][0]) - float(element[1][1]) )
		b.append( [element[0][0], diff] )

	fig_bars = go.Figure(data=bars, layout=go.Layout(barmode='group', title=title))	
	plot_div = plot(fig_bars, output_type='div', include_plotlyjs=True, auto_open=True)

	return plot_div, b

def preloaded(request):
	idx = request.POST.get('item')
	X = getReunionIsland.getPreloadedX(idx)

	lenX = len(X) // 2
	image1 = X[:lenX]
	image2 = X[lenX:]

	plot_div, a = plotGraph([image1, image2], idx)
	return render(request, 'reunion.html', context={'plot_div': plot_div, 'a':a})



















