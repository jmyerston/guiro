import prodigy
from pathlib import Path 
import json

@prodigy.recipe("load_data")  # add argument annotations and shortcuts if needed
def load_data(dir_path):
    # the loader code here
   data_path = Path(dir_path)
   for file_path in data_path.iterdir():  # iterate over directory
       lines = Path(file_path).open("r", encoding="utf8")  # open file
       for line in lines:
           task = {"text": line}  # create one task for each line of text
           print(json.dumps(task))  # dump and print the JSON


