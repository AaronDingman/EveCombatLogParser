import os

n = 0
list = []
# C:\\Users\\xxx\\Documents\\TestInputDir
originalDir = 'C:\\Users\\xxx\\Documents\\TestInputDir'
# C:\\Users\\xxx\\Documents\\TestDirToDeleteFrom
targetDir = 'C:\\Users\\xxx\\Documents\\PyTesting - Copy\\'
for file in os.listdir(originalDir): # For each file in the directory 
    list = os.listdir(originalDir) # Sets the file names from the directory to a list
    if file in os.listdir(targetDir): # If the file is in the target file to be deleted
        os.remove(targetDir + list[n])  # Remove the file from the directory
        print(targetDir + list[n] + ': Deleted.')   # State which file was deleted
    n += 1  # Increment n to delete the next file
