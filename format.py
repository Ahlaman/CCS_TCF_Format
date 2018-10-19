#!/usr/bin/env python3
# coding=utf-8
import re
import sys
import getopt


def main(argv):
    inputfile = ''
    outputfile = ''
    dic = {}
    try:
        opts, args = getopt.getopt(argv[1:], "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(argv[0] + '-i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('format.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    fileinput = open(inputfile, 'r')
    fileoutput = open(outputfile, 'w+')
    for inputline in fileinput:
        res = re.search(r'(.*)\s=\s(.*);', inputline)
        if res is not None:
            res_tmp1 = res.group(1)
            res_tmp2 = res.group(2)
            res2 = re.split(r'\.', res_tmp1)
            ptmp = dic
            for res2line in res2:
                if res2line != res2[-1]:
                    if res2line not in ptmp:
                        ptmp[res2line] = {}
                    ptmp = ptmp[res2line]
                else:
                    ptmp[res2line] = res_tmp2
        res = re.search(r'(.*)\.(instance\(".*"\))\.destroy\(\);', inputline)
        if res is not None:
            res_tmp1 = res.group(1)
            res_tmp2 = res.group(2)
            res2 = re.split(r'\.', res_tmp1)
            ptmp = dic
            for res2line in res2:
                ptmp = ptmp[res2line]
            if res_tmp2 in ptmp.keys():
                del ptmp[res_tmp2]
            res3 = re.search(r'instance\((.*)\)', res_tmp2)
            if res3 is not None:
                res_tmp3 = res3.group(1)
                res_tmp3 = "create(" + res_tmp3 + ")"
                if res_tmp3 in ptmp.keys():
                    del ptmp[res_tmp3]
        res = re.search(r'(.*\.create\(".*"\));', inputline)
        if res is not None:
            res_tmp1 = res.group(1)
            res2 = re.split(r'\.', res_tmp1)
            ptmp = dic
            for res2line in res2:
                if res2line != res2[-1]:
                    if res2line not in ptmp:
                        ptmp[res2line] = {}
                    ptmp = ptmp[res2line]
                else:
                    ptmp[res2line] = ""
    list_all('', dic, fileoutput)


def list_all(output, dict_in, fileoutput):
    if isinstance(dict_in, dict):
        keys = dict_in.keys()
        for key in keys:
            output2 = output
            if output2 == '':
                output2 = str(key)
            else:
                output2 += "." + str(key)
            list_all(output2, dict_in[key], fileoutput)
    else:
        if dict_in == "":
            fileoutput.write(str(output) + ";\n")
        else:
            fileoutput.write(str(output) + " = " + str(dict_in) + ";\n")


main(sys.argv)
