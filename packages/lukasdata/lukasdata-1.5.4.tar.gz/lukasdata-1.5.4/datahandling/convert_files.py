import pandas as pd

def csv_to_excel(path):
    csv=pd.read_csv(path)
    csv.to_excel(path[:-4]+".xlsx")
