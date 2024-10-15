import os
import getpass

username = getpass.getuser()
def root_search(directory):
      root_list=[]
      walk=os.walk(f"C:/Users/{username}/Desktop/bachelor")
      for root,dirs,files in walk:
            if root.endswith(directory):
                  root_list.append(root)
            if len(root_list)>1:
                  print("to many roots, returned the first one")
                  return root_list[0]
      return root_list[0]

def chdir_root_search(directory):
      root_dir=root_search(directory)
      os.chdir(root_dir)

def chdir_bachelor():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor")

def chdir_data():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor/data")

def chdir_id():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor/data/id")

def chdir_sql():
      if username == "lukas":
            os.chdir(r"E:\sql")
      if username=="Lukas":
            os.chdir(r"C:\sql")

def chdir_pdf():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor/pdf") 

def chdir_auth():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor/auth")    

def chdir_txt():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor/txt")    

def chdir_fig():
      os.chdir(f"C:/Users/{username}/Desktop/bachelor/data/figures")          

def switch_dir(type):
      if type =="pdf":
            chdir_pdf()
      if type == "json":
            chdir_data()


def chdir_search(directory):
      walk=os.walk(f"C:/Users/{username}/Desktop/bachelor")
      for root,dirs,files in walk:
            if root.endswith(directory):
                  print(root)
                  os.chdir(root)

