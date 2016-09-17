The Architect
=============

The Architect is **a code factory** intended to provide **non-offensive pseudo-malwares**. The main use is to test introspection-style the correct behaviour of analysis system while also having the opportunity to proactively stress test it and pinpoint particular functionalities and weakness.

The use of an intermediary language allows less-technical researchers and enthusiasts access to designed samples they can trust. The aim is to provide a tool easier to manage than creating new samples while having an imitation of malware with their full potential. Bonus, the tool is created with an adaptive and evolving mindset, allowing users to easily integrate new pieces, routines and treatments.

The Architect : a factory
-------------------------

The main component is the factory, the Architect in itself, that assemble *pieces* of code according to a *schematic* in order to craft an *executable*. The Architect is in *Python* while the pieces are in *C* and the schematics are in a *homebrew language*.

Language basics : instructions and schematics
---------------------------------------------

The homebrew language is basically a way to arrange the various pieces in C, in a consecutive execution manner, with some twists.

The *pieces* of C represent various instructions, ranging from low to high level. They are named according to the following convention : *type*.*name* (e.g. : *if.equaval*, *netcom.localip*, *reg.open*, *sysvar.getwinversion*).

The *schematics*, excluding the header part (the format being pretty much self-explanatory), follow these conventions :
- *category.function[input args][output args]* is the instruction format
- if there is no args, you still have to put the []
- one instruction per line
- arguments can be *raw*, "*string*", {*embedded instruction*}, (*list of arguments*)
- arguments can be reused between instructions

**One should beware of too common argument names that may already been use inside the pieces !** Which mean that yes, you can reuse arguments from inside pieces that were not explicitly named inside the schematics.

Language specificities
----------------------

**Aliases** : an aliases file exists, allowing one instruction in place of many. Basically the aliases file is your library full of functions. Input and output arguments are allowed. e.g. : *if.username[IVAR1,IVAR2,IVAR3][]* instead of *sysvar.getusername[][userstr] if.strdelta[userstr,IVAR1,IVAR2,IVAR3][]*.

**Routines** : using the keyword routine as an instruction category allows you to inject a full schematic as an instruction. No input or output arguments ([] still needed). e.g. : *routine.melting[][]* to inject the instructions of the *melting.schematic*

Factory specificities
---------------------

**Pretreatments** : as of now two pretreatments are available. Pretreatments are optional data manipulation functions (coded in the *pretreatment.py* file and configured with both this file and the *compile_conf.py*). **junkinject** automatically add junk code inside the schematic (*junkratio* and *junklist* as the configuration elements). **inpacking** replace special tags (*PACK*) with content (like a particular string or file content, manageable through *pretreatment.py* and its variables *inpacklist* and *filetupac*).

**Tools** : **xorarray** allows you to easily xOR the content of a string or a file (in order to copy it inside a schematic or inject it using the *inpacking* pretreatment). **docgen** generate the homebrew language documentation according to the content of the pieces and aliases. Yep, documentation generator included, the least for a homebrew language every user can tune.

Available schematics
--------------------

As of now, various schematics are available as examples. Including :
- Pafish, an imitation (*in-the-spirit*) of the famous paranoid fish
- TheKid, that will download a new wallpaper
- Anderson, that will test inputs/outputs and basic behaviours
- Neo, environment awareness, nebett shuttle, decoy and real payloads
- Smith, that will test self-replication
- Melting, the self-deletion routine

Installation and configuration
------------------------------

Made using **Python 2.7**, should be easily converted to Python 3 if necessary. Runs with Python standard library, no external library needed.

Mainly configured through **compile_conf.py**, including the folder names, the pretreatment options, and, more importantly, the **schematic to be loaded** and the **command line for the C compiler** (and its options). For the moment, the command line is made for a *gcc mingw32 64 bits* situation.

The **pretreatment.py** allows the user to make fine tuning to the various pretreatment options (including *junklist*, the pool of junk, *junkratio*, the ratio of junk; *filetupac*, *inpacklist*, *inpacktag* for the inpacking pretreatment).

Please enjoy the flexibility of the system to create new pieces, new aliases, new routines, new pretreatments, re-adapt the folder structures.

Anticipated FAQ
---------------

*todo*

Todo list
---------------------------

- *Anticipated FAQ*
- *A real todo list*

Thanks to
---------

- a0rtega, for its paranoid fish and associated works
- w4kfu, for its work on shuttle and other works
- the people documenting hidden bits and pieces of Windows
- stackoverflow and various sources (cited inside the pieces, sometimes)