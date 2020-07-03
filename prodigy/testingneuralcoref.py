# testingneuralcoref.py

import spacy
nlp = nlp=spacy.load("en_core_web_lg")

# Add neural coref to SpaCy's pipe
import neuralcoref
neuralcoref.add_to_pipe(nlp)

# You're done. You can now use NeuralCoref as you usually manipulate a SpaCy document annotations.
#doc = nlp(u'My sister has a dog. She loves him.')
#doc = nlp(u"Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race; some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian, from the city of Tyre.")
#doc=nlp("Jacinto Dávila loves Juliet. But he bores her to death")
#x doc=nlp("Juliet's boyfriend loves Juliet. But he bores her to death")
#doc=nlp("Pythagoras loves Juliet. But he bores her to death")
#doc=nlp("Pythagoras II loves Juliet. But he bores her to death")
#doc=nlp("Pythagoras from Tyre loves Juliet. But he bores her to death")
doc=nlp("Thraso II loves Juliet. But he bores her to death")
#x doc=nlp("Romeo Montague loves Juliet. But he bores her to death")

if doc._.has_coref:
    for mention in doc._.coref_clusters:
        #propn, list_of_equiv = mention
        #print(mention.i, mention.main, mention.mentions)
        #print(propn, end="")
        print(mention.main) #, dir(mention.main))
        #for equiv in list_of_equiv:
        #    print(" is the reference for ", equiv)
        #print(doc._.coref_clusters[mention])
        for equiv in mention.mentions:
            if equiv.text == "him" or equiv.text == "She" or equiv.text == "he" or equiv.text == "her" : 
                print("    is the reference for ", equiv.string)#, equiv.text, dir(equiv))


def get_main_ref(doc, token):
    for mention in doc._.coref_clusters:
        for equiv in mention.mentions:
            if equiv.text == token.text: 
                return mention.main
    return token


print(get_main_ref(doc, doc[8]))

#print(doc._.has_coref)
#print(doc._.coref_clusters)
