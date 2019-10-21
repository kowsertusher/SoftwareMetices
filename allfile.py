import os

path = '/home/tushar/Desktop/Mask_RCNN'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.py' in file:
            files.append(os.path.join(r, file))

allfile = ""
for f in files:
    print(f)
    singlefile = open(f,"r").read()
    allfile +="\n" +singlefile
#print(allfile)
