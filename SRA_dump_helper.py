#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 19:15:06 2017

@author: yolandatiao
"""

#####------------------ Import START ------------------#####
import os # For changing directory
import subprocess # For calling bash 
from astropy.io import ascii # For using ascii table to open csv
from Tkinter import Tk    # For opening file user interface
from tkFileDialog import askopenfilename    # For opening file user interface
import csv
import numpy as np
import seaborn as sns
#####------------------ Import END ------------------#####



#####------------------ Config START ------------------#####xw
code_directory=os.getcwd()
#####------------------ Config END ------------------#####



#####------------------ Self Defined functions START ------------------#####
os.chdir(code_directory)
import fc_basic_astropy_subprocess as fc

# A function to call bash commands
def run_sh(command):                                     
  process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  retcode = process.wait()
  if retcode != 0:
    raise Exception, "Problem running command: " + command
  stdout, stderr = process.communicate()
  return stdout

#####------------------ Self Defined functions END ------------------######


#####------------------ Main START ------------------######

###----- Open file
print 'Please find your input file: '
root = Tk()
root.withdraw()
root.update()
main_input_file = askopenfilename()
input_file_name = fc.Getfilename(main_input_file)
input_file_name_noformat = fc.filenamenoformat(input_file_name)
out_filename="%s.csv"% input_file_name_noformat

input_file_path_list=main_input_file.split("/")[:-1]
input_file_path=("/".join(input_file_path_list))
os.chdir(input_file_path)


###----- Find sra tool you need to use
print 'Please find your sra tool: '
#root = Tk()
#root.withdraw()
#root.update()
#sra_tool_directory = askopenfilename()
sra_tool_directory=raw_input()
print 'Please enter your output file type:'
file_type=raw_input()

###----- Read SraRunTable and transform into csv file
fout=open(out_filename,"wb")
foutwriter=csv.writer(fout,delimiter=",")
with open(main_input_file, "r") as f:
    readCSV=csv.reader(f, delimiter="\t")
    for row in readCSV:
        foutwriter.writerow(row)   
fout.close()

###----- Read csv SraRunTable and write bash file
sra_tab=ascii.read(out_filename)
sra_tab=fc.setcolnames(sra_tab)
sra_tab_colnames=sra_tab.colnames

#--- Select identifier column
for x in xrange(0, len(sra_tab_colnames)):
    print "%s\t%s\te.g.%s" %(x, sra_tab_colnames[x], sra_tab[0][x])
print "Which one you use to identify your samples: "
print "Please enter the number"
idt_colname_number=int(raw_input())
idt_colname=sra_tab_colnames[idt_colname_number]
print "\n"

#--- Find SRR column
for x in xrange(0, len(sra_tab_colnames)):
    print "%s\t%s\te.g.%s" %(x, sra_tab_colnames[x], sra_tab[0][x])
print "Which one you want to extract: "
print "Please enter the number"
srr_colname_number=int(raw_input())
srr_colname=sra_tab_colnames[srr_colname_number]
print "\n"


#--- Select sample according to identifier
idt_list=list(set(list(sra_tab[idt_colname])))
for x in xrange(0, len(idt_list)):
    print "%s\t%s"%(x, idt_list[x])
print "Please pick the numbers of samples: (seperated by comma)"
idt_pick_numbers=raw_input()
idt_pick_numbers_list=idt_pick_numbers.split(",")
print idt_pick_numbers_list
print '\n'

idt_pick_list=[]
for x in xrange(0,len(idt_pick_numbers_list)):
    idt_pick_list.append(idt_list[int(idt_pick_numbers_list[x])])

print "You picked:"
print (", ".join(idt_pick_list))

#--- Find rows and write into bash commands
fout=open("%s.sh"%input_file_name_noformat,"wb")
fout.writelines("#!/bin/bash")
fout.writelines("\n")
for x in xrange(0, len(sra_tab)):
    if sra_tab[idt_colname][x] in idt_pick_list:
        idt_x=sra_tab[idt_colname][x]
        srr_x=sra_tab[srr_colname][x]
        output_name='%s_%s.%s'%(idt_x,srr_x,file_type)
        #output_name_path="%s%s"%(input_file_path,output_name)
        cmd='%s %s > %s'%(sra_tool_directory, srr_x,output_name)
        fout.writelines(cmd)
        fout.writelines("\n")
fout.close()
#####------------------ Main END ------------------######








