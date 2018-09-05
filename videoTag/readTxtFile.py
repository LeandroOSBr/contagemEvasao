import os
import ast

directory = '../Videos/segmentado/comprimido'
a = []

for filename in sorted(os.listdir(directory)):
    if filename.endswith(".txt"):
        fileN = directory + "/" + filename
        with open(fileN) as fp:
            content = fp.readline()
            #Formata para Dicionario
            content = content.replace(":","' : ")
            content = content.replace(";",", '")
            content = "{'" + content + "}"
            content = ast.literal_eval(content)
            print(content)
            #print(content["SimPula"])
            #print(content["SimPassaPorBaixo"])
            a.append(content)
print("SimPula: ",sum(item['SimPula'] for item in a))
print("NaoPula: ",sum(item['NaoPula'] for item in a))
print("SimPassaPorBaixo: ",sum(item['SimPassaPorBaixo'] for item in a))
print("NaoPassaPorBaixo: ",sum(item['NaoPassaPorBaixo'] for item in a))
    #print(filename)
    #txtFilename = directory + "/" + (filename[0:len(filename)-4]) + ".txt"

#with open(fname) as f:
#    content = f.readlines()
## you may also want to remove whitespace characters like `\n` at the end of each line
#content = [x.strip() for x in content] 