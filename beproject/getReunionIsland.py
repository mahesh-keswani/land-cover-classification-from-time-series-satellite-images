import pandas as pd 
import pickle
import numpy as np 

def getReunionData():
	arr = []
	for line in open('C:/Users/renu/Desktop/django_projects/beproject/beproject/training.txt', 'r'):
		line = list(map(float, line.split(",")))
		arr.append(line)

# (81714, 230) -> (23, 81714, 10)
	arr = np.array(arr).reshape(23, 81714, 10)
	sc = pickle.load(open('C:/Users/renu/Desktop/django_projects/beproject/beproject/my_scaler.pkl','rb'))

	data = []
	for single_arr in arr:
		data.append(sc.transform(single_arr))
	
	return np.array(data)