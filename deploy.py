
import joblib
import pandas as pd
import numpy as np
import streamlit as st
import requests


# forward geocding from state and countyr input
# get API key
try:
    API_KEY = st.secrets['API_KEY']
except Exception:
    API_KEY = os.getenv('API_KEY')

def forwardgeocode(address, api_key ):
  url= f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
  response = requests.get(url)

  if response.status_code ==200:
      result = response.json()
      if 'results' in result and len(result['results']) > 0:
          location = result['results'][0]['geometry']['location']
          return location['lat'], location['lng']
      else:
           return None, None
  else:
       return None, None

# country list
countries = [
    'Nigeria', 'United States', 'United Kingdom', 'Ghana',
    'United Arab Emirates', "Côte d'Ivoire", 'Thailand', 'Russia',
    'Benin', 'Niger', 'China', 'Australia'
]

# States by country
states_by_country = {
    "Nigeria": [
        'Lagos', 'Ogun State', 'Delta', 'Federal Capital Territory',
        'Rivers', 'Imo', 'Gombe', 'Akwa Ibom', 'Oyo', 'Nasarawa', 'Ondo',
        'Edo', 'Abia', 'Cross River', 'Niger', 'Taraba', 'Kaduna',
        'Ìpínlẹ̀ Ògùn', 'Ìpínlẹ̀ Èkó', 'Kwara', 'Osun', 'Anambra',
        'Ekiti', 'Benue', 'Kano', 'Enugu', 'Bayelsa', 'Jigawa', 'Agege',
        'Kogi', 'Plateau', 'Ebonyi', 'Adamawa', 'Katsina', 'Igbaga',
        'Borno', 'Ìpínlẹ̀ Ọ̀yọ́', 'Bauchi', 'Auaba', 'Igbile', 'Kebbi',
        'Bakatari', 'Ìpínlẹ̀ Kwárà', 'Sokoto', 'Zamfara'
    ],
    "United States": [
        'California', 'Georgia', 'Texas', 'New York', 'Kansas', 'Ohio',
        'Maryland', 'Arkansas'
    ],
    "United Kingdom": [
        'Northern Ireland', 'England', 'Scotland', 'Wales'
    ],
    "Ghana": [
        'Greater Accra Region'
    ],
    "United Arab Emirates": [
        'Sharjah', 'Dubai', 'دبي'
    ],
    "Côte d'Ivoire": [
        "District Autonome d'Abidjan"
    ],
    "Thailand": [
        'Krung Thep Maha Nakhon'
    ],
    "Russia": [
        'Krasnoyarsk Krai'
    ],
    "Benin": [
        'Ouémé Department', 'Littoral Department'
    ],
    "Niger": [
        'Tahoua'
    ],
    "China": [
        'Bei Jing Shi'
    ],
    "Australia": [
        'New South Wales'
    ]
}

banks = ['GT Bank', 'Sterling Bank', 'Fidelity Bank', 'Access Bank',
       'EcoBank', 'FCMB', 'Skye Bank', 'UBA', 'Diamond Bank',
       'Zenith Bank', 'First Bank', 'Union Bank', 'Stanbic IBTC',
       'Standard Chartered', 'Heritage Bank', 'Keystone Bank',
       'Unity Bank', 'Wema Bank']



# Streamlit APP
model = joblib.load('loan_model.pkl')
st.title ('Customer Loan Default Risk Predictor')

st. write('Provide Customer Details: ')
country = st.selectbox('Bank Branch COuntry', countries)
state = st.selectbox('Bank Branch State', states_by_country[country])
bank_name = st.selectbox('Customers Client Bank', banks)
account_type = st.selectbox('Account Type', ["Savings", "Current", 'Other'])
employment_status = st.selectbox('Employment Status', ['Permanent', 'Student', 'Self-Employed', 'Unemployed', 'Retired',
       'Contract' ])
education_level = st.selectbox('Level of Education', ['Graduate', 'Secondary', 'Post-Graduate', 'Primary'])

credit_score = st.number_input("Credit Score", min_value=300, max_value=850, step=1)
age = st.number_input("Age", min_value=18, max_value=100, step=1)
loan_freq = st.number_input('Loan Frequency', min_value = 1, step= 1)



# predictions
if st.button('Predict'):
    fulladdress = f'{state}, {country}'
    lat, lon = forwardgeocode(fulladdress, API_KEY)
    
    if lat is None or lon is None:
        st.error("Couldn't fetch coordinates for given state/country. Please crosscheck entry")
    else:
        features_data ={
            "bank_account_type": account_type,
            "longitude_gps": lon,
            "latitude_gps": lat,
            "bank_branch_state": state,
            "bank_branch_country": country,
            "employment_status_clients": employment_status,
            "level_of_education_clients": education_level,
            "bank_name_clients": bank_name,
            "credit score": credit_score,
            "age": age,
           "loan_freq": loan_freq
        }
    x= pd.DataFrame([features_data])
    prediction = model.predict(x)
    if prediction[0] == 0:
      st.error("Prediction: Likely to Default (Bad Credit Risk)")
    else:
      st.success("Prediction: Likely to Not Default (Good Credit Risk)")

