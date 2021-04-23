import spacy
from spacy.util import minibatch, compounding
from spacy.pipeline.textcat import DEFAULT_SINGLE_TEXTCAT_MODEL
from spacy.training import Example
import os
import random

def load_training_data(
    data_directory: str = "aclImdb/train",
    split: float = 0.8,
    limit: int = 0
) -> tuple:
    # Load from files
    reviews = []
    for label in ["pos", "neg"]:
        labeled_directory = f"{data_directory}/{label}"
        for review in os.listdir(labeled_directory):
            if review.endswith(".txt"):
                with open(f"{labeled_directory}/{review}", encoding="utf8") as f:
                    text = f.read()
                    text = text.replace("<br />", "\n\n")
                    if text.strip():
                        spacy_label = {
                            "cats": {
                                "pos": "pos" == label,
                                "neg": "neg" == label}
                        }
                        reviews.append((text, spacy_label))
    random.shuffle(reviews)

    if limit:
        reviews = reviews[:limit]
    split = int(len(reviews) * split)
    return reviews[:split], reviews[split:]


def train_model(training_data, test_data=None):

    nlp = spacy.load("en_core_web_sm")
    config = {
    "threshold": 0.5,
    "model": DEFAULT_SINGLE_TEXTCAT_MODEL,
    }

    tk = nlp.add_pipe("textcat", config=config, last=True)
    optimizer = tk.create_optimizer()

    batch_sizes = compounding(
        4.0, 32.0, 1.001
    )  # A generator that yields infinite series of input numbers

    batches = minibatch(training_data, size=batch_sizes)

    with nlp.select_pipes(enable="textcat") as t:
        for batch in batches:
            examples = [Example.from_dict(nlp.make_doc(b[0]), b[1]) for b in batch]
            break
        optimizer = nlp.initialize(lambda: examples)
        for batch in batches:
            examples = [Example.from_dict(nlp.make_doc(b[0]), b[1]) for b in batch]
            losses = nlp.update(examples, sgd=optimizer)
    return nlp

def save_model(nlp, path):
    return nlp.to_disk(path)

def load_model(path):
    """ the returned object is an nlp which takes a text, nlp("some texst") and has a .cat property where the sentiment is"""
    # for example -> f"{os.getcwd()}/trained_models"
    return spacy.load(path)