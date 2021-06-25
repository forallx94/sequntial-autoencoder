import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv), data manipulation as in SQL
import matplotlib.pyplot as plt # this is used for the plot the graph
import seaborn as sns # used for plot interactive graph.
from sklearn.metrics import mean_squared_error

from utils import power_data, rmse
from model import setup_lstm_ae_model

import tensorflow.keras.backend as K

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, InputLayer, Activation, Dropout

## Data can be downloaded from: http://archive.ics.uci.edu/ml/machine-learning-databases/00235/
## Just open the zip file and grab the file 'household_power_consumption.txt' put it in the directory
## that you would like to run the code.

# define path to save model
model_path = '../Trained models/Power_regression_LSTM.h5'

# import data
train_X, train_y, test_X, test_y , scaler = power_data()

model = setup_lstm_ae_model(train_X)
print(model.summary())

# fit network
history = model.fit(train_X, train_X,  epochs=200, batch_size=14, validation_data=(test_X, test_X), verbose=2,
                    callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_mse', patience=2, verbose=0, mode='auto'), 
                                tf.keras.callbacks.ModelCheckpoint(model_path,monitor='val_mse', save_best_only=True, mode='min', verbose=0)])


# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper right')
plt.show()

# # make a prediction
# yhat = model.predict(test_X)
# test_X = test_X.reshape((test_X.shape[0], 7))
# # invert scaling for forecast
# inv_yhat = np.concatenate((yhat, test_X[:, -6:]), axis=1)
# inv_yhat = scaler.inverse_transform(inv_yhat)
# inv_yhat = inv_yhat[:,0]
# # invert scaling for actual
# test_y = test_y.reshape((len(test_y), 1))
# inv_y = np.concatenate((test_y, test_X[:, -6:]), axis=1)
# inv_y = scaler.inverse_transform(inv_y)
# inv_y = inv_y[:,0]
# # calculate RMSE
# rmse = np.sqrt(mean_squared_error(inv_y, inv_yhat))
# print('Test RMSE: %.3f' % rmse)


# ## time steps, every step is one hour (you can easily convert the time step to the actual time index)
# ## for a demonstration purpose, I only compare the predictions in 200 hours.

# fig_verify = plt.figure(figsize=(100, 50))
# aa=[x for x in range(200)]
# plt.plot(aa, inv_y[:200], marker='.', label="actual")
# plt.plot(aa, inv_yhat[:200], 'r', label="prediction")
# plt.ylabel('Global_active_power', size=15)
# plt.xlabel('Time step', size=15)
# plt.legend(fontsize=15)
# plt.show()