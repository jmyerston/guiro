# relation_extraction_diogenet.py based on bio_relation_extraction.py

import spacy
from spacy import displacy
import random
import matplotlib.pyplot as plt
import numpy
from collections import Counter

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

#nlp = spacy.load("en_core_sci_md")
nlp = spacy.load("en_diogenet_model")

from spacy.matcher import DependencyMatcher
from collections import defaultdict
from typing import Dict, List


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


#x example = "was|nsubj|START_ENTITY was|attr|son son|prep|of of|pobj|END_ENTITY"

#example = "was|nsubj|Pythagoras was|attr|son son|prep|of of|pobj|Mnesarchus"
#example = "was|nsubj|ENTITY_ONE was|attr|son son|prep|of of|pobj|ENTITY_TWO"
#1 example = "taken|auxpass|was taken|prep|to to|pobj|ENTITY_TWO"
#2 example = "returned|nsubj|ENTITY_ONE returned|prep|to to|pobj|ENTITY_TWO"
#x example = "sailing|prep|to to|pobj|ENTITY_ONE took|nsubj|ENTITY_TWO took|dobj|ENTITY_THREE"
#3 example = "took|nsubj|ENTITY_TWO took|dobj|ENTITY_THREE"
#3a example = "sailing|prep|to to|pobj|ENTITY_ONE"
#x example = "sailing|prep|to to|pobj|ENTITY_ONE took|nsubj|ENTITY_TWO"
#x example = "opened|nsubj|ENTITY_ONE returning|prep|to to|pobj|ENTITY_TWO"
#4 example = "Returning|prep|to to|pobj|ENTITY_TWO"
#5 example = "returned|prep|to to|pobj|ENTITY_TWO"
#6 example = "Going|prep|to to|pobj|ENTITY_ONE"
example = "went|nsubj|ENTITY_ONE went|prep|to to|pobj|ENTITY_TWO"


#sent = "The ICE inhibitor Z-YVAD-FMK prevented the release of IL-1beta evoked by DNFB ."
#sent = "Many think that Pythagoras was the son of Mnesarchus, but they differ as to the latter's race; some thinking him a Samian, while Neanthes, in the fifth book of his Fables states he was a Syrian, from the city of Tyre."


#1 sent = "There also was born his son Pythagoras, who early manifested studiousness, but was later taken to Tyre, and there entrusted to the Chaldeans, whose doctrines he imbibed."
#2 sent = "Thence he returned to Ionia, where he first studied under the Syrian Pherecydes, then also under Hermodamas the Creophylian who at that time was an old man residing in Samos."
#3 sent = "On sailing to Italy, Mnesarchus took the youth Pythagoras with him."
#4 sent = "Returning to Ionia, he opened in his own country, a school, which is even now called Pythagoras's Semicircles, in which the Samians meet to deliberate about matters of common interest."
#5 sent = "Pythagoras then, longing to be with Hermodamas the Creophylian , returned to Samos."
#6 sent = "Going to Crete, Pythagoras besought initiation from the priests of Morgos, one of the Idaean Dactyli, by whom he was purified with the meteoritic thunder-stone."
sent = "Pythagoras then went to Delos, to visit the Syrian Pherecydes, formerly his teacher, who was dangerously sick, to nurse him."



#sent = "Pythagoras was the son of Mnesarchus"

# rules are of the form: A | governs (via relation) | B
# So for semregex we need A > B OR B < A, which might be better as spacy t.dep_ refers to the word's parent.

#  For this subtree, it looks like:
#                prevented
#       start_ent           release
#                                   end_entity

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

#pattern = [
#    {"SPEC": {"NODE_NAME": "prevented"}, "PATTERN": {"ORTH": "prevented"}},
#    {"SPEC": {"NODE_NAME": "start_entity", "NBOR_RELOP": ">", "NBOR_NAME": "prevented"}, "PATTERN": {"DEP": "nsubj"}},
#    {"SPEC": {"NODE_NAME": "release", "NBOR_RELOP": ">", "NBOR_NAME": "prevented"}, "PATTERN": {"DEP": "dobj", "ORTH":"release"}},
#    {"SPEC": {"NODE_NAME": "end_entity", "NBOR_RELOP": ">", "NBOR_NAME": "release"}, "PATTERN": {"DEP": "nmod"}},
#
#]

rules = [rule.split("|") for rule in example.split(" ")]
print(rules)
print()

doc = nlp(sent)
#visualise_doc(doc) #comment to visualise the subtree below

constructed_pattern = construct_pattern(rules)

matcher = DependencyMatcher(nlp.vocab)

matcher.add("pattern1", None, constructed_pattern)
print(matcher._patterns)
print(matcher._nodes)
print(matcher._tree)
print(matcher. _keys_to_token)
print(matcher._root)
print(matcher._entities)

matches = matcher(doc)
print(matches)
subtree = matches[0][1][0]

visualise_subtrees(doc, subtree)
