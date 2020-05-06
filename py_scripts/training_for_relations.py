#!/usr/bin/env python
# coding: utf-8
# training_for_relations.py
# version 0.5
# adapted from https://github.com/explosion/spaCy/tree/master/examples/training/train_intent_parser.py
"""Using the parser to recognise your own semantics

spaCy's parser component can be used to trained to predict any type of tree
structure over your input text. You can also predict trees over whole documents
or chat logs, with connections between the sentence-roots used to annotate
discourse structure. In the original example, they build a message parser for a common
"chat intent": finding local businesses. Our message semantics will have the
following types of relations: ROOT, PLACE, QUALITY, ATTRIBUTE, TIME, LOCATION.

"show me the best hotel in berlin"
('show', 'ROOT', 'show')
('best', 'QUALITY', 'hotel') --> hotel with QUALITY best
('hotel', 'PLACE', 'show') --> show PLACE hotel
('berlin', 'LOCATION', 'hotel') --> hotel with LOCATION berlin

Compatible with: spaCy v2.0.0+

In the adaptation, we learn a parser for the relations "son of" and "nationality" and
 "from city". 

"""
from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding


# training data: texts, heads and dependency labels
# for no relation, we simply chose an arbitrary dependency label, e.g. '-'
# as explained in https://github.com/explosion/spaCy/issues/2322
# after first doing
# import spacy
nlp = spacy.load("en_diogenet_model")
# doc = nlp("Many think that Pythagoras was the son of Mnesarchus")
# print([t.head.i for t in doc])
# print([t.dep_ for t in doc])
# for each
TRAIN_DATA = [
    (
        "Many think that Pythagoras was the son of Mnesarchus",
        {
            "heads": [1, 1, 4, 4, 1, 6, 4, 6, 7],  # index of token head
            "deps": ["-", "ROOT", "-", "PERSON", "-", "-", "RELATION" , "-","PERSON"],
        },
    ),
    (
        "some think Pythagoras a Samian",
        {
            "heads": [1, 1, 4, 4, 1],
            "deps": ["-", "ROOT",  "PERSON", "-", "NATIONALITY"],
        },
    ),
    (
        "while Neanthes states Pythagoras was a Syrian",
        {
            "heads": [2, 2, 2, 4, 2, 6, 4],
            "deps": [
                "-",
                "-",
                "ROOT",
                "PERSON",
                "-",
                "-",
                "NATIONALITY",
            ],
        },
    ),
    (
        "while Neanthes states Pythagoras was from the city of Tyre",
        {
            "heads": [2, 2, 2, 4, 2, 4, 7, 5, 7, 8],
            "deps": [ "-", "-", "ROOT",  "PERSON", "-", "ORIGIN", "-", "-", "-", "CITY"],
        },
    ),
    (
        "the Chaldeans, whose doctrines Pythagoras imbibed",
        {
            "heads": [1, 1, 1, 4, 6, 6, 1],
            "deps": ['-', 'TEACHER', '-', '-', '-', 'STUDENT', 'ROOT'],
        },
    ),
    (
        "where Pythagoras first studied under the Syrian Pherecydes",
        {
            "heads": [3, 3, 3, 3, 3, 7, 7, 4],
            "deps": ['-', 'STUDENT', '-', 'ROOT', '-', '-', '-', 'TEACHER'],
        },
    ),
    (
        "Pythagoras also studied under Hermodamas",
        {
            "heads": [2, 2, 2, 2, 3],
            "deps": ['STUDENT', '-', 'ROOT', '-', 'TEACHER'],
        },
    ),
]


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir=None, n_iter=15):
    """Load the model, set up the pipeline and train the parser."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # We'll use the built-in dependency parser class, but we want to create a
    # fresh instance – just in case.
    if "parser" in nlp.pipe_names:
        nlp.remove_pipe("parser")
    parser = nlp.create_pipe("parser")
    nlp.add_pipe(parser, first=True)

    for text, annotations in TRAIN_DATA:
        for dep in annotations.get("deps", []):
            parser.add_label(dep)

    pipe_exceptions = ["parser", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    with nlp.disable_pipes(*other_pipes):  # only train parser
        optimizer = nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, losses=losses)
            print("Losses", losses)

    # test the trained model
    test_model(nlp)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        test_model(nlp2)


def test_model(nlp):
    texts = [
        "Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race; some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian, from the city of Tyre",
        "As a famine had arisen in Samos, Mnesarchus went thither to trade, and was naturalized there",
        "There also was born his son Pythagoras, who early manifested studiousness, but was later taken to Tyre, and there entrusted to the Chaldeans, whose doctrines he imbibed",
        "Thence he returned to Ionia, where he first studied under the Syrian Pherecydes, then also under Hermodamas the Creophylian who at that time was an old man residing in Samos",
    ]
    docs = nlp.pipe(texts)
    for doc in docs:
        print(doc.text)
        print([(t.text, t.dep_, t.head.text) for t in doc if t.dep_ != "-"])


if __name__ == "__main__":
    plac.call(main)

    # Expected output:
    # find a hotel with good wifi
    # [
    #   ('find', 'ROOT', 'find'),
    #   ('hotel', 'PLACE', 'find'),
    #   ('good', 'QUALITY', 'wifi'),
    #   ('wifi', 'ATTRIBUTE', 'hotel')
    # ]
    # find me the cheapest gym near work
    # [
    #   ('find', 'ROOT', 'find'),
    #   ('cheapest', 'QUALITY', 'gym'),
    #   ('gym', 'PLACE', 'find'),
    #   ('near', 'ATTRIBUTE', 'gym'),
    #   ('work', 'LOCATION', 'near')
    # ]
    # show me the best hotel in berlin
    # [
    #   ('show', 'ROOT', 'show'),
    #   ('best', 'QUALITY', 'hotel'),
    #   ('hotel', 'PLACE', 'show'),
    #   ('berlin', 'LOCATION', 'hotel')
    # ]


    # actual output for the new examples
    # Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race; some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian, from the city of Tyre
    # [('think', 'ROOT', 'think'), ('Pythagoras', 'SON', 'was'), ('son', 'NATIONALITY', 'was'), ('states', 'TEACHER', ','), ('he', 'PERSON', 'was'), ('Syrian', 'NATIONALITY', 'was'), ('Tyre', 'PARENT', 'of')]
    # As a famine had arisen in Samos, Mnesarchus went thither to trade, and was naturalized there
    # [('famine', 'ROOT', 'famine'), ('trade', 'NATIONALITY', ','), ('there', 'NATIONALITY', 'was')]
    # There also was born his son Pythagoras, who early manifested studiousness, but was later taken to Tyre, and there entrusted to the Chaldeans, whose doctrines he imbibed
    # [('was', 'ROOT', 'was'), ('Pythagoras', 'PERSON', ','), ('studiousness', 'NATIONALITY', ','), ('he', 'STUDENT', 'imbibed'), ('imbibed', 'TEACHER', ',')]
    # Thence he returned to Ionia, where he first studied under the Syrian Pherecydes, then also under Hermodamas the Creophylian who at that time was an old man residing in Samos
    # [('studied', 'ROOT', 'studied'), ('Pherecydes', 'TEACHER', 'under'), ('time', 'TEACHER', 'who'), ('Samos', 'NATIONALITY', 'old')]
