#! /usr/bin/python

import random

# PRETREATMENT : JUNKINJECT

junklist = [['junk.maths', '', ''],
            ['junk.filecheck', '', ''],
            ['junk.regcheck', '', '']]  # [piece name, input,output]
junkratio = 0.3


def junkinject(plist):
    jk = int(junkratio*len(plist)) + 1
    jk += (random.randint(-1, 1))*(random.randint(0, int(len(plist)/5)))

    if jk > len(plist):  # not too much junk
        jk = len(plist)-1

    if jk < 1:  # neither not enough
        jk = 1

    for i in range(jk):
        plist.insert(random.randint(0, len(plist)-1), random.choice(junklist))

    return plist

# PRETREATMENT : INPACKING

filetupac = []
# e.g. : filetupac = [[0, "utils/mhello.xored"], [1, "utils/smith.xored"]]

inpacklist = []
inpacktag = str("PACK")


def packfromfile(pos, filename):
    global inpacklist
    with open(filename, "rb") as f:
        data = f.read()
        inpacklist.insert(pos, str(data))


def inpacking(plist):

    for l in filetupac:
        packfromfile(l[0], l[1])

    for i in range(len(inpacklist)):
        for k in range(len(plist)):
            for q in range(len(plist[k])):
                if inpacktag+str(i+1) in plist[k][q]:
                    plist[k][q] = plist[k][q].replace(inpacktag+str(i+1),
                                                      '"'+inpacklist[i]+'"')
    return plist
