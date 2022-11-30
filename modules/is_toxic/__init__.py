import nltk
import string
import pickle

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from langdetect import detect


class IsToxic:
    def __init__(self, min_toxic_value: float = 0.5) -> None:
        self.min_toxic_value = min_toxic_value

        nltk.download('stopwords')
        nltk.download('punkt')

        self.snowball = SnowballStemmer(language="russian")
        self.russian_stop_words = stopwords.words("russian")

        self.vectorizer = pickle.load(open("vectorizer.pickle", 'rb'))

        self.model = pickle.load(open('model.bf', 'rb'))
        
    def tokinize_sentence(self, sentence: str):
        sentence = sentence.strip().lower()
        try:
            if detect(sentence) == "ru":
                sentence = sentence.replace("e", "е").replace("a", "а").replace("c", "с").replace("p", "р").replace("o", "о").replace("M", "м").replace("H", "н").replace("B", "в")
                sentence = sentence.replace("не ", "не").replace("no ", "no")
        except:
            pass
        sentence = sentence.replace("\t", " ")
        for i in string.punctuation:
            if i in sentence and i != " ":
                sentence = sentence.replace(i, '')
        tokens = word_tokenize(sentence, language="russian")
        tokens = [i for i in tokens if i not in self.russian_stop_words]
        tokens = [self.snowball.stem(i) for i in tokens]
        return " ".join(tokens)

    def toxicity_probab_of(self, text:str) -> float:
        return self.model.predict_proba(self.vectorizer.transform([
            self.tokinize_sentence(text)
        ]))[0, 1]

    def is_toxic(self, text:str) -> bool:
        return self.toxicity_probab_of(text) > self.min_toxic_value