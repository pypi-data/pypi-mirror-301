import regex as re

rechtsform_regex=re.compile(r"UG\s*\(haftungsbeschränkt\)|\bUG\b|\bAG\b|\beG\b|Unternehmensgesellschaft|\be\.k\b|GmbH & Co\. KG|\bmbH\b|PartG|GbR|PartG|StGes|\bSE\b|KGaA|Handelsgesellschaft mit beschränkter Haftung|Gesellschaft mit beschränkter Haftung|KG|\bGmbH\b|OHG",flags=re.I) #wir müssen es case sensitive machen, möglicherweise sind wir jetzt zu restriktiv 

rechtsform_regex_bachelor_format=re.compile(r"UG_\(haftungsbeschränkt\)|(?<=_)UG|(?<=_)AG|(?<=_)eG|Unternehmensgesellschaft|\be\.k\b|GmbH_& Co\._KG|(?<=_)mbH|PartG|GbR|PartG|StGes|(?<=_)SE|(?<=_)KGaA|Handelsgesellschaft_mit_beschränkter_Haftung|Gesellschaft_mit_beschränkter_Haftung|(?<=_)KG|(?<=_)GmbH|(?<=_)OHG",flags=re.I)

def return_rechtsform(company_name):
      rechtsform=rechtsform_regex_bachelor_format.findall(company_name)
      if rechtsform !=[]:
            rechtsform=rechtsform[0]
            return rechtsform
      
def strip_rechtsform(company_name):
    rechtsform_regex_search=rechtsform_regex.findall(company_name)
    if len(rechtsform_regex_search)>=1:
        company_name=company_name.rstrip(rechtsform_regex_search[0]).lower().rstrip()
    return company_name     

def strip_rechtsform_list(lst):
    new_list=[]
    for item in lst:
         stripped_item=strip_rechtsform(item)
         new_list.append(stripped_item)
    return new_list
         
def filter_companies_with_rechtsform(lst):
    with_rechtsform=[]
    without_rechtsform=[]
    for entry in lst:
        rechtsform=return_rechtsform(entry)
        if rechtsform!=None:
            with_rechtsform.append(entry)
        else:
            without_rechtsform.append(entry)
    return with_rechtsform,without_rechtsform

def remove_haftungsbeschränkt(names):
    new_names=[]
    names=list(names)
    for name in names:
        name=name.strip()
        name=name.rstrip(" (haftungsbeschränkt)")
        new_names.append(name)
    return new_names
     
