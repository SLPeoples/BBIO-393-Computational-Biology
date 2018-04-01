import pandas as pd

df = pd.read_csv("C:/Users/Ripti/Dropbox/Peoples/CSS143/BBIO-393-Computational-Biology/Project2/data/test_data/test_node_table.txt", sep="\t")
try:
    print(df.skrgj)
except AttributeError as e:
    print(e)