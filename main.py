import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from sklearn.exceptions import NotFittedError
from sklearn.utils.validation import check_is_fitted

ps = PorterStemmer()

# Ensure required NLTK resources are available
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load artifacts
try:
    tfidf = pickle.load(open('./artifacts/vectorizer.pkl','rb'))
    model = pickle.load(open('./artifacts/model.pkl','rb'))
except Exception as e:
    st.error(f"Failed to load artifacts: {e}")
    st.stop()

# Validate artifacts are fitted
artifacts_ok = True
try:
    check_is_fitted(tfidf)
except Exception:
    artifacts_ok = False

try:
    check_is_fitted(model)
except NotFittedError:
    artifacts_ok = False
except Exception:
    # Fallback: many classifiers expose `classes_` when fitted
    artifacts_ok = artifacts_ok and hasattr(model, 'classes_')

if not artifacts_ok:
    st.error("Model artifacts are not fitted. Please retrain the model and vectorizer and save fitted files to ./artifacts as 'vectorizer.pkl' and 'model.pkl'.")
    st.stop()

st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):

    if not input_sms.strip():
        st.warning("Please enter a message.")
    else:
        # 1. preprocess
        transformed_sms = transform_text(input_sms)
        try:
            # 2. vectorize
            vector_input = tfidf.transform([transformed_sms])
            # 3. predict
            result = model.predict(vector_input)[0]
        except NotFittedError:
            st.error("Loaded model/vectorizer is not fitted. Retrain and re-save the artifacts.")
            st.stop()
        # 4. Display
        if result == 1:
            st.header("Spam")
        else:
            st.header("Not Spam")