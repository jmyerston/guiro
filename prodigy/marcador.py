# marcador.py v 0.7 marcador de relaciones a partir de patrones
# marcando la relación went to (ver add_matches_to_stream)
# leyendo un archivo jsonl con los textos originales 
# produciendo un archivo csv, went_to_relation.csv, con las relaciones y sus párrafos de origen 

import prodigy
from prodigy.components.loaders import JSONL
from prodigy.components.preprocess import add_tokens
import spacy
from spacy import displacy
import random
import matplotlib.pyplot as plt
import numpy
from collections import Counter
from spacy.matcher import DependencyMatcher
from collections import defaultdict
from typing import Dict, List
import csv
from pathlib import Path

#nlp = spacy.load("en_core_sci_md")
nlp = spacy.load("en_diogenet_model")


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
            elif child in {"ENTITY_ONE", "ENTITY_TWO", "ENTITY_THREE"}:
                print("entity matched")
                #token_pattern["ENT_TYPE"] = {"NOT_IN": [""]}
                #token_pattern["POS"] = "NOUN"
                #token_pattern["TEXT"] = {"REGEX": "*"}
            # If we are on part of the path which is not the start/end entity,
            # we want the word to match. This could be made very flexible, e.g matching
            # verbs instead, etc.
            else:
                token_pattern["ORTH"] = child

            node["PATTERN"] = token_pattern

            pattern.append(node)
            add_node(child, pattern)

    pattern = [{"SPEC": {"NODE_NAME": root}, "PATTERN": {"ORTH": root}}]
    add_node(root, pattern)

    assert len(pattern) < 20
    return pattern


def add_matches_to_stream(stream, patterns):
   # patterns = "went|nsubj|ENTITY_ONE went|prep|to to|pobj|ENTITY_TWO"
   matcher = DependencyMatcher(nlp.vocab)
   count = 0
   for pattern in patterns:
       rules = [rule.split("|") for rule in pattern.split(" ")]
       constructed_pattern = construct_pattern(rules)
       count += 1
       print("Adding these patterns ", rules)
       matcher.add("patron "+str(count), None, constructed_pattern)
         
   print("Matcher full settings >")
   print("patterns: ", matcher._patterns)
   print("keys to token", matcher._keys_to_token)
   print("root ", matcher._root)
   print("entities ", matcher._entities)
   print("callbacks ", matcher._callbacks)
   print("nodos ", matcher._nodes)
   print("árbol ", matcher._tree)
   print("< Matcher full settings")
   
   # salida csv
   # based on https://stackoverflow.com/questions/33309436/python-elementtree-xml-output-to-csv
   with open('all_relations.csv', 'w', newline='') as r:  # [went, Pythagoras, to, Delos]
       writer = csv.writer(r,  delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
       #writer.writerow(['id', 'relation','subject','to','destination', 'source_text'])  # WRITING HEADERS
       # rows vary in lenght. Therefore cannot use just one header
       counter = 1;
       for eg in stream:
           doc = nlp(eg["text"])  # get the text to be matched upon
           matches = matcher(doc) # do the matching
           print(eg["text"])
           print(matches)
       
           eg["relations"] = []
           for match_id, token_idxs in matches:
               for each_pattern in token_idxs: 
                   tokens = [doc[i] for i in each_pattern]
                   heads = [doc[i].head for i in each_pattern]
                   deps = [doc[i].dep_ for i in each_pattern]
                   print("tokens>")
                   print(tokens)
                   print(heads)
                   print(deps)
                   print("<")
                   one_row = [counter] + tokens + [eg["text"]] 
                   writer.writerow(one_row) # to the csv
                   counter += 1
                 
                   branch = matcher._tree[match_id] # realnente es una lista de branches de este id
                   print(branch)
                   
                   for k in branch[0]:
                       for rel, j in branch[0][k]:
                           print(tokens[k],"--",deps[j],rel,tokens[j]) 
                           eg["relations"].append({"child": int(each_pattern[j]), "head": int(each_pattern[k]), "label": deps[j]})             

           print( eg["relations"])
           yield eg



@prodigy.recipe("marcador")
def custom_dep_recipe(dataset, source, patterns_source):
    patterns = load_patterns(patterns_source)
    
    stream = JSONL(source)                          # load the data
    stream = add_tokens(spacy.blank("en"), stream)  # add "tokens" to stream
    stream = add_matches_to_stream(stream, patterns)  # add custom patterns

    return {
        "dataset": dataset,      # dataset to save annotations to
        "stream": stream,        # the incoming stream of examples
        "view_id": "relations"  # annotation interface to use
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


