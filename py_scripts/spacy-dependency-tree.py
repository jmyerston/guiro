import spacy

nlp = spacy.load("en_core_web_sm")

#doc = nlp("The team is not performing well in the match")
#doc = nlp("Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race; some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian, from the city of Tyre.")
doc = nlp("Pythagoras was the son of Mnesarchus.")


for token in doc:
    print(str(token.text),  str(token.lemma_),  str(token.pos_),  str(token.dep_))


#>>> The, the, NOUN, nsubj
#>>> team, team, Noun, nsubh
#>>> Is, is, VERB, aux
#>>> Not, not, ADV, neg
#>>> Performing, perform, VERB, root
#>>> Well, well, ADV, advmod
#>>> In, in, ADP, prep
#>>> The, the, Noun, pobj
#>>> Match, match ,Noun, pobj

from spacy import displacy

displacy.serve(doc, style='dep')
