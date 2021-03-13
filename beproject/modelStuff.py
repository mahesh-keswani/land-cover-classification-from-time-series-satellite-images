import pickle
import tensorflow as tf

def load_model():
	loaded_model = pickle.load(open('adaboost_for_tiselac.sav', 'rb'))
	return loaded_model

def CNN3d():
	model = tf.keras.models.load_model('model_tiselac_without_latlon_v1.h5')
	return model

def getPrediction(X):
	# model = load_model()
	model = CNN3d()
	data_gen = data_generator(X)
	predictions = model.predict_generator(data_gen)

	print(predictions.shape)
	# predictions = model.predict(X).astype('int32')
	return predictions

def scale_data(x):
	sc = pickle.load(open('my_scaler.pkl','rb'))
	scaled_x = sc.transform(x)
	return scaled_x

def smoothing(row):
    # given a row of shape (23,10), smoothes all 10 feature according to the smoothing factor (mean over a SMOOTH_SIZE window)
    
    to_smooth = np.copy(row)
    
    for i in range(row.shape[1]):
        for j in range(row.shape[0]):
            
            smoothing_indices = np.array([k % row.shape[0] for k in range(int(j - SMOOTH_SIZE / 2), int(j + SMOOTH_SIZE / 2 + 1))])
            
            acc = 0
            for idx in smoothing_indices:
                acc += row[idx,i]
                
            to_smooth[j,i] = acc / SMOOTH_SIZE
            
    return to_smooth
 
def down_sampling(row):
    new_row = []
    
    for j in range(0, len(row)+1, DOWN_SAMPLING_FACTOR):
        new_row.append(row[j])
    
    return np.array(new_row)

def data_generator(X, input_shape=10, batch_size=64):
        
	while True:
        
	    for i in range(0, len(X), batch_size):
	        
	        upper = min(i+batch_size, len(X)-1)

	        
	        batch = np.copy(X[i:upper])
	        smoothed = np.copy(X[i:upper])
	        down = np.zeros( (len(batch), DOWN_SAMPLING_SIZE, input_shape ))
	        
	        # coords = np.copy(X_coord[i:upper])
	        
	        for row_idx in range(len(batch)):
	            smoothed[row_idx, :] = smoothing(X[row_idx, :])
	            down[row_idx, :] = down_sampling(X[row_idx, :])
	        
	        
	        X_batch = [batch,smoothed,down]
	            
	        yield X_batch