import os
import ipyparams

currentNotebook = ipyparams.notebook_name
cur_dir = os.getcwd()
def to_PDF(filename=currentNotebook):
    print("filename: {}".format(filename))
    os.system("jupyter-nbconvert --to PDFviaHTML {}".format(filename))