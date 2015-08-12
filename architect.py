#! /usr/bin/python

# IMPORT CONF
import compile_conf as cconf

# IMPORT HOMEBREW LIBRARY
import pretreatment

# IMPORT STANDARD LIBRARIES
import subprocess, shlex, importlib

# VARIABLES

alias_dict = {}
include = ["<stdio.h>","<windows.h>"]
var = []

# FONCTIONS

def pretreating(plist):
    ptlist = cconf.pretreat
    for i in ptlist:
        plist = getattr(pretreatment, i)(plist)
    return plist

def load_aliases():

    tdict = {}
    fdata = open(cconf.alias_file)
    data = fdata.read()
    fdata.close()

    for i in filter(None, data.split("#DEF")):
        tdict[filter(None,i.split("#ALIAS"))[0].strip().split("[")[0]] = [
            filter(None,no_comments(filter(None,i.split("#ALIAS"))[0].split("\n")))[0].strip(),
            filter(None,no_comments(filter(None,i.split("#ALIAS"))[1].split("\n")))]
        
    return tdict

def read_schematic(schemaname):
    fdata = open(cconf.schematics_folder+'/'+cconf.schematic+'.schematic','r')
    data = fdata.read()
    fdata.close()
    return data

def get_order(ivdict,ovdict):
    k = 1

    for i in ivdict:
        if ((type(ivdict[i]) is list) and (len(ivdict[i])>k)):
            k = len(ivdict[i])

    for o in ovdict:
        if ((type(ovdict[o]) is list) and (len(ovdict[o])>k)):
            k = len(ovdict[o])
            
    return k

def special_replace(strarg):
    strarg = strarg.replace("\\\"",r'\x34')
    strarg = strarg.replace("\\{",r'\x123')
    strarg = strarg.replace("\\}",r'\x125')
    strarg = strarg.replace("\\(",r'\x40')
    strarg = strarg.replace("\\)",r'\x41')
    return strarg

def format_string(strarg):

    if strarg.count('"') > 0:
        if strarg.count('"') % 2 == 0:
            for i in range(strarg.count('"')):
                if i % 2 == 0:
                    old = strarg.split('\"')[(i+1)].split('\"')[0]
                    new = strarg.split('\"')[(i+1)].split('\"')[0].replace(',', r'\x2c').replace('(', r'\x40').replace(')', r'\x41').replace('{', r'\x123').replace('}', r'\x125')
                    if old != new :
                        strarg = strarg.replace(old,new)
        else:
            print "You are probably missing a \" in "+strarg
    return strarg

def format_injection(strarg):

    if ((strarg.count('(') > 0) and (strarg.count(')') > 0)):
        if (strarg.count('(') == strarg.count(')')):
            for i in range(strarg.count('(')):
                #if i % 2 == 0:
                    old = strarg.split('(')[(i+1)].split(')')[-2]
                    new = strarg.split('(')[(i+1)].split(')')[-2].replace(',', r'\x2c')
                    if old != new :
                        strarg = strarg.replace(old,new)
        else:
            print "You are probably missing a ( or a ) in "+strarg
    return strarg

def format_list(strarg):

    if ((strarg.count('{') > 0) and (strarg.count('}') > 0)):
        if (strarg.count('{') == strarg.count('}')):
            for i in range(strarg.count('{')):
                if i % 2 == 0:
                    old = strarg.split('{')[(i+1)].split('}')[-2]
                    new = strarg.split('{')[(i+1)].split('}')[-2].replace(',', r'\x2c').replace('(', r'\x40').replace(')', r'\x41')
                    if old != new :
                        strarg = strarg.replace(old,new)
        else:
            print "You are probably missing a { or a } in "+strarg
    return strarg

def format_args(strarg):
    strarg = special_replace(strarg)

    # switching reserved chars inside string to avoid parser confusing
    strarg = format_string(strarg)

    # switching reserved chars inside instruction injections to avoid parser confusing
    strarg = format_injection(strarg)

    # switching reserved chars inside lists to avoid parser confusing
    strarg = format_list(strarg)

    # spliting along ',' outside of strings and lists
    strarg = filter(None,map(str.strip,strarg.split(",")))

    # switching back reserved chars
    for i in range(len(strarg)):
        strarg[i] = strarg[i].replace(r'\x40', '(').replace(r'\x41', ')').replace(r'\x123', '{').replace(r'\x125', '}').replace(r'\x91', '[').replace(r'\x93', ']').replace(r'\x2c', ',').replace(r'\x34', '\x5c"')

    # recursive process for listed arguments
    for i in range(len(strarg)):
        if ((strarg[i][0] == '{') and (strarg[i][-1] == '}')):
            strarg[i] = format_args(strarg[i][1:-1])

    # recursive process for injected instructions
    for i in range(len(strarg)):
        if ((strarg[i][0] == '(') and (strarg[i][-1] == ')')):
            strarg[i] = code_factory(pparts_process(no_comments([strarg[i][1:-1],])))

    return strarg

def code_engine(plist):

    inst = str(plist[0]).replace('.','_')
    argi = format_args(str(plist[1]))
    argo = format_args(str(plist[2]))

    ivdict = {}
    ovdict = {}
    
    # finding and loading the piece

    tf = open(str(cconf.pieces_folder)+"/"+str(inst)+'.piece','r')
    temp = tf.read()
    tf.close()

    # parsing the piece

    invar = temp.split("#INVAR")[1].split("#OTVAR")[0]
    invar = filter(None,map(str.strip,invar.replace("\n","").replace(" ","").strip().split(",")))
    
    otvar = temp.split("#OTVAR")[1].split("#INCLUDES")[0]
    otvar = filter(None,map(str.strip,otvar.replace("\n","").replace(" ","").split(",")))
    
    tinclude = temp.split("#INCLUDES")[1].split("#VARS")[0]
    tinclude = filter(None,tinclude.replace("\n","").replace(" ","").split(","))
    
    tvar = temp.split("#VARS")[1].split("#HEADER")[0]
    tvar = filter(None,tvar.replace("\n","").split(","))
    
    cheader = temp.split("#HEADER")[1].split("#MAIN")[0]
    cmain = temp.split("#MAIN")[1].split("#FOOTER")[0]
    cfooter = temp.split("#FOOTER")[1]

    # building the i/o dictionnaries
    
    if (len(argi) != len(invar)):
        print inst
        print "ERREUR : input argument error (inequality)"
    else:
        for i in range(len(invar)):
            ivdict[invar[i]] = argi[i]
    
    if (len(argo) != len(otvar)):
        print inst
        print "ERREUR : output argument error (inequality)"
    else:
        for i in range(len(otvar)):
            ovdict[otvar[i]] = argo[i]

    # injecting i/o args inside the code

    tcode = ""
    
    k = get_order(ivdict,ovdict)

    for o in ovdict:
        if type(ovdict[o]) is list:
            temp = ovdict[o][0]
        else:
            temp = ovdict[o]
        cheader = cheader.replace(o,temp)
        cfooter = cfooter.replace(o,temp)
        tvar = [v.replace(o,temp) for v in tvar]

    for i in ivdict:
        if type(ivdict[i]) is list:
            temp = ivdict[i][0]
        else:
            temp = ivdict[i]
        cheader = cheader.replace(i,temp)
        cfooter = cfooter.replace(i,temp)
        tvar = [v.replace(i,temp) for v in tvar]

    tcode += cheader

    for z in range(k):
        tcmain = cmain
        for i in ivdict:
            if type(ivdict[i]) is list:
                tcmain = tcmain.replace(i,ivdict[i][z%len(ivdict[i])])
            else:
                tcmain = tcmain.replace(i,ivdict[i])
        for o in ovdict:
            if type(ovdict[o]) is list:
                tcmain = tcmain.replace(o,ovdict[o][z%len(ovdict[o])])
            else:
                tcmain = tcmain.replace(o,ovdict[o])
        tcode += tcmain

    tcode += cfooter

    return tcode,tinclude,tvar

def code_factory(plist):

    global include, var

    code = ""

    tk = len(plist)
    i = 0

    # replacing aliases
    while i<tk:
        if plist[i][0] in alias_dict.keys():
            at_list = []
            at_list = pparts_process(alias_dict[plist[i][0]][1])
            # HERE BE DRAGONS !
            for j in range(len(at_list)):
                iarglist = format_list(format_injection(format_string(special_replace(str(plist[i][1])))))
                iarglist = iarglist.split(",")
                for k in range(len(iarglist)):
                    at_list[j] = [at_list[j][0], at_list[j][1].replace("IVAR"+str(k+1),iarglist[k]), at_list[j][2]]

                oarglist = format_list(format_injection(format_string(special_replace(str(plist[i][2])))))
                oarglist = oarglist.split(",")
                for q in range(len(oarglist)):
                    at_list[j] = [at_list[j][0], at_list[j][1], at_list[j][2].replace("OVAR"+str(q+1),oarglist[q])]

                at_list[j] = at_list[j]
            plist[i:i+1] = at_list
            tk += len(at_list)-1
        i += 1

    for i in plist:
        temp = code_engine(i)
        code += temp[0]
        include += temp[1]
        var += temp[2]

    return code

def assemble_code(plist):

    global include, var

    hcode = "main()\n{\n"
    code = '\n'+hcode+code_factory(plist)
    
    # add the vars to the code
    var = list(set(var))
    for v in var:
        if v.strip() != "":
            code = str(v.strip())+';\n'+code
    code = '\n'+code

    # add the includes to the code
    include = list(set(include))

    # re-arrange the main includes for interdependance issues
    if '<windows.h>' in include:
        include.remove('<windows.h>')
        include += ['<windows.h>']
    if '<winsock2.h>' in include:
        include.remove('<winsock2.h>')
        include += ['<winsock2.h>']
    if '<stdio.h>' in include:
        include.remove('<stdio.h>')
        include += ['<stdio.h>']

    for i in include:
        if i.strip() != "":
            code = '#include'+str(i.strip())+'\n'+code
    code += '}'

    # limit abusive linebreaks and forcing windows-compatibility
    code = code.replace('\r\n','\n')
    code = code.replace('\n','\r\n')
    while '\r\n\r\n\r\n' in code:
        code = code.replace('\r\n\r\n\r\n','\r\n\r\n')

    return code

def sparts_process(sparts):
    sdict = {}
    for part in sparts:
        sdict[part.split('[')[0]] = part.split('[')[1].split(']')[0]
    return sdict

def no_comments(t_parts):

    return [i for i in t_parts if i[0:2] != "##"]

def pparts_process(pparts):

    plist = []
    for part in pparts:

    # switching reserved chars inside instruction injections to avoid parser confusing
        part = part.replace("\\(",r'\x40').replace("\\)",r'\x41')
        if ((part.count('(') > 0) and (part.count(')') > 0)):
            if (part.count('(') == part.count(')')):
                for i in range(part.count('(')):
                    #if i % 2 == 0:
                        old = part.split('(')[(i+1)].split(')')[-2]
                        new = part.split('(')[(i+1)].split(')')[-2].replace('[', r'\x91').replace(']', r'\x93')
                        if old != new :
                            part = part.replace(old,new)
            else:
                print "You are probably missing a ( or a ) in "+strarg

        part = part.replace("\\[",r'\x91')
        part = part.replace("\\]",r'\x93')
        plist += [[part.split('[')[0], part.split('[')[1].split(']')[0],part.split('[')[2].split(']')[0]],]
    return plist

def preprocess_schematic(schmdata):
    sample_parts = filter(None,map(str.strip,schmdata.split("#SAMPLE")[1].split("#PIECES")[0].split("\n")))
    pieces_parts =filter(None,map(str.strip,schmdata.split("#PIECES")[1].split("\n")))

    sdict = sparts_process(no_comments(sample_parts))
    plist = pparts_process(no_comments(pieces_parts))

    return sdict, plist

def import_routines(plist):

    recent = True

    while recent:
        recent = False
        for i in range(len(plist)):
            if plist[i][0].split(".")[0] == "routine":
                recent = True
                tf = open(str(cconf.schematics_folder)+"/"+str(plist[i][0].split(".")[1])+'.schematic','r')
                temp = tf.read()
                tf.close()
                plist[i:i+1] = preprocess_schematic(temp)[1]
    return plist	

# MAIN

print "THE ARCHITECT"
print "\tReading and processing the main schematic"
data = read_schematic(cconf.schematic)

sdict, plist = preprocess_schematic(data)

print "\tCompiling "+str(sdict["name"])+", version "+str(sdict["version"])

print "\tImporting routines ..."
plist = import_routines(plist)

print "\tLoading aliases dictionnary ..."
alias_dict = load_aliases()

print "\tPre-treatment of the schematics ..."
plist = pretreating(plist)

print "\tRefactoring the code ..."
code = assemble_code(plist)

print "\tWriting down the file ..."
mf = open(cconf.incmd,'w')
mf.write(code)
mf.close()

print "\tCompiling and linking the file ..."
subprocess.call(shlex.split(cconf.cmd))

print "Quite right. Interesting. That was quicker than the others."
