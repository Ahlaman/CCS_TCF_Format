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
        res1 = re.search(r'(.*)\s=\s(.*);', inputline)
        if res1 is not None:
            res_tmp1 = res1.group(1)
            res_tmp2 = res1.group(2)
            res2 = re.split(r'\.', res_tmp1)
            ptmp = dic
            for res2line in res2:
                if res2line != res2[-1]:
                    if res2line not in ptmp:
                        ptmp[res2line] = {}
                    ptmp = ptmp[res2line]
                else:
                    ptmp[res2line] = res_tmp2
        res11 = re.search(r'(.*)(\.destroy\(\));', inputline)
        if res11 is not None:
            res_tmp11 = res11.group(1)
            res22 = re.split(r'\.', res_tmp11)
            ptmp = dic
            for res22line in res22:
                if res22line != res22[-1]:
                    if res22line not in ptmp:
                        print("error")
                        sys.exit()
                    ptmp = ptmp[res22line]
                else:
                    del ptmp[res22line]
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
        fileoutput.write(str(output) + " = " + str(dict_in) + "\n")


main(sys.argv)
