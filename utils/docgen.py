#! /usr/bin/python
# DOCUMENTATION GENERATOR, BASED ON PIECES TEXT HEADER

# TODO
# add as an intro a file containing basic coding rules and reserved keywords
# including an explaination of the "modulo system" for the list args

# IMPORT STANDARD LIBRARIES

import glob, os.path

# VARIABLES

pieces_folder = '../pieces'
docfile = "architect_doc.txt" # name of the generated file
taglist = ["Todo : ","Stolen from : ","In vars : ","Out vars : "] # tags inside piece text header
ddict = {}
aliases_on = False
alias_path = str(pieces_folder)+'/aliases'

# FUNCTIONS

def key2doc(k, kdict):

    data = ""
    data += "# "+str(k).upper()+"\n\n"

    if "main" in kdict[k]:
        data += str(kdict[k]["main"])+"\n\n"

    for t in taglist:
         if t in kdict[k]:
             data += "\t"+str(t)+str(kdict[k][t])+"\n"
    return data

# MAIN

print "DOCUMENTATION GENERATION\n"

# listing the pieces
print "\tLooking for .pieces in folder \""+str(pieces_folder)+"\" ..."
plist = glob.glob(str(pieces_folder)+'/*.piece')
print "\tFound "+str(len(plist))+" different pieces ..."

# getting the data for each file (the DOC part of the piece header)
print "\tReading the files ..."
for p in plist:
    with open(p, "rb") as f:
        tdata = f.read()
    ddict[p.split("/")[-1].replace(".piece",'')] = tdata.split("#")[1].split("DOC")[1].strip()

# formatting the data
print "\tFormating the information ..."
for d in ddict:
    tdict = {}
    temp = ddict[d]
    
    for t in taglist[::-1]:
        if t in temp:
            tdict[t] = temp.split(t)[-1].strip()
            temp = temp.split(t)[0]
    tdict["main"] = temp.strip()
    ddict[d] = tdict

ddata = ""
section = ""
stable = {}
llist = []
tdata = ""

print "\tBuilding the docfile ..."
for d in sorted(ddict.keys()):
    if len(d.split("_")) == 1:
        llist += [d]
    else :
        if d.split("_")[0] != section:
            section = d.split("_")[0]
            stable[section] = 0
            tdata += "\n#### "+str(section).upper()+"\n\n"
        stable[section] += 1
        tdata += str(key2doc(d, ddict))+"\n"
ddata += tdata

if len(llist) > 0 :
    tdata = "\n#### COMMON\n\n"
    stable["common"] = 0
    for l in llist:
        stable["common"] += 1
        tdata += str(key2doc(l, ddict))+"\n"
    ddata = tdata+ddata

# detecting the exitence of aliases and adding them
if os.path.isfile(alias_path):
    aliases_on = True
    print "\tAliases found at \""+alias_path
else:
    print "\tNo \"aliases\" file found at "+alias_path+" !"

if aliases_on:
    print "\tAdding a list of enabled aliases ..."
    with open(alias_path, "rb") as f:
        adata = f.read()
    tdata = "\n#### ALIASES\n\n"
    for i in filter(None,[i.split("#ALIAS")[0].strip() for i in adata.split("#DEF")]):
        tdata += str(i.split("[")[0]+"\n")
    ddata = ddata+tdata

# if aliases found and loaded, add them to the section table bro ! (outside sorted keys)

# building the section table according to the various pieces type
if len(stable)>0:
    tdata = "#### SECTIONS TABLE ####\n"
    for t in sorted(stable.keys()):
        tdata += "\t"+str(t).upper()+" ("+str(stable[t])+")\n"
    if aliases_on:
        tdata += "\tALIASES\n"
    tdata += "########################\n\n"
    ddata = tdata + ddata

# adding the title
ddata = "THE ARCHITECT DOCUMENTATION : PIECES\n\n"+ddata

# writing down the file
print "\tWriting down the docfile in \""+str(docfile)+"\" ..."
mf = open(docfile,'w')
mf.write(ddata)
mf.close()
