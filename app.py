import pickle
from pathlib import Path

from flask import Flask, render_template, request

from clean_text import clean_text
from train_model import train_and_save_model


MODEL_PATH = Path('model.pkl')


app = Flask(__name__)


def load_artifacts():
    if not MODEL_PATH.exists():
        return train_and_save_model()

    with open(MODEL_PATH, 'rb') as file:
        artifacts = pickle.load(file)

    if isinstance(artifacts, dict) and {'model', 'vectorizer'} <= artifacts.keys():
        return artifacts

    return train_and_save_model()


artifacts = load_artifacts()
model = artifacts['model']
vectorizer = artifacts['vectorizer']


@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    confidence = None
    email_text = ''
    error_message = None

    if request.method == 'POST':
        email_text = request.form.get('email', '').strip()
        cleaned_email = clean_text(email_text)

        if not cleaned_email:
            error_message = 'Please paste a meaningful email message to analyze.'
        else:
            email_tfidf = vectorizer.transform([cleaned_email])
            prediction = str(model.predict(email_tfidf)[0]).strip()

            if hasattr(model, 'predict_proba'):
                confidence = round(float(model.predict_proba(email_tfidf).max()) * 100, 1)

    is_spam = isinstance(prediction, str) and prediction.lower() == 'spam'

    return render_template(
        'index.html',
        prediction=prediction,
        confidence=confidence,
        email_text=email_text,
        error_message=error_message,
        has_result=prediction is not None,
        is_spam=is_spam,
    )


if __name__ == '__main__':
    app.run(debug=True)