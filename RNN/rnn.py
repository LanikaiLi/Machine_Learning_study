# -*- coding: utf-8 -*-
"""RNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ay0IwccHDCRh5Jduojv0GfKrA9n1O2bU

# 第一个stock market prediction model
"""

#Import Dependencies
import os 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Get Data
url = 'https://raw.githubusercontent.com/LanikaiLi/Machine_Learning_study/main/RNN/GOOG.csv'
data = pd.read_csv(url)
data.head(10)

data_training = data[data['Date']<'2021-10-01'].copy()
data_test = data[data['Date']>='2021-10-01'].copy()

data_training

data_training = data_training.drop(['Date', 'Adj Close'], axis = 1)

data_training

scaler = MinMaxScaler()
data_training = scaler.fit_transform(data_training)
data_training[0:5]

X_train = []
y_train = []

data_training.shape[0]

for i in range(60, data_training.shape[0]):
    X_train.append(data_training[i-60:i])
    y_train.append(data_training[i, 0])

X_train, y_train = np.array(X_train), np.array(y_train)
#X_train

print(X_train.shape)
print(y_train.shape)

#build RNN
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout

model = Sequential()

model.add(LSTM(units = 80, activation = 'relu', return_sequences = True, input_shape = (X_train.shape[1], 5)))
model.add(Dropout(0.2))

model.add(LSTM(units = 60, activation = 'relu', return_sequences = True))
model.add(Dropout(0.2))

model.add(LSTM(units = 80, activation = 'relu', return_sequences = True))
model.add(Dropout(0.2))

model.add(LSTM(units = 120, activation = 'relu'))
model.add(Dropout(0.2))

model.add(Dense(units = 1))

model.compile(optimizer='adam', loss = 'mean_squared_error')

model.fit(X_train, y_train, epochs=5, batch_size=32)

data_test.head()

data_training = data[data['Date']<'2021-10-01'].copy()

past_60_days = data_training.tail(60)

df = past_60_days.append(data_test, ignore_index = True)
df = df.drop(['Date', 'Adj Close'], axis = 1)
df.head()

inputs = scaler.transform(df)
inputs

X_test = []
y_test = []

for i in range(60, inputs.shape[0]):
    X_test.append(inputs[i-60:i])
    y_test.append(inputs[i, 0])

X_test, y_test = np.array(X_test), np.array(y_test)
X_test.shape, y_test.shape

y_pred = model.predict(X_test)

scaler.scale_

scale = 1/8.18605127e-04
scale

y_pred = y_pred*scale
y_test = y_test*scale

# Visualising the results
#这个图画出来不好看可能是因为数据太少了，所以没有把model教会，原本那个人的code里有3000 多个数据，我们只有300个
#也可能是因为参数不对，需要调参
plt.figure(figsize=(14,5))
plt.plot(y_test, color = 'red', label = 'Real Google Stock Price')
plt.plot(y_pred, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()

"""**Hyperparameter** **Tunning** **for** **first model**"""

#Jiahua 你觉得都有哪些是需要tune的？
#需要几层layer 
#每层layer有几个perceptron
#batch size
#number of epochs
#?

"""# 第二个stock market prediction model"""

!pip install nsepy

from nsepy import get_history as gh
import datetime as dt
from matplotlib import pyplot as plt
from sklearn import model_selection
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

start = dt.datetime(2013,1,1)
end = dt.datetime(2018,12,31)
stk_data = gh(symbol='SBIN',start=start,end=end)

stk_data

#build model

"""# 第三个stock predict model

*3.1 Data Descriptive Analysis*
"""

import os 
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sklearn.preprocessing import MinMaxScaler

# Get Data
url2 = 'https://raw.githubusercontent.com/LanikaiLi/Machine_Learning_study/main/RNN/Google_Stock_Price_Train.csv'
dataset = pd.read_csv(url2)
dataset.head(10)

#check if there is any missing values
dataset.isna().any()

#get the information about every column in this dataset
#here, note that column close and volume has different datatype as open, high and low columns, which might be an issue
#note, the reason they are object rather than float is because some of their values have "," inside which make them not able to be a float
dataset.info()

#plot the open price of Google stock price within the period that the dataset specifies
dataset['Open'].plot(figsize=(16,6))

#becasue several columns does not have the same datatype as others, we need to make them homogeneous
dataset['Close'] = dataset['Close'].str.replace(',','').astype(float)
dataset['Volume'] = dataset['Volume'].str.replace(',','').astype(float)

#check again about their datatype， now they are all float！
dataset.info()

#get the 7-day rolling mean for each date, note this data will start from the 6th day after 2012-1-3, becasue there is no 7-day rolling mean for the dates before that day
#note: A rolling mean is simply the mean of a certain number of previous periods in a time series. (reference: https://www.statology.org/rolling-mean-pandas/)
dataset.rolling(7).mean().head(20)

#plot the 7-days rolling mean of Open price along with original data
dataset['Open'].plot(figsize=(16,6))
dataset.rolling(window=30).mean()['Close'].plot()

#plot the 30-days rolling mean of Close price along with original data
dataset['Close: 30 Day Mean'] = dataset['Close'].rolling(window=30).mean()
dataset[['Close','Close: 30 Day Mean']].plot(figsize=(16,6))

#set trainning data
training_set = dataset['Open']
training_set = pd.DataFrame(training_set)
training_set

"""*3.2 Data reprocessing*"""

from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0,1))
training_set_scaled = sc.fit_transform(training_set)
training_set_scaled[0]

#creating a data structure with 60 timesteps and 1 output
#i.e. we will use day1-day60 to make prediction about day61,and day2-day61 to make prediction about day62,...
#
X_train = []
y_train = []
#####这里我改了######从1250变成1258####
for i in range(60,1258):
  X_train.append(training_set_scaled[i-60:i,0])
  y_train.append(training_set_scaled[i,0])
X_train, y_train = np.array(X_train), np.array(y_train)

X_train

#Reshaping
#note, X_train.shape[0] = 1258-60 = 1198, X_train.shape[1] = 60
#The shape attribute for numpy arrays returns the dimensions of the array. If Y has n rows and m columns, then Y.shape is (n,m). So Y.shape[0]=n is n
#By this line of code, we want to make X_train a 2D array with 1190 rows and 60 columns
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1],1))

X_train

"""*3.2 Build RNN model*"""

#importing useful libraries
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam


#initializing RNN
regressor = Sequential()

#add layers to it
#note, Dropout rate is just a technique to void overfitting in neural networks
#dropout能让这个模型不要钻牛角尖，如果其中一个神经元突然不工作了，有dropout那么我们的模型就能忽略它继续前行，没有的话它就原地被困住
#所以说dropout can make neurons more robust, it can make them predict trend without focusing on any one neuron
#不信可以plot mse，有dropout的error rate明显更小

#input layer
regressor.add(LSTM(units = 50, return_sequences=True, input_shape = (X_train.shape[1],1)))
regressor.add(Dropout(0.2))

#three layer inside
regressor.add(LSTM(units = 50, return_sequences=True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50, return_sequences = True))
regressor.add(Dropout(0.2))

regressor.add(LSTM(units = 50))
regressor.add(Dropout(0.2))

#add the output layer
regressor.add(Dense(units = 1))

#compiling RNN model
#here, the optimizer affects how fast the algorithm converges to the minimum value.
#becasue the optimizer somehow represents the gradient descent and learning rate the model is using behind the scene
#another parameter we are using is the regularization parameter, its function it to make sure the weights do not get too large and avoid overfitting
regressor.compile(optimizer = 'adam', loss = 'mean_squared_error')

#fitting model to training dataset
regressor.fit(X_train, y_train, epochs = 100, batch_size = 32)

"""*3.3 make prediction and visualize the result*"""

#getting the real stock price of 2017
dataset_test = pd.read_csv("https://raw.githubusercontent.com/LanikaiLi/Machine_Learning_study/main/RNN/Google_Stock_Price_Test.csv")
dataset_test.head()

#real stock price其实就是 Open的那一列
real_stock_price = dataset_test.iloc[:,1:2].values
real_stock_price

dataset_test.info()

dataset_test['Volume'] = dataset_test['Volume'].str.replace(',', '').astype(float)
dataset_test.info()

test_set = dataset_test['Open']
test_set = pd.DataFrame(test_set)
test_set

#get the predicted stock price of 2017
dataset_total = pd.concat((dataset['Open'], dataset_test['Open']), axis = 0)
inputs = dataset_total[len(dataset_total) - len(dataset_test) - 60:].values
inputs = inputs.reshape(-1,1)
inputs = sc.transform(inputs)
X_test = []
for i in range(60,80):
  X_test.append(inputs[i-60:i,0])
X_test = np.array(X_test)
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
predicted_stock_price = regressor.predict(X_test)
predicted_stock_price = sc.inverse_transform(predicted_stock_price)

predicted_stock_price = pd.DataFrame(predicted_stock_price)
predicted_stock_price.info()

#visualizing
plt.plot(real_stock_price, color = 'red', label = 'Real Google Stock Price')
plt.plot(predicted_stock_price, color = 'blue', label = 'Predicted Google Stock Price')
plt.title('Google Stock Price Prediction')
plt.xlabel('Time')
plt.ylabel('Google Stock Price')
plt.legend()
plt.show()

"""# 第四个model：这次是一个天气预报的model"""

