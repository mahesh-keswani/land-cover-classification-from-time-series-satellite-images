import pickle

def load_model():
	loaded_model = pickle.load(open('C:/Users/renu/Desktop/django_projects/beproject/beproject/adaboost_for_tiselac.sav', 'rb'))
	return loaded_model

def getPrediction(X):
	model = load_model()
	predictions = model.predict(X).astype('int32')
	return predictions