# Test script
import pickle

with open('/Users/mar/.cache/kagglehub/models/qadeer884/emplyee-chrun-prediction/scikitLearn/default/1/Hiring_classifier/Rf_classifier.pkl', 'rb') as f:
    model = pickle.load(f)

# Create a sample input matching your features
sample_input = [[0.7, 4, 3, 160, 3, 0, 0, 1]]  # Example values
prediction = model.predict(sample_input)
print(f"Prediction: {prediction}")