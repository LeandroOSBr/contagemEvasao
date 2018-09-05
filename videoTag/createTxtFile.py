import os

directory = '../Videos/segmentado/comprimido'

for filename in sorted(os.listdir(directory)):
        #print(filename)
        txtFilename = directory + "/" + (filename[0:len(filename)-4]) + ".txt"
        mode = 'a' if os.path.exists(txtFilename) else 'w'
        with open(txtFilename, mode) as f:
           print(txtFilename)