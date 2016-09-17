#! /usr/bin/python

import binascii

XORVAL = 42  # change to the wanted value, impact the schematic according to


def data_from_file(ifile):
    with open(ifile, "rb") as f:
        data = f.read()
    return data


def data_to_file(ofile, data):
    with open(ofile, "wb") as f:
        f.write(data)
        f.close()

# if one's want to xor the content of a file
filename = "/mhello.exe"
filepath = "../results"+filename
data = data_from_file(filepath)

# if one's want to xor a string instead of a file
# data = "the choice"

xdata = ""
for i in data:
    xdata += chr(ord(i) ^ XORVAL)

data_to_file(str(filename).split(".")[0]+".xored", binascii.hexlify(xdata))
