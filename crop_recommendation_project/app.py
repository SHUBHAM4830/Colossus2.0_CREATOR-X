# app.py

import os
import numpy as np
import pandas as pd
import pickle
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Define file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'Crop_recommendation.csv')
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'crop_model.pkl')
SCALER_PATH = os.path.join(BASE_DIR, 'scalers', 'scaler.pkl')
TRANSLATIONS_PATH = os.path.join(BASE_DIR, 'static', 'js', 'translations.json')

# Create directories if they don't exist
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
os.makedirs(os.path.dirname(SCALER_PATH), exist_ok=True)
os.makedirs(os.path.dirname(TRANSLATIONS_PATH), exist_ok=True)


def load_data():
    """Load the dataset and return the DataFrame."""
    try:
        df = pd.read_csv(DATA_PATH)
        print("Dataset loaded successfully.")
        return df
    except FileNotFoundError:
        print(f"Error: The file {DATA_PATH} was not found.")
        return None
    except Exception as e:
        print(f"Error loading data: {e}")
        return None


def preprocess_data(df):
    """Preprocess the dataset: handle missing values and split features/labels."""
    if df.isnull().sum().sum() > 0:
        print("Missing values found. Filling with mean...")
        df.fillna(df.mean(), inplace=True)
    else:
        print("No missing values found.")

    X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
    y = df['label']
    return X, y


def train_model(X, y):
    """Train the Random Forest model and save it along with the scaler."""
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.ensemble import RandomForestClassifier

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = MinMaxScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    train_score = model.score(X_train_scaled, y_train)
    test_score = model.score(X_test_scaled, y_test)
    print(f"Training Accuracy: {train_score:.4f}")
    print(f"Testing Accuracy: {test_score:.4f}")

    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    with open(SCALER_PATH, 'wb') as f:
        pickle.dump(scaler, f)

    return model, scaler


def predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    """Predict the best crop based on input parameters."""
    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        input_data = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
        input_scaled = scaler.transform(input_data)
        predicted_crop = model.predict(input_scaled)[0]
        return predicted_crop
    except FileNotFoundError:
        print(f"Error: Model or scaler file not found.")
        return None
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None


def get_translated_crop(crop_name, language='en'):
    """Get the translated crop name based on the language preference."""
    try:
        with open(TRANSLATIONS_PATH, 'r', encoding='utf-8') as f:
            translations = json.load(f)

        if language in translations and 'crops' in translations[language] and crop_name in translations[language][
            'crops']:
            return translations[language]['crops'][crop_name]
        else:
            return crop_name
    except Exception as e:
        print(f"Error getting translation: {e}")
        return crop_name


# Train model if not already trained
if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    df = load_data()
    if df is not None:
        X, y = preprocess_data(df)
        train_model(X, y)


@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission and return prediction."""
    try:
        # Get form data and language preference
        lang = request.form.get('language', 'en')
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])
        temperature = float(request.form['temperature'])
        humidity = float(request.form['humidity'])
        ph = float(request.form['ph'])
        rainfall = float(request.form['rainfall'])

        # Make prediction
        prediction = predict_crop(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall)

        if prediction is None:
            error_msg = "Error: Unable to make a prediction."
            return render_template('index.html', prediction=error_msg, language=lang)

        # Translate crop name if possible
        translated_crop = get_translated_crop(prediction, lang)

        return render_template('index.html', prediction=translated_crop, language=lang,
                               inputs={'N': nitrogen, 'P': phosphorus, 'K': potassium,
                                       'temperature': temperature, 'humidity': humidity,
                                       'ph': ph, 'rainfall': rainfall})

    except Exception as e:
        print(f"Error processing form: {e}")
        error_msg = "Error: Invalid input. Please check your values."
        return render_template('index.html', prediction=error_msg)


@app.route('/change-language', methods=['POST'])
def change_language():
    """API endpoint to handle AJAX language change requests."""
    try:
        lang = request.json.get('language', 'en')
        crop = request.json.get('crop', '')

        if crop:
            translated_crop = get_translated_crop(crop, lang)
            return jsonify({'success': True, 'translation': translated_crop})
        else:
            return jsonify({'success': False, 'error': 'No crop provided'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True)