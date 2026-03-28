from pathlib import Path
import pickle

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

from clean_text import clean_text


DATA_PATH = Path('email.csv')
MODEL_PATH = Path('model.pkl')


def train_and_save_model(data_path=DATA_PATH, model_path=MODEL_PATH):
    data = pd.read_csv(data_path)
    data['Message'] = data['Message'].fillna('').apply(clean_text)

    features = data['Message']
    labels = data['Category']

    x_train, _, y_train, _ = train_test_split(
        features,
        labels,
        test_size=0.2,
        random_state=42,
    )

    vectorizer = TfidfVectorizer(stop_words='english')
    x_train_tfidf = vectorizer.fit_transform(x_train)

    model = MultinomialNB()
    model.fit(x_train_tfidf, y_train)

    artifacts = {
        'model': model,
        'vectorizer': vectorizer,
    }

    with open(model_path, 'wb') as file:
        pickle.dump(artifacts, file)

    return artifacts


if __name__ == '__main__':
    train_and_save_model()