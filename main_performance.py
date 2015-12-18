####################################################
#                  Revision: 2.0                   #
#              Updated on: 12/18/2015              #
#                                                  #
# What's new:                                      #
#                                                  #
#           Support for SSD Peformance files       #
#                                                  #
#                                                  #
# Additional files:                                #
#                                                  #
#           1.) performance_ssd_functions.py       #
#           2.) generate_table_plots_ssd.py        #
####################################################

####################################################
#                  Revision: 1.0                   #
#              Updated on: 11/06/2015              #
####################################################


''' 
    This file generates Modified .csv file,
    Average IOps plot, and Sequential MBps
    for all drives. Then it replaces KEYWORDS
    in template provided my User. Finally, it
    appends generated 3 files to the template
    and removes/deletes those files.
    
    For more information: "Read me.txt"
    
    Author: Zankar Sanghavi                        
    
    © Dot Hill Systems Corporation '''


###################################################
#
#   Importing required packages
# 
###################################################
import time
start_time = time.time()

import os
import sys


###################################
#  Importing from other Directory
###################################
os.chdir('..')
c_path = os.getcwd()
sys.path.insert(0, r''+str(c_path)+'/Common Scripts')

import report_functions
import extract_lists
import modify_word_docx
import fixed_data
import user_inputs


###################################
#  Importing from Current Directory
###################################
sys.path.insert(0, r''+str(c_path)+'/Performance_HDD_SSD')
import csv
import numpy as np
import matplotlib.pyplot as plt
import time

import generate_table_plots
import append_files

import generate_table_plots_ssd
import performance_ssd_functions


##########################################
#
#   Empty lists to store Inputs from User 
#
###########################################
no_files_concatenate=0
file_names=[] 
cap_names=[]
model_no_names=[]
chassis_names=[]
cntrllr_names=[]
fw_no_names=[]
vendor_names=[]
eco_names=[]
fw_type_names=[]
product_fnames=[]
ind_same_fname=[] 


#######################################
#
#   Input file names from User 
#
#######################################
ui = user_inputs.User_Inputs
fd= fixed_data.Fixed_Data
el= extract_lists.Extract_Lists
af= append_files
psf = performance_ssd_functions.Peformance_SSD_Functions


##########################################
#
#   Prompts for HP drives or BB/SSD 
#   drives selection
#
##########################################
HP_dec=ui.hp_question()


##########################################
#
#   Prompts for Qualification or Regression 
#   selection
#
##########################################
fw_type=ui.fw_type()


###################################
#  To make sure, User inputs enters  
#  a numeric character for Number of 
#  files to concatenate.
###################################
no_of_files='abc' #dummy string
while not no_of_files.isnumeric():
    no_of_files= input('\nPlease enter number of files to concatenate: ')
    no_of_files.isnumeric()
no_of_files=int(no_of_files)


######################################
#  This loop will collect all inputs
#  from User, for specified number of 
#  files. And store it in List, which 
#  is used to process later. 
######################################
for i in range(no_of_files):
    ##########################################
    #
    #   Prompts for Original .csv file 
    #
    ##########################################
    original_file_path=ui.org_path(i+1)
    original_file_path=str(original_file_path).replace('"','')
    
    
    ##########################################
    #
    #   Stores multiple Original .csv files 
    #
    ##########################################
    file_names.append(original_file_path) 
    
    
    ##############################################
    #
    #   1.)Prompts to Enter Model Number till it  
    #   is from "Supported_drives.xlsx" file. 
    #
    #   2.)Extracts Capacity, Vendor, Firmware, ECO 
    #   number, and Product family name of User 
    #   entered Model number. 
    #
    ##############################################
    [temp_model,
    temp_capacity,
    temp_fw,
    temp_vendor,
    temp_eco,
    temp_product_name] = ui.hdd_model(HP_dec) #model number
    
    
    ##########################################
    #
    #   Stores multiple Model Number, Capacity,
    #   Firmware, Product Family Name, Vendor
    #   name, ECO numbers for Multipe Files.
    #
    ##########################################
    model_no_names.append(temp_model)
    cap_names.append(temp_capacity)
    fw_no_names.append(temp_fw) 
    product_fnames.append(temp_product_name)
    vendor_names.append(temp_vendor)
    eco_names.append(temp_eco)    
    
    
    ############################################
    #
    #   Prompts to enter Chassis number till it
    #   is from a pre-defined list. And store 
    #   it in a list for multiple files. 
    #
    ############################################
    chassis_i =ui.chassis_in(i)
    chassis_names.append(fd.chassis_list_d[int(chassis_i)])

    ##############################################
    #
    #   Prompts to enter Controller number till it
    #   is from a pre-defined list. And store 
    #   it in a list for multiple files. 
    #
    ##############################################
    cntrller_i =ui.cntrller_in(i)
    cntrllr_names.append(fd.cntrllr_list_d[int(cntrller_i)])
    
##########################################
#
#   Prompts for Word Template Path 
#
##########################################
word_file =ui.word_in()


###################################################
#
#   After taking all User inputs it starts 
#   processing in following steps:
#   
#   1.) Generate Modified .csv files
#       and Generate 2 Plots
#   2.) Modify contents of Word template
#   3.) Append Modified .csv files to Modified
#       word template. 
#   
###################################################


##############################
# Check if File name contains
# SSD string 
##############################
# Possible combination of SSD:
ssd_name_list = ['ssd', 'Ssd', 'sSd', 'ssD', 'SSd', 'SsD', 'sSD', 'SSD']

# ssd detection of all file
ssd_detection_all = psf.detect_ssd(no_of_files, file_names, ssd_name_list)

###################################################
#
#   1.) Generate Modified .csv files and 2 Plots
#   for Multiple files(i.e. User defined times)
#      
###################################################
if len(ssd_detection_all) == no_of_files:
    for i in range(no_of_files):
        if ssd_detection_all[i] == 0:
            
            generate_table_plots.Generate_Table_Plots(file_names[i])
        
        elif ssd_detection_all[i] == 1:
            
            generate_table_plots_ssd.Generate_Table_Plots_SSD(file_names[i])
            
        else:
            print("\nError in SSD dectection")
else:
    print("\nLength of SSD Detection Matrix and No. of Files not same!")
    
    

 
    
###################################################
#
#   This File extracts lists of Vendors, OEM       
#   models,Vendor Internal Names, Vendor Family    
#   names, Capacities, Next FW revs, and Release   
#   ECOs from "Supported_drive.xlsx" located       
#   in Local directory.
# 
###################################################
[model_list, capacity_list, vendor_list, fw_list, eco_list,
 product_fname_list,model_list_HP, capacity_list_HP, vendor_list_HP, 
 fw_list_HP, eco_list_HP, product_fname_list_HP]=  el.get_data()

 
###################################################
#
#   Finding Index of Model & FW no. with same
#   Vendor Family name.
# 
###################################################
if HP_dec=='N': #For BB/SSD drives
    for i in range(len( product_fname_list)):     
        if  product_fname_list[i]== (product_fnames[0]):
            temp=i
            ind_same_fname.append(temp)
  
    model_alist=np.array( model_list)
    model_alist=model_alist[ind_same_fname]
    model_alist.tolist()
    
    fw_alist=np.array( fw_list)
    fw_alist=fw_alist[ind_same_fname]
    fw_alist.tolist()
    
    new_list=''
    for i in range(len(model_alist)):
        new_list += model_alist[i] 
        new_list += '-'
        new_list += fw_alist[i]
        new_list += ' '
    #print(new_list)

elif HP_dec=='Y': # For HP drives
    for i in range(len( product_fname_list_HP)): 
        if  product_fname_list_HP[i] == str(product_fnames[0]):
            temp=i
            ind_same_fname.append(temp)

    model_alist=np.array( model_list_HP)
    model_alist=model_alist[ind_same_fname]
    model_alist.tolist()
    
    fw_alist=np.array( fw_list_HP)
    fw_alist=fw_alist[ind_same_fname]
    fw_alist.tolist()
    
    new_list=''
    for i in range(len(model_alist)):
        new_list += model_alist[i] 
        new_list += '-'
        new_list += fw_alist[i]
        new_list += ' '

        
###################################################
#
#   This Dictionary will change KEYWORDS in Word 
#   Template.
# 
###################################################
if fd.fw_type_d[fw_type]=='Qualification':
    temp_fw_type='Initial release of'
else:
    temp_fw_type='Firmware regression for'


###################################################
#
#   FIND TODAY'S DATE & Directory of Word Template
# 
###################################################
date=time.strftime("%m/%d/%Y") 

fixed_dir=os.path.dirname(r''+str(word_file))
word_file=str(word_file).replace('"','')


###################################################
#
#   Find Part number, Revision number from the name
#   of Word Template to change Footer and Revision 
#   number in Final Report. 
# 
###################################################
file_name = word_file[-(len(word_file)-len(fixed_dir)-1):]
part_no=file_name[:19] # Part no for Footer
rev_no=part_no[-1] # Revision no of the table


###################################################
#   Final Report name
###################################################
test_name = ' SFT Performance Test Report'


###################################################
#   Removes temporary files, if it is still exists
###################################################
if os.path.isfile(r''+str(fixed_dir)+'\\'+str(part_no)
    +str(test_name)+'.docx'):
    
    os.remove(r''+str(fixed_dir)+'\\'+str(part_no)
        +str(test_name)+'.docx')

if os.path.isfile(r''+str(fixed_dir)+'\\temp_doc.docx'):
    os.remove(r''+str(fixed_dir)+'\\temp_doc.docx')

if os.path.isfile(r"C:/temp.xml"):
    os.remove(r"C:/temp.xml")

if os.path.isfile(r"C:/temp1.xml"):
    os.remove(r"C:/temp1.xml")

    
###################################################
#
#   This Dictionaries will change KEYWORDS in Word 
#   Template.
# 
###################################################    
replaceText = {"INITIAL": str(temp_fw_type), #For Document
        "VENDOR" : str(vendor_names[0]),
        "MDLLIST" : new_list,
        "MODEL" : str(model_no_names[0]),
        "FW": str(fw_no_names[0]),
        "DATE":str(date),
        "ECONUM":str(eco_names[0]),
       "PRODUCT":str(product_fnames[0]),
        "REV":str(rev_no)}

replaceText_f = {"FOOTER":str(part_no)} #For Footer


###################################################
#
#   Modifying contents of Word Template. Replacing
#   Keywords in Word Template.
# 
###################################################
modify_word_docx.Modify_Word_Docx(word_file,fixed_dir
    ,part_no,replaceText,replaceText_f, test_name)


###################################################
#
#   Appending Modified .csv files and 2 plots 
#   to the Modified Word template.
# 
###################################################
af.Append_Files(file_names, no_of_files, fixed_dir, part_no,
                   model_no_names, cap_names, chassis_names,
                    cntrllr_names,fd.fw_type_d[fw_type], fw_no_names
                    , test_name, ssd_detection_all)
                    
os.remove(r"C:/temp.xml")
os.remove(r"C:/temp1.xml")
                   
os.chdir(r''+str(c_path)+'/Performance_HDD_SSD')

elapse_time =round((time.time() - start_time),2) # seconds
if elapse_time < 60 :
    print("Elapsed time: %s seconds" % elapse_time )
else:
    print("Elapsed time: %s minutes" % round(((time.time() - start_time)/60),2))

                   
#####################################
#              END                  #
#####################################
