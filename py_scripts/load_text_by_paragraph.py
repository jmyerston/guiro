# load_text_by_paragraph.py  To load a text into json paragraph by paragraph
# It assumes that paragraphs are separated by \n only lines

import prodigy
from pathlib import Path 
import json

@prodigy.recipe("load_text")  # add argument annotations and shortcuts if needed
def load_data(dir_path):
    # the loader code here
   data_path = Path(dir_path)
   for file_path in data_path.iterdir():  # iterate over directory
       lines = Path(file_path).open("r", encoding="utf8")  # open file
       paragraph = "";
       for line in lines:
           if line!="\n": 
               paragraph += line
           else: 
               paragraph = paragraph.replace("\n", " ") # replace \n from the rest
               paragraph = paragraph.replace("\u00a0", " ") # replace \u00a0 from the rest
               task = {"text": paragraph}  # create one task for each paragraph of text
               print(json.dumps(task))  # dump and print the JSON
               paragraph = ""


