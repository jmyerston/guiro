#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import spacy
from spacy import displacy
from spacy.matcher import Matcher


# In[ ]:


import stanza
from spacy_stanza import StanzaLanguage
from spacy import displacy


# In[ ]:


#stanza.download('grc') # download Greek model


# In[ ]:


snlp = stanza.Pipeline(lang="grc")
nlp = StanzaLanguage(snlp)


# In[ ]:


text_as_string = open('../texts/porph_gr.txt', 'r').read()
text_as_string = text_as_string.replace("\r"," ").replace("\n"," ")
#nlp = spacy.load("en_diogenet_model")
doc = nlp(text_as_string)
matcher = Matcher(nlp.vocab)
matched_sents = []  # Collect data of matched sentences to be visualized


# In[ ]:


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


# In[ ]:


#print(text_as_string)


# In[114]:


pattern_went_to = [{"TEXT": "εἰς"},{"DEP": "det","OP": "?"},{"POS": "PROPN"}]


# In[115]:


#pattern_went_to = [{"DEP": "obl"}]


# In[116]:


matcher.add("went_to", collect_sents, pattern_went_to)


# In[117]:


#doc = nlp(text_as_string)
matches = matcher(doc)


# In[118]:


displacy.serve(matched_sents, style="ent", manual=True)


# In[ ]:





# In[ ]:




