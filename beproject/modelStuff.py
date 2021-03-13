import pickle

def load_model():
	loaded_model = pickle.load(open('adaboost_for_tiselac.sav', 'rb'))
	return loaded_model

def getPrediction(X):
	model = load_model()
	predictions = model.predict(X).astype('int32')
	return predictions

def scale_data(x):
	sc = pickle.load(open('my_scaler.pkl','rb'))
	scaled_x = sc.transform(x)
	return scaled_x