import nltk

# Download required resources
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("corpora/wordnet")
except LookupError:
    nltk.download("wordnet")

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


def preprocess_text(text):

    tokens = word_tokenize(text.lower())

    stop_words = set(stopwords.words("english"))

    words = [
        word for word in tokens
        if word.isalpha() and word not in stop_words
    ]

    lemmatizer = WordNetLemmatizer()

    clean_words = [
        lemmatizer.lemmatize(word)
        for word in words
    ]

    return " ".join(clean_words)