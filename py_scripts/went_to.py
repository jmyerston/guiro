# spacy_relationsxtractor.py
# version 0.5
#
# from https://spacy.io/usage/rule-based-matching#example1
import spacy
from spacy import displacy
from spacy.matcher import Matcher

text_as_string = open('../texts/dl_book1.txt', 'r').read()
text_as_string = text_as_string.replace("\r"," ").replace("\n"," ")
nlp = spacy.load("en_diogenet_model")
matcher = Matcher(nlp.vocab)
matched_sents = []  # Collect data of matched sentences to be visualized

def collect_sents(matcher, doc, i, matches):
    match_id, start, end = matches[i]
    span = doc[start:end]  # Matched span
    sent = span.sent  # Sentence containing matched span
    # Append mock entity for match in displaCy style to matched_sents
    # get the match span by ofsetting the start and end of the span with the
    # start and end of the sentence in the doc
    string_id = nlp.vocab.strings[match_id]
    match_ents = [{
        "start": span.start_char - sent.start_char,
        "end": span.end_char - sent.start_char,
        "label": "RELATION: "+string_id,
    }]
    matched_sents.append({"text": sent.text, "ents": match_ents})

# Pythagoras was the son of Mnesarchus
"""pattern_son_of = [{},  {"LEMMA": "be"}, {"LOWER": "the"}, {"LOWER": "son"}, {"LOWER": "of"},{}]


pattern_son_of2 = [{'ENT_TYPE': 'PERSON'},
           {'LEMMA': 'be', 'OP': '?'},
           {'POS': 'DET', 'OP': '?'},
           {'LEMMA': 'son'},
           {'POS': 'ADP', 'OP': '?'},
           {'ENT_TYPE': 'PERSON'}] """
# Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race;
# some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian,
# from the city of Tyre.

pattern_went_to = [{"LEMMA": {"REGEX": "go|sail|take|return"}},
                   {"TEXT": {"REGEX": "to|towards"}},
                   {"ENT_TYPE": "GPE"}]



#matcher.add("son_of", collect_sents, pattern_son_of) add pattern
#matcher.add("son_of2", collect_sents, pattern_son_of2)

matcher.add("went_to", collect_sents, pattern_went_to)

doc = nlp(text_as_string)
matches = matcher(doc)

# Serve visualization of sentences containing match with displaCy
# set manual=True to make displaCy render straight from a dictionary
# (if you're not running the code within a Jupyer environment, you can
# use displacy.serve instead)
# displacy.render(matched_sents, style="ent", manual=True)
displacy.serve(matched_sents, style="ent", manual=True)
