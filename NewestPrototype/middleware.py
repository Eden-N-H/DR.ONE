import os

def pathToText():
    # Get the directory path of the current file
    savePath = os.path.dirname(os.path.abspath(__file__))
    # Create the subdirectory path
    subdir = "path_text_files"
    savePath = os.path.join(savePath, subdir)
    
    # Create the subdirectory if it doesn't exist
    if not os.path.exists(savePath):
        os.makedirs(savePath)

    fileName = "path"
    completeName = os.path.join(savePath, fileName+".txt")
    f = open(completeName, "a")
    # Do something eg. write into text file 'f'

    # # Testing if something gets written into the file.
    # Write a string into the file
    f.write("This is a test string.")
    
    # Close the file
    f.close()