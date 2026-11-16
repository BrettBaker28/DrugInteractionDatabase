#######Description######
#
#Downloads new DDInter version. 
#Gets new cvs files and concats them into one.
#

######To Do######
#
#Implement pull code.
#

import pandas as pd
from pathlib import Path

KEYS = ("File name", "Dataframe")

folder_path = Path("ddinter_csv")
ddinter_dataframe = pd.DataFrame()

for file_path in folder_path.iterdir():
    if file_path.is_file():
        dataframe = pd.read_csv(file_path)
        ddinter_dataframe = pd.concat([ddinter_dataframe, dataframe])

ddinter_dataframe.to_csv("interaction_csv/severity.csv", index = False)