# spacy_relationsxtractor.py
# version 0.5
#
# from https://spacy.io/usage/rule-based-matching#example1
import spacy
from spacy import displacy
from spacy.matcher import Matcher

text_as_string = open('../texts/porphyry.txt', 'r').read()
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
pattern_son_of = [{},  {"LEMMA": "be"}, {"LOWER": "the"}, {"LOWER": "son"}, {"LOWER": "of"},
           {}]
# Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race;
# some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian,
# from the city of Tyre.
pattern_nationality = [{"ENT_TYPE": "GPE"}]
pattern_city = [{"LOWER": "from"}, {"LOWER": "the"}, {"LOWER": "city"}, {"LOWER": "of"},
           {}]

matcher.add("son_of", collect_sents, pattern_son_of)  # add pattern´´´´´´´´´
matcher.add("nationality", collect_sents, pattern_nationality)
matcher.add("from_city", collect_sents, pattern_city)

doc = nlp(text_as_string)
matches = matcher(doc)

# Serve visualization of sentences containing match with displaCy
# set manual=True to make displaCy render straight from a dictionary
# (if you're not running the code within a Jupyer environment, you can
# use displacy.serve instead)

#displacy.serve(matched_sents, style="ent", manual=True)

# In this case displacy.render is used in order to create different files than be further distributed and studied

sentence_spans = list(doc.sents)
html_sentence_spans = displacy.render(sentence_spans, style="dep", page=True)
open('sentence_spans.html','w', encoding='utf-8').write(html_sentence_spans)

html_doc = displacy.render(doc, style='ent', page=True)
open('doc.html','w', encoding='utf-8').write(html_doc)

html_matched_sents = displacy.render(matched_sents, style="ent", manual=True, page=True)
open('matched_sents.html','w', encoding='utf-8').write(html_matched_sents)

