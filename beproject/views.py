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
	return render(request, 'map1.html')

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

	if os.path.isfile('reunion_pred.csv'):
		predictions = pd.read_csv('reunion_pred.csv').values
	else:
		predictions = []
		for x in X:
			predictions.append(modelStuff.getPrediction(x))

		predictions = np.array(predictions).T
		pd.DataFrame(data = predictions, columns = range(1, 24)).to_csv('reunion_pred.csv', index = False)

	
	xs = list(range(1, 24))
	classes_to_per = []
	for day in range(23):
		_, ys = np.unique(predictions[:, day], return_counts=True)
		ys = ( ys / np.sum(ys) ) * 100
		classes_to_per.append(ys.tolist())

	# TODO: plot every row of classes_to_per on line chart
	classes_to_per = np.array(classes_to_per).T.tolist()
	# print(classes_to_per)
	lines = []
	classes = ["urban areas", "other built-up surfaces", "forests", 
		           "sparse vegetation", "rocks and bare soil", "grassland", 
		           "sugarcane crops", "other crops", "water"]

	colors = ['green', 'red', 'blue', 'orange', 'cyan', 'yellow', 'black', 'magenta', 'brown', 'lightgreen'] 
	fig = go.Figure()
	for i in range(len(classes_to_per)):
		scatter = go.Scatter(x=xs, y=classes_to_per[i],
                     mode='lines', name=classes[i],
                     opacity=0.8, marker_color=colors[i])
		fig.add_trace(scatter)

	plt_line_div = plot(fig, output_type='div')

	plot_div = plot_bars(predictions.T.tolist(), "reunion.html", title = 'Reunion Island Data from Landsat-8 of the year 2014')

	return render(request, 'reunion.html', context={'plot_div': plot_div, 'plt_line_div': plt_line_div})


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



















