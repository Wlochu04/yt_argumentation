import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def train_local_model(df):
    #importing source
    df = pd.read_excel("YT_comm.xlsx")

    vectorizer = TfidfVectorizer()
    model = LogisticRegression()

    train_X = vectorizer.fit_transform(df['comment'])
    train_Y = df['category']

    model.fit(train_X, train_Y)

    return model, vectorizer

def prediction_confidence(text, model, vectorizer):
    test_X = vectorizer.transform([text])

    probabilites = model.predict_proba(test_X)[0]

    classes = model.classes_

    max_index = probabilites.argmax()

    best_category = classes[max_index]
    confidence = probabilites[max_index]

    return best_category, confidence