import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_local_model(df):
    # Train TF-IDF vectorizer and Logistic Regression classifier on master dataset 
    if df.empty:
        raise ValueError("DataFrame passed to training is empty!")

    vectorizer = TfidfVectorizer()
    model = LogisticRegression()

    train_X = vectorizer.fit_transform(df['comment'])
    train_Y = df['category']

    model.fit(train_X, train_Y)

    return model, vectorizer

def prediction_confidence(text, model, vectorizer):
    # Predict category for a single text and return highest confidence score 
    test_X = vectorizer.transform([text])
    probabilities = model.predict_proba(test_X)[0]
    classes = model.classes_

    max_index = probabilities.argmax()
    best_category = classes[max_index]
    confidence = probabilities[max_index]

    return best_category, confidence