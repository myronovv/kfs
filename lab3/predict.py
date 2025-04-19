import joblib

def predict_safety(input_df):
    model = joblib.load("air_model.pkl")
    return model.predict(input_df)
