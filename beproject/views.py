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
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def homepage(request):
	return render(request, 'index.html')

def map(request):
	return render(request, 'map.html')

def analysis(request):
	if (request.method=='POST'):
		fromDate = request.POST['fromDate']
		toDate = request.POST['toDate']
		allLatLng = request.POST['allLatLng']
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
	plot_div = (predictions, "reunion.html", "Graphs for the real time data !!!")
	return plot_div

def reunion(request):

	X = getReunionIsland.getReunionData()
	plot_div = plotGraph(X, "Reunion Island Land Cover predictions")

	return render(request, 'reunion.html', context={'plot_div': plot_div})

def plotGraph(X, title):
	fig = go.Figure()
	classes = ["urban areas", "other built-up surfaces", "sugarcane crops", 
		           "sparse vegetation", "rocks and bare soil", "grassland", 
		           "forests", "other crops", "water"]

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

	# b = []
	# for element in np.array(a).T:
	# 	print(element[1], element[1][0])
	# 	diff = abs(float(element[1][0]) - float(element[1][1]) )
	# 	b.append( [element[0][0], diff] )

	fig_bars = go.Figure(data=bars, layout=go.Layout(barmode='group', title=title))	
	plot_div = plot(fig_bars, output_type='div', include_plotlyjs=True, auto_open=True)

	return plot_div

def preloaded(request):
	idx = request.POST.get('item')
	X = getReunionIsland.getPreloadedX(idx)

	lenX = len(X) // 2
	image1 = X[:lenX]
	image2 = X[lenX:]

	plot_div = plotGraph([image1, image2], idx)
	return render(request, 'reunion.html', context={'plot_div': plot_div})

def upload(request):
    if request.method == 'POST' and request.FILES['myfile1'] and request.FILES['myfile2']:
        myfile1 = request.FILES['myfile1']
        myfile2 = request.FILES['myfile2']
        fs = FileSystemStorage()
        filename1 = fs.save(myfile1.name, myfile1)
        filename2 = fs.save(myfile2.name, myfile2)
        uploaded_file_url_1 = fs.url(filename1)
        uploaded_file_url_2 = fs.url(filename2)
        print(uploaded_file_url_1,filename1)
        X = getReunionIsland.getPreloadedX(settings.MEDIA_ROOT+'/'+filename1)
        Y = getReunionIsland.getPreloadedX(settings.MEDIA_ROOT+'/'+filename2)

        plot_div = plotGraph([X, Y], filename1+filename2)
        return render(request, 'reunion.html', context={'plot_div': plot_div})
		
        
    return render(request, 'upload.html')

