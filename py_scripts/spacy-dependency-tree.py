import spacy

#nlp = spacy.load("en_core_web_sm")
nlp = spacy.load("en_diogenet_model")

#doc = nlp("The team is not performing well in the match")
#doc = nlp("Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race; some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian, from the city of Tyre.")
#doc = nlp("Pythagoras was the son of Mnesarchus.")
#doc = nlp("There also was born his son Pythagoras, who early manifested studiousness, but was later taken to Tyre, and there entrusted to the Chaldeans, whose doctrines he imbibed.")
#doc = nlp("Thence he returned to Ionia, where he first studied under the Syrian Pherecydes, then also under Hermodamas the Creophylian who at that time was an old man residing in Samos.")
#doc = nlp("On sailing to Italy, Mnesarchus took the youth Pythagoras with him.")
#doc = nlp("Returning to Ionia, he opened in his own country, a school, which is even now called Pythagoras's Semicircles, in which the Samians meet to deliberate about matters of common interest.")
#doc = nlp("Pythagoras then, longing to be with Hermodamas the Creophylian , returned to Samos.")
#doc = nlp("Going to Crete, Pythagoras besought initiation from the priests of Morgos, one of the Idaean Dactyli, by whom he was purified with the meteoritic thunder-stone.")
doc = nlp("Pythagoras then went to Delos, to visit the Syrian Pherecydes, formerly his teacher, who was dangerously sick, to nurse him.")



for token in doc:
    print(str(token.text),  str(token.lemma_),  str(token.pos_),  str(token.dep_))
    
for ent in doc.ents:
    print(ent.text, ent.label_)


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
