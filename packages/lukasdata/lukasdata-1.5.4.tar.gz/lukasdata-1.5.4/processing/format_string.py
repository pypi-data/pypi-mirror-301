import regex as re
from typing import Literal
import pandas as pd

def clean_multiple_space(string):
    regex=re.compile("\s{2,}")
    search=regex.findall(string)
    for item in search:
        string=string.replace(item," ")
    return string

def my_rstrip(string,stripped):
    if isinstance(stripped,str) and string.endswith(stripped):
        string=string[:-len(stripped)]
    return string

def unify_format(string:str,case_option: Literal['lower', 'upper'],strip=True,replace_whitespace=True):
    if isinstance(string,str):
        if case_option=="lower":
            string=string.lower()
        elif case_option=="upper":
            string=string.upper()
        if strip:
            string=string.strip()
        if replace_whitespace:
            string=string.replace(" ","_")
    else:
        return string
    return string
    
def bachelor_format(string):
    string=unify_format(string,case_option="upper")
    return string
    
def format_df(df:pd.DataFrame,rename_df={"idnr":"bvdid","name_native":"name","name_nat":"name","nr_months":"months","repbas":"conscode"},string_format=bachelor_format):
    df=df.apply(lambda x: list(map(string_format,x)))
    df.rename(columns=rename_df,inplace=True)
    return df
