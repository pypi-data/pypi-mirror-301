import subprocess
import os
import pandas as pd

def rwrapper(script_path,arguments=None):
    if arguments==None:
        result=subprocess.run(["Rscript",script_path],capture_output=True,text=True)
    else:
        result=subprocess.run(["Rscript",script_path,arguments],capture_output=True,text=True)
    print(result.stdout)
    print(result.stderr)
    return result