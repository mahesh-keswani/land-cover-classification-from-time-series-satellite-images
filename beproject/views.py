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

		area =  [ [ -86.88194274902344, 21.030673628606102],
                 [-86.73431396484375, 21.030673628606102],
                 [-86.73431396484375, 21.197216077387107],
                 [-86.88194274902344, 21.197216077387107]
          		]
		(image1, n1), (image2, n2) = handleEEstuff.getData(fromDate, toDate, area)

		if n1 == 1 and n2 == 1:
			print("Shape of images", image1.shape, image2.shape)
			plot_div = plot_graphs(image1, image2)
			
			return render(request, 'reunion.html', context={'plot_div': plot_div})

		return HttpResponse("Server Error: " + str(image1) + "\n" + str(image2) )

def plot_graphs(image1, image2):
	scaled_image1 = modelStuff.scale_data(image1)
	scaled_image2 = modelStuff.scale_data(image2)

	pred1 = modelStuff.getPrediction(scaled_image1)
	pred2 = modelStuff.getPrediction(scaled_image2)

	predictions = [pred1, pred2]
	plot_div = plot_bars(predictions, "reunion.html", "Graphs for the real time data !!!")
	return plot_div


def reunion(request):
	X = getReunionIsland.getReunionData()

	predictions = []
	for x in X:
		predictions.append(modelStuff.getPrediction(x))

	plot_div = plot_bars(predictions, "reunion.html", title = 'Reunion Island Data from Landsat-8 of the year 2014')

	return render(request, 'reunion.html', context={'plot_div': plot_div})


def plot_bars(predictions, template, title):
	bars = []
	for i, pred in enumerate(predictions):
		_, ys = np.unique(pred, return_counts=True)

		ys = ( ys / np.sum(ys) ) * 100
		xs = ["urban areas", "other built-up surfaces", "forests", 
		           "sparse vegetation", "rocks and bare soil", "grassland", 
		           "sugarcane crops", "other crops", "water"]

		bar = go.Bar(x=xs, y=ys, name="Day {}".format(i + 1))
		bars.append(bar)

		# pie = {'labels':xs, 'values':ys, "domain": {"x": [0, .5], 'y': [0, 1.0]}, "name": "Day {}".format(i + 1), "hoverinfo":"label+percent+name", "hole": .4, "type": "pie"}
		# pies.append(pie)

	fig = go.Figure(data=bars, layout=go.Layout(barmode='group', title=title))
	# fig_pies = go.Figure(data=pies, layout=go.Layout(piemode='group', title='Reunion Island Data from Landsat-8 of the year 2014'))
	
	plot_div = plot(fig, output_type='div', include_plotlyjs=True, auto_open=True)
	# plot_div_pies = plot(fig_pies, output_type='div', include_plotlyjs=True, auto_open=True)
	return plot_div



















