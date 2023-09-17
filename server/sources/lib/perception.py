from flair.models import TextClassifier
from flair.data import Sentence

classifier: TextClassifier = TextClassifier.load("en-sentiment")

def calculate_perception(title: str) -> float:
    sentence: Sentence = Sentence(title)
    classifier.predict(sentence)
    label = sentence.labels[0]

    if label.score < 0.8:
        return 0
    elif label.value == "POSITIVE":
        return 1
    else:
        return -1
