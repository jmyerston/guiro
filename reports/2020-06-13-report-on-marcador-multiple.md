# Updates to marcadormultiple.py

J. Dávila

I completed the specified features for marcadormultiple.py, our prodigy recipe to process a json file with the texts tasks mark them up with the patterns in text files stored in a directory and them allow prodigy to display the dependency relations in each tasks AND some text windows where our intented, logical relations are also displayed. 

## How to run the recipe

Given those requirements, the recipe can be invoked from the shell with the command:

`prodigy marcador <dataset> <json-source> <patternsdir> --exolabel <list_of_labels> -F ./marcadormultiple.py` 

For instance, with:

`prodigy marcador set5 ./books4.jsonl ./patterns --exolabel CORREF,REL -F ./marcadormultiple.py`

where CORREF y REL are external labels (exolabels) to be added to the labels internally used by the dependency matcher. The recipe can also be invoked without any external labels, like this: 

`prodigy marcador set4 ./books3.jsonl ./patterns -F ./marcadormultiple.py`

These are some screenshots of the prodigy interface:

[Recipe marcadormultiple](./corref-exolabel-example-03.png)

[Recipe marcadormultiple with many labelled items](./corref-exolabel-example-02.png)
     
Those shots do not show the lower part of the interface, where extracted logical relations are displayed. I found no way to display several text windows, one per relation, so that annotator could edit them right there. I tried to compose blocks in prodigy but, apparently, that is not allowed. So, it seems we will have to do some normalizations of tasks to have just one logical relation for every text paragraph, to allow easy edition on the web interface. 

Please notice that those logical relations are also produced as a csv file next to the recipe. 

We have a few other issues with the prodigy interface. There is an error I have not able to isolate when the task is an empty text or one filled with -- characters. It goes bad with an error message on the screen. 

Also, the interface is too small for a not so long paragraph as required to resolve correferences (anaphoras) like those 'he's in the texts. It marks them well, but it is hard to see it all at once. Moreover, we must remember that only local, same paragraph correferences can be resolved this way. If the original reference is in another task is not accessible for the annotator to mark. 

## On the patterns for the logical relations

Finally, a few lessons about our strategy to define patterns, based on:
[SpaCy's Dependency Matcher - An Introduction](http://markneumann.xyz/blog/dependency_matcher/#the-dependencymatcher)

A pattern is a set of triples with the basic form `<token or ENTITY>|<dependency relation>|<token or ENTITY>`, intended to be all applied simultaneously to match a text. For instance:

`took|prep|On On|pobj|sailing sailing|prep|to to|pobj|ENTITY_ONE took|nsubj|ENTITY_TWO took|dobj|ENTITY_THREE`

Notice that we are using ENTITY\_ONE, ENTITY\_TWO. ENTITY\_THREE, ENTITY\_FOUR and ENTITY\_FIVE, as placeholders for **any** token (Not even asking for a NOUN). 

But we must avoid the use of a token in the first, left place of a triple, repeated in the last, righ place of another triple because the dependency matcher assumes that it is a loop and fails with a confusing error (None error). 

This is the collection of those sets we are providing as a text file in the directory patterns:

`taken|auxpass|was taken|prep|to to|pobj|ENTITY_TWO`
`returned|nsubj|ENTITY_ONE returned|prep|to to|pobj|ENTITY_TWO`
`took|nsubj|ENTITY_TWO took|dobj|ENTITY_THREE`
`sailing|prep|to to|pobj|ENTITY_ONE`
`Returning|prep|to to|pobj|ENTITY_TWO`
`returned|prep|to to|pobj|ENTITY_TWO`
`Going|prep|to to|pobj|ENTITY_ONE`
`went|nsubj|ENTITY_ONE went|prep|to to|pobj|ENTITY_TWO`
`took|prep|On On|pobj|sailing sailing|prep|to to|pobj|ENTITY_ONE took|nsubj|ENTITY_TWO took|dobj|ENTITY_THREE`


End of report











