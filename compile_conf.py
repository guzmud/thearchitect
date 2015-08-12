#! /usr/bin/python

# FOLDERS

pieces_folder = "pieces"
results_folder = "results"
schematics_folder = "schemas"

# ALIAS ALIAS

alias_file = str(pieces_folder)+"/aliases"

# TARGET SCHEMATIC

# schematic filename in schematics folder
# e.g. : schematic = "thekid", schematic = "pafish"
schematic = "guihello"

# PRETREATMENTS

# Existing pretreatments : junkinject, inpacking

# Warning : inpacking is using PACKx tags (PACK1, PACK2, etc.),
# avoid at all costusing them for other reasons when enabling this pretreatment

# add pretreatments according to function name in pretreatment.py
# e.g. : ["junkinject"] or ["junkinject","inpacking"]
pretreat = []

# COMPILER OPTIONS

# mingw and .lib
libs = ["wtsapi32", "psapi", "advapi32", "ws2_32", "gdiplus", "ole32"]
llibs = ' '+''.join(["-l"+str(i)+" " for i in libs])

incmd = str(results_folder)+"/"+str(schematic)+".c"
otcmd = str(results_folder)+"/"+str(schematic)+".exe"

# COMPILER CONSOLE COMMAND

cmd="i686-w64-mingw32-gcc ./"+str(incmd)+str(llibs)+"-s -Os -o ./"+str(otcmd)
