# importing the dependencies
import streamlit as st
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA

#   loading the trained model
model = pickle.load(open('model.pkl', 'rb'))
st.title('Petrol Price Forecasting')

#   reading the data
df = pd.read_csv('train_data.csv')
#   deleting all the null entries
df.dropna(inplace=True)

#   changing the datatype of Date column to datetime
df['Date'] = pd.to_datetime(df['Date'])

#   setting date as an index column
df.set_index('Date', inplace=True)

#   Resampling the entries. Entries are in given per week. We are converting them to monthly format by summing up the entries.
df = df['Petrol (USD)'].resample('MS').sum()

st.text('Past Data of Petrol Price')
st.write(df)

st.line_chart(df)

#   Extracting the trend, season, and residual error from the series
decomposition = sm.tsa.seasonal_decompose(df, model='multiplicative')
fig = decomposition.plot()
st.write('Trend, Seasonality component, and Error')
st.pyplot(fig)

#   Range for the future months
list = [i for i in range(1, 16)]
st.write('Future data for next 15 months')
option = st.selectbox(
    'decide how many future months you want to predict into?',
    list
)
#   Predicting into the future
predictions = model.predict(len(df), len(df)+option-1)
st.write(predictions)

fig1 = plt.figure(figsize=(10,5))
fig1.add_subplot(df.plot(legend=True, label='Train'))
fig1.add_subplot(predictions.plot(legend=True, label='Prediction'))
st.pyplot(fig1)

# storing the result in csv file
result = pd.DataFrame(predictions)
result.columns = ['Prediction']
result = result.rename_axis('Date')
result.to_csv('ARIMA_result.csv')