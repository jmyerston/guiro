# marcador.py v 2.0 (basado en marcadormultiple.py v 1.1) 
# Funciona de dos maneras. Como simple pytho script marcador de relaciones 
# a partir de patrones guardados en un archivo json dado. 
# Lee un archivo jsonl con los textos originales 
# y recibe el nombre del archivo para el vaciado intermedio y en un csv.
# La segunda forma es como recipe prodigy para invocar la interfaz con
# la que un anotador puede aprobar, corregir o rechazar instancias de relaciones.

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
from prodigy.util import split_string
import spacy
from spacy import displacy
import random
import matplotlib.pyplot as plt
import numpy
from collections import Counter, defaultdict
from spacy.matcher import DependencyMatcher
from typing import Dict, List, Optional
from spacy.pipeline import merge_entities
import copy
import json

import csv
from pathlib import Path
#import neuralcoref

#nlp = spacy.load("en_core_sci_md")
#nlp = spacy.load("en_core_web_sm")
#nlp = spacy.load("en_diogenet_model")
# nlp.add_pipe(merge_entities)
nlp = nlp=spacy.load("en_core_web_lg")
#neuralcoref.add_to_pipe(nlp)


def visualise_doc(doc):
    #displacy.render(doc, style="dep", options={"distance": 120}, jupyter=True)
    #displacy.render(doc, style="ent", options={"distance": 120}, jupyter=True)
    displacy.serve(doc, style="dep", options={"distance": 120})
    displacy.serve(doc, style="ent", options={"distance": 120})


def visualise_subtrees(doc, subtrees):

    words = [{"text": t.text, "tag": t.pos_} for t in doc]

    if not isinstance(subtrees[0], list):
        subtrees = [subtrees]

    for subtree in subtrees:
        arcs = []

        tree_indices = set(subtree)
        for index in subtree:

            token = doc[index]
            head = token.head
            if token.head.i == token.i or token.head.i not in tree_indices:
                continue

            else:
                if token.i < head.i:
                    arcs.append(
                        {
                            "start": token.i,
                            "end": head.i,
                            "label": token.dep_,
                            "dir": "left",
                        }
                    )
                else:
                    arcs.append(
                        {
                            "start": head.i,
                            "end": token.i,
                            "label": token.dep_,
                            "dir": "right",
                        }
                    )
        print("Subtree: ", subtree)
        # displacy.render(
        displacy.serve(
            {"words": words, "arcs": arcs},
            style="dep",
            options={"distance": 120},
            manual=True,
            #jupyter=True
        )

PTB_BRACKETS = {
    "-LRB-": "(",
    "-RRB-": ")",
    "-LCB-": "{",
    "-RCB-": "}",
    "-LSB-": "[",
    "-RSB-": "]",
}

def clean_and_parse(sent: str, nlp):

    tokens = sent.strip().split(" ")

    new = []

    for token in tokens:
        new_token = PTB_BRACKETS.get(token, None)
        if new_token is None:
            new.append(token)
        else:
            new.append(new_token)

    return nlp(" ".join(new))


def parse_dep_path(dep_string: str):

    rules = [rule.split("|") for rule in dep_string.split(" ")]

    for triple in rules:

        if triple[0] in PTB_BRACKETS:
            triple[0] = PTB_BRACKETS[triple[0]]

        if triple[2] in PTB_BRACKETS:
            triple[2] = PTB_BRACKETS[triple[2]]

        if triple[1] == "nsubj:xsubj":
            triple[1] = "nsubj"

        if triple[1] == "nsubjpass:xsubj":
            triple[1] = "nsubjpass"
    return rules


def check_for_non_trees(rules: List[List[str]]):

    parent_to_children = defaultdict(list)
    seen = set()
    has_incoming_edges = set()
    for (parent, rel, child) in rules:
        seen.add(parent)
        seen.add(child)
        has_incoming_edges.add(child)
        if parent == child:
            return None
        parent_to_children[parent].append((rel, child))

    # Only accept strictly connected trees.
    roots = seen.difference(has_incoming_edges)
    if len(roots) != 1:
        return None

    root = roots.pop()
    seen = {root}

    # Step 2: check that the tree doesn't have a loop:
    def contains_loop(node):
        has_loop = False
        for (_, child) in parent_to_children[node]:
            if child in seen:
                return True
            else:
                seen.add(child)
                has_loop = contains_loop(child)
            if has_loop:
                break

        return has_loop

    if contains_loop(root):
        return None

    return root, parent_to_children

def person_labels():
    return ["PERSON", "PERSON_1", "PERSON_2", "PERSON_3", "PERSON_4", "PERSON_5"]
    
def location_labels():
    return ["LOC", "GPE", "LOC_1", "GPE_1", "LOC_2", "GPE_2", "LOC_3", "GPE_3"]
    
def wildcard_labels():
    return ["ANY", "ANY_1","ANY_2","ANY_3","ANY_4","ANY_5","WILDCAR", "*", "WILDC"]
    
def is_pronoun(token):
    if str(token.lemma_) == "-PRON-":
        return True 
    return False 

def construct_pattern(rules: List[List[str]]):
    """
    Idea: add patterns to a matcher designed to find a subtree in a spacy dependency tree.
    Rules are strictly of the form "CHILD --rel--> PARENT". To build this up, we add rules
    in DFS order, so that the parent nodes have already been added to the dict for each child
    we encounter.
    """
    # Step 1: Build up a dictionary mapping parents to their children
    # in the dependency subtree. Whilst we do this, we check that there is
    # a single node which has only outgoing edges.

    if "dep" in {rule[1] for rule in rules}:
        return None

    ret = check_for_non_trees(rules)

    if ret is None:
        return None
    else:
        root, parent_to_children = ret

    def add_node(parent: str, pattern: List):

        for (rel, child) in parent_to_children[parent]:

            # First, we add the specification that we are looking for
            # an edge which connects the child to the parent.
            node = {
                "SPEC": {
                    "NODE_NAME": child,
                    "NBOR_RELOP": ">",
                    "NBOR_NAME": parent},
            }

            # DANGER we can only have these options IF we also match ORTH below, otherwise it's torturously slow.
            # token_pattern = {"DEP": {"IN": ["amod", "compound"]}}

            # Now, we specify what attributes we want this _token_
            # to have - in this case, we want to match a certain dependency
            # relation specifically.
            token_pattern = {"DEP": rel}

            # Additionally, we can specify more token attributes. So here,
            # if the node refers to the start or end entity, we require that
            # the word is part of an entity (spacy syntax is funny for this)
            # and that the word is a noun, as there are some verbs annotated as "entities" in medmentions.

            if child in {"START_ENTITY", "END_ENTITY"}:
                token_pattern["ENT_TYPE"] = {"NOT_IN": [""]}
                token_pattern["POS"] = "NOUN"
            elif child in {"ENTITY_ONE", "ENTITY_TWO", "ENTITY_THREE", "ENTITY_FOUR", "ENTITY_FIVE"}:
                pass
                #print(child)
                #token_pattern["ENT_TYPE"] = {"NOT_IN": [""]}
                #token_pattern["POS"] = "NOUN"
                #token_pattern["TEXT"] = {"REGEX": "*"}
            # If we are on part of the path which is not the start/end entity,
            # we want the word to match. This could be made very flexible, e.g matching
            elif child in person_labels():
                token_pattern["ENT_TYPE"] = "PERSON"
                #print("PERSON ", child)
            elif child in location_labels():
                token_pattern["ENT_TYPE"] = "GPE"
                #print("LOCATION ", child)
            elif child in wildcard_labels():
                pass
                #print("ANYTHING ", child)
            else:
                #token_pattern["ORTH"] = child
                token_pattern["LEMMA"] = child  #working with lemmas

            node["PATTERN"] = token_pattern

            pattern.append(node)
            add_node(child, pattern)

    #pattern = [{"SPEC": {"NODE_NAME": root}, "PATTERN": {"ORTH": root}}]
    pattern = [{"SPEC": {"NODE_NAME": root}, "PATTERN": {"LEMMA": root}}] # to use lemmas as root
    add_node(root, pattern)

    assert len(pattern) < 20
    return pattern

def get_main_ref(doc, token):
    for mention in doc._.coref_clusters:
        for equiv in mention.mentions:
            if equiv.text == token.text: 
                return mention.main
    return token


def add_matches_to_stream(stream, patterns, datafile, csvfile):    
    #print(patterns)

    patternid_and_lrels = {} # a dict for (patternids: lrel) items
       
    def get_lrel(patternid):
       lrel = patternid_and_lrels[patternid]
       llrel = [x.strip() for x in lrel.split(",")]  # transform the lrel string into a list
       return llrel
       
    def get_patternid(lrel):
        for patterind in patternid_and_lrels.keys():
            if patternid_and_lrels[patternid] == lrel:
                return patternid
           
    count = 0
       
    matcher = DependencyMatcher(nlp.vocab)
    for generated in patterns:
        #print(str(generated))
        #print(dir(generated))
        [(lrelation, pattern)] = generated.items()
           
        rules = [rule.split("|") for rule in pattern.split(" ")]
        constructed_pattern = construct_pattern(rules)
        # print("Adding these patterns ", constructed_pattern)
        matcher.add(str(lrelation)+","+str(count), None, constructed_pattern)
        #print("relation ", lrelation)
        keyslist = list(matcher._nodes.keys())
        #print("node ", keyslist[count])
        patternid_and_lrels[keyslist[count]] = lrelation+","+str(count)
        count += 1


    print(patternid_and_lrels)
         
    #print("Matcher's settings >")
    #print("patterns: ", matcher._patterns)
    #print("keys to token", matcher._keys_to_token)
    #print("root ", matcher._root)
    #print("entities ", matcher._entities)
    #print("callbacks ", matcher._callbacks)
    #print("nodes ", matcher._nodes)
    #print("tree ", matcher._tree)
    #print("< Matcher's settings")
    
    def get_element_in_nodes(patternid, element):
        listofpatterns = matcher._nodes[patternid]
        print(element, "> ", listofpatterns[0][element])
        return listofpatterns[0][element]

    # first output of the process, a csv
    # based on https://stackoverflow.com/questions/33309436/python-elementtree-xml-output-to-csv
    with open(csvfile, 'w', newline='') as r:  # [went, Pythagoras, to, Delos]
        writer = csv.writer(r,  delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)


        counter = 1;
        alltegs = []    
        for eg in stream:
            doc = nlp(eg["text"])  # get the text to be matched upon
           
            if eg["text"]=="":
                #continue  # jump over empty tasks
                #eg["text"]=="(DELETE empty lines)"
                return []
            
            matches = matcher(doc) # do the matching
           
            print("aplicando al texto >",eg["text"], "<")
            print(" aciertos ", matches)
       
            eg["relations"] = []
            eg["logical_relation"] = ""
            #eg["rel"] = []
            #str_rel = ""
      
            for match_id, token_idxs in matches:
                teg= copy.deepcopy(eg) # deep copy of the example from the original stream
                final_rel = ""
                for each_pattern in token_idxs:
                    tokens = [doc[i] for i in each_pattern]
                    #heads = [doc[i].head for i in each_pattern]
                    deps = [doc[i].dep_ for i in each_pattern]
                    #print("tokens>", tokens, "<")
                    #    print(tokens)
                    #    print(heads)
                    #    print(deps)
                    #print("<")
                
                    lrelation = get_lrel(match_id)
                    final_rel += lrelation[0]  # takes the name of the relation only
                    for element in lrelation: 
                        if element != lrelation[0] and element != lrelation[len(lrelation)-1]: # neither first nor last
                            wordnumber = get_element_in_nodes(match_id, element)
                            final_rel = final_rel+", "+str(tokens[wordnumber])
                            #if doc._.has_coref: # solving correfs
                            #    if is_pronoun(tokens[wordnumber]):
                            #       actual_ref = get_main_ref(doc, tokens[wordnumber])
                            #       final_rel = final_rel+", "+str(actual_ref)
                            #    else:
                            #       final_rel = final_rel+", "+str(tokens[wordnumber])  
                            #else:
                            #    final_rel = final_rel+", "+str(tokens[wordnumber])
                
                    one_row = [counter] + tokens + [eg["text"]] 
                    writer.writerow(one_row) # to the csv
                    
                    #eg["logical_relation"].append({"instance"+str(counter):str(tokens).strip('[]')})  # adding the logical relation to the db too
                    teg["logical_relation"] = final_rel # str(tokens).strip('[]')
                    #str_rel += " instance "+str(counter)+" ("+str(tokens).strip('[]')+")\n"
                    counter += 1
                 
                    branch = matcher._tree[match_id] # realnente es una lista de branches de este id
                    #print(branch)
                   
                    for k in branch[0]:
                        for rel, j in branch[0][k]:
                            #print(tokens[k],"--",deps[j],rel,tokens[j])
                            teg["relations"].append({"child": int(each_pattern[j]), "head": int(each_pattern[k]), "label": deps[j]})             

                    #teg["rel"] = [str_rel]
                    #print("teg>", teg)

                    if teg["relations"]==[]:
                        teg.pop("relations") 
                    #else: 
                    #    print("relations: ", teg["relations"]) 
               
                    if teg["logical_relation"]==[]:  
                        teg.pop("logical_relation")  
           
                    alltegs += [teg]  # it adds one copy of the example subjected to one pattern at the time
 
 
        print("\nAll new eg>", alltegs, "<\n") 
 
 
    # producing second output of the process
    with open(datafile, 'w') as outfile:
        for neg in alltegs:
            json.dump(neg, outfile)
            outfile.write('\n')


@prodigy.recipe("marcador",
    source=("INPUT: The source data as a JSONL file", "positional", None, str),
    patterns_source=("INPUT: The patterns as a JSONL file", "positional", None, str),
    datafile=("OUTPUT: A JSONL file to store data in", "positional", None, str),
    csvfile=("OUTPUT: A csv file with the logical relations", "positional", None, str),
)
def custom_dep_recipe(source, patterns_source, datafile, csvfile):
    # patterns = load_patterns(patterns_source)
    #print("loading the patterns")
    patterns = JSONL(patterns_source)
    
    #print("loading the original data")
    stream0 = JSONL(source)                          # load the data
    stream0 = add_tokens(spacy.blank("en"), stream0)  # add "tokens" to stream
    add_matches_to_stream(stream0, patterns, datafile, csvfile)  # add custom patterns to a json intermediate file

    return {
    }


@prodigy.recipe("anotador",
    dataset=("The dataset to use", "positional", None, str),
    source=("The source data as a JSONL file", "positional", None, str),
    exolabel=("One or more comma-separated labels", "option", "l", split_string)
)
def custom_dep_recipe(dataset, source, exolabel: Optional[List[str]] = None):
    # from https://prodi.gy/docs/custom-recipes
    blocks = [
        {"view_id": "relations"},
        {"view_id": "text_input", "field_id": "logical_relation", "field_label": "Relation: ", "field_rows": 1, "field_autofocus": True}
        #{"view_id": "blocks" }
        #{"view_id": "choice", "text": None},
        #{"view_id": "text_input", "field_rows": 3, "field_label": "Explain your decision"}
    ]
    
    stream = JSONL(source)
    
    if exolabel is None: 
        labels = ["nsubj", "prep", "pobj", "dobj", "auxpass"]
    else:
        labels = ["nsubj", "prep", "pobj", "dobj", "auxpass"] + exolabel

    return {
        "dataset": dataset,      # dataset to save annotations to
        "stream": stream,        # the incoming stream of examples
        "view_id": "blocks",     # annotation interface to use
        "config": {
            "labels": labels,
            "blocks": blocks
        }
    }


# https://deploy-preview-11--prodi-gy.netlify.app/docs/custom-recipes
def update(answers):
    texts = [eg["text"] for eg in answers]
    ents = [(span["start"], span["end"], span["label"]) for span in eg["spans"]]
    annots = [{"entities": ent} for ent in ents]
    losses = {}
    nlp.update(texts, annots, losses=losses)
    return losses["ner"]


def load_patterns(pattern_pathfile):
    data_path = Path(pattern_pathfile)
    for file_path in data_path.iterdir():  # iterate over directory
        lines = Path(file_path).open("r", encoding="utf8")  # open file
        lines = [line.rstrip("\n") for line in lines]
    return lines






