import streamlit as st
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Load breast cancer dataset
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target

# Define the features used for prediction
feature_names = [
    'mean radius', 'mean texture', 'mean perimeter', 'mean area', 'mean smoothness',
    'mean compactness', 'mean concavity', 'mean concave points', 'mean symmetry', 'mean fractal dimension',
    'radius error', 'texture error', 'perimeter error', 'area error', 'smoothness error',
    'compactness error', 'concavity error', 'concave points error', 'symmetry error', 'fractal dimension error',
    'worst radius', 'worst texture', 'worst perimeter', 'worst area', 'worst smoothness',
    'worst compactness', 'worst concavity', 'worst concave points', 'worst symmetry', 'worst fractal dimension'
]

# Streamlit app
st.title('Breast Cancer Prediction App')

st.sidebar.header('User Input Parameters')

def user_input_features():
    features = {name: st.sidebar.slider(name, float(df[name].min()), float(df[name].max()), float(df[name].mean())) for name in feature_names}
    features_df = pd.DataFrame(features, index=[0])
    return features_df

df_features = user_input_features()

# Prepare the data
X = df[feature_names]
y = df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
X_features = scaler.transform(df_features)

# Train a RandomForest model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Prediction
predictions = model.predict(X_features)
prediction_proba = model.predict_proba(X_features)[0]

st.subheader('User Input Features')
st.write(df_features)

st.subheader('Model Prediction')
st.write('Probability of Malignant: {:.2f}%'.format(prediction_proba[1] * 100))
st.write('Probability of Benign: {:.2f}%'.format(prediction_proba[0] * 100))
st.write('Prediction:', 'Malignant' if predictions[0] == 1 else 'Benign')
