from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
	return render(request, 'map.html')

def analysis(request):
	if (request.method=='POST'):
		fromDate = request.POST['fromDate']
		toDate = request.POST['toDate']
		allLatLng = request.POST['allLatLng']

		print("From date",fromDate)
		print("toDate",toDate)
		print("allLatLng",allLatLng)
		return HttpResponse("analysis")
