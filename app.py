import streamlit as st
import numpy as np
from tensorflow import keras
from keras.models import load_model
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd

model= pickle.load(open('classifier.pkl','rb'))
scaler= pickle.load(open('scaler.pkl','rb'))
cols_when_model_builds = model.get_booster().feature_names
st.title("Welcome to Delhi House Price Prediction app")

Area = float(st.number_input("Area of the Property in square feet"))
BHK = float(st.number_input("No. of Bedrooms along with 1 Hall and 1 kitchen",max_value=6))
Bathroom = float(st.number_input("No. of Bathrooms",max_value=7))
Parking = float(st.number_input("No. of parking available",max_value=5))
Status = st.radio("Property's Status",("Ready to move",'Under Constuction'))
Transaction = st.radio("Its a new property or being re-sold?",("Resale",'New Property'))
Type = st.radio("Its an Apartment or Builder Floor?",("Appartment",'Builder Floor'))
Per_Sqft = float(st.number_input("Price per square feet",max_value=183333.0))
Furnishing = st.radio("Level Of Furnishing",('Furnished', 'Semi-Furnished', 'Unfurnished'))

btn = st.button("Predict Price")

input_data=[Area,BHK,Bathroom,Parking]

if Status=='Ready to move':
	input_data.append(1)
elif Status=='Under Construction':
	input_data.append(0)
if Transaction=='Resale':
	input_data.append(1)
elif Transaction=='New Property':
	input_data.append(0)
if Type=='Appartment':
	input_data.append(1)
elif Type=='Builder Floor':
	input_data.append(0)
input_data.append(Per_Sqft)
if Furnishing=='Furnished':
	input_data.extend([1,0,0])
elif Furnishing=='Semi-Furnished':
	input_data.extend([0,1,0])
elif Furnishing=='Unfurnished':
	input_data.extend([0,0,1])


inp=pd.DataFrame([input_data],columns=cols_when_model_builds)
inp_scaled=scaler.transform(inp)
if btn:
	pred = model.predict(inp_scaled)
	st.write('The Predicted Price for this Property is : {} '.format(int(pred[0])))
	print(input_data)