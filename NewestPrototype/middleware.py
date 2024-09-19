import os

def pathToText():
    #you must replace the savePath with the directory of the path_text_files folder within your local directory
    # (right click -> copy path/reference -> paste below
    savePath = "/Users/edenhallett/Documents/UTS/Application Studio A/Pathfind/NewestPrototype/path_text_files"
    fileName = "path"
    completeName = os.path.join(savePath, fileName+".txt")
    f = open(completeName, "a")
    # Do something eg. write into text file 'f'




