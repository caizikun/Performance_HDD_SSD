####################################################
#                  Revision: 2.0                   #
#              Updated on: 12/18/2015              #
#                                                  #
# What's new:                                      #
#           Support functions for SSD              #
#           Peformance files.                      #
####################################################

####################################################
#                                                  #
#   This File has all functions required to        #
#   generate Modified .csv, Average IOps plot,     #
#   and Sequential MBps plot for SSD Peformance    # 
#   files.                                         #
#                                                  #
#   Author: Zankar Sanghavi                        #
#                                                  #
#   © Dot Hill Systems Corporation                 #
#                                                  #
####################################################

###################################################
#
#   Importing required packages
# 
###################################################
import pandas
import numpy as np
import os
import sys
import csv

from openpyxl import load_workbook

import matplotlib.pyplot as plt

###################################
#  Importing from other Directory
###################################
os.chdir('..')
c_path = os.getcwd()
sys.path.insert(0, r''+str(c_path)+'/Common Scripts')

import report_functions
rf = report_functions.Report_Functions

import fixed_data
fd = fixed_data.Fixed_Data

''' This class contains all Functions 
    useful to extract data from SSD
    Performance file '''
    
class Peformance_SSD_Functions:
    
    ''' To check if path exists and/or if file is corrupt '''
    def read_csv_file(file_path):
        try:
            data = pandas.read_csv(open(r'' + str(file_path)),header=None, skipinitialspace=True)
            return data
        except:
            data = pandas.read_csv(open(r'' + str(file_path)),skiprows=13,header=None)
            return data
            

  
    ''' Find Number of "DISK" associated with each "WORKER" '''
    def find_disk_associated_with_worker(rf, data):
        

        # Find indices of "WORKER"
        data= np.array(data)
        #print(data)

        [wrkr_count,wrkr_index]= rf.find_string(data,0,0,'WORKER') # Finding only disk drives
        
        #print("\nWORKER INDEX:")
        #print(wrkr_index)

        each_disk_count = []
        for i in range(len(wrkr_index)):
            #print(i)
            if i == len(wrkr_index)-1:
                #print(i)
                temp_data = data[wrkr_index[i] :]
                
                #print("IF")
                #print(temp_data)
                
                [disk_count,disk_index]= rf.find_string(temp_data,0,0,'DISK') # Finding only disk drives

            else:
                #print(i,i+1)
                temp_data = data[wrkr_index[i] : wrkr_index[i+1]]
                
                #print("ELSE")
                #print(temp_data)
                
                [disk_count,disk_index]= rf.find_string(temp_data,0,0,'DISK') # Finding only disk drives

            each_disk_count.append([wrkr_index[i], disk_count])
        return [wrkr_index, each_disk_count]
    


    ''' This function will exclude repeatative elements '''
    def create_nonrepeatative_list(data, wrkr_index):
        
        if len(wrkr_index) != 0:
            data = np.array(data)
            oldlist = data[wrkr_index,2].tolist()

            newlist=[]
            for i in range(len(oldlist)):
                if oldlist[i] not in newlist:
                    newlist.append(oldlist[i])
            return newlist
        
        else:
            return print("WORKER indices empty!")
            sys.exit()
    
    

    ''' This function will create a dictionary
    relating Column with its Index '''
    def create_dictionary_of_columns_index(rf, data, column_list):
        
        [tt_count,tt_index] = rf.find_string(data,0,0,'\'Target Type')
        
        column_dict = {}

        for i in range(len(column_list)):

            [temp_count,temp_index] = rf.find_string(data, tt_index[0], 1, str(column_list[i]))
            column_dict[column_list[i]] = temp_index[0]

        return column_dict
        
        
        
    ''' This function collects indices of each test
        from "testlist" makes a list out of it. And
        returns a Super-list for all tests in 
        "testlist" '''
    def find_indices_of_testlist(rf, file_data, req_dict, wrkr_index, testlist):
        
        each_test_indices = []
        for i in range(len(testlist)):

            [test_count, test_index] = rf.find_string(file_data, req_dict['Access Specification Name'], 0, testlist[i])

            temp_list = []
            for j in range(len(test_index)):
                for k in range(len(wrkr_index)):
                    if test_index[j] == (wrkr_index[k])[0]:
                        temp_list.append(wrkr_index[k]) 

            each_test_indices.append(temp_list)
            
        return each_test_indices 



    ''' Grab Alignment Info from 1st Test '''
    def find_alignment_info(data):
        # top 13 rows
        #top_data = data[0:13]
        top_data = np.array(data)

        # seraching '\size' which contains 'align' column
        [size_count, size_index] = rf.find_string(top_data, 0, 0, '\'size')
        #size_index[0]

        # seraching 'align' column to find align info.
        [align_count, align_index] = rf.find_string(top_data, size_index[0], 1, 'align')
        #align_index[0]

        align_info = [top_data[size_index[0]+1,align_index[0]]]

        return align_info

        
    ''' To check if given number is float.
    It also works for Int. '''
    def is_it_float(num):
    
        try:
            float(num)
            return True

        except:
            return False
    


    ''' To check if given number is an Integer.
    It also works for Int. '''
    def is_it_int(num):
    
        try:
            int(num)
            return True

        except:
            return False    
            

            
    ''' This function we extract data of Drive's data 
    with required_columns. '''
    def extract_all_data(data, all_test_indices, req_dict, required_columns, align_info):
        
        data = np.array(data)
        
        super_final_data = []
        for i in range(len(all_test_indices)):

            final_data = []
            for j in range(len(all_test_indices[i])):

                temp = all_test_indices[i][j]
                #print(temp)

                for k in range(1, temp[1]+1):
                    temp_list = []        
                    #print(k)
                    for l in range(len(req_dict)):

                        if required_columns[l] == 'Access Specification Name':

                            td1 = data[temp[0],req_dict[required_columns[l]]]
                            access_spec = td1
                            #print(td1)


                        else:
                            td1 = data[temp[0]+k,req_dict[required_columns[l]]]
                            #print(td1)

                        if l < len(req_dict):
                            #temp_list += td1
                            
                            if Peformance_SSD_Functions.is_it_int(td1):
                                temp_list.append(int(td1))
                            
                            elif Peformance_SSD_Functions.is_it_float(td1):
                                temp_list.append(float(td1))

                            else:


                                temp_list.append(td1)
                            #print(temp_list)
                temp_list = align_info + temp_list
                final_data.append(temp_list)

                #final_data1 = np.array(final_data)


            temp1 = [final_data[t][4:] for t in range(len(final_data))]
            #print(temp1)

            temp = np.array(temp1)
            #print(temp)
            temp1 = (np.mean(temp, axis = 0, dtype=np.float32)).tolist()
            #temp1 = np.array(temp1)
            temp2 =  [str(align_info), 'MANAGER', 'AVG', str(access_spec)] 
            #temp2 = np.array(temp2)
            #print("\nTemp1:")
            #print(temp1, type(temp1))
            
            #print("\nTemp2:")
            #print(temp2, type(temp2))
            
            temp = temp2 + temp1
            
            #print("\nTemp:")
            #print(temp)
            
            final_data = (np.vstack((final_data, temp))).tolist()
            
            super_final_data += final_data

        return super_final_data       
        
        
        
    ''' This function will write given data into a .csv file 
    in same directory of the original file. Path is given
    by "file_path" '''
    def write_csv_file(file_path, extracted_data, header):

        try:
            with open(r'' + str(file_path)+"_Modified.csv","w") as out_file:
                
                out_string = ""
                out_string += header
                out_string += "\n"
                
                for i in range(len(extracted_data)): 

                    temp_str = (str(extracted_data[i])).strip("[")
                    temp_str = temp_str.strip("]")
                    temp_str = temp_str.replace("'","")
                    temp_str = temp_str.replace(", ",",")
                    temp_str = temp_str.replace("\"","")
                    temp_str = temp_str.replace("[","")
                    temp_str = temp_str.replace("]","")

                    out_string += temp_str 
                    out_string += "\n"        

                out_file.write(out_string) 
        except:
            return print("\nFailed to write .csv file!")    
            sys.exit()
    
    
    ''' This function will generate 
    a plot of Average IOps for 
    4k and 256k test '''
    def create_avg_iops_plot1(data, file_path):
        
        import matplotlib
        import matplotlib.pyplot as plt
        
        ''' Finding indices of IOps, Target Name et al
            which is used to extract data from modified 
            csv file '''
        md=np.array(data)

        [iops_c, iops_index] = rf.find_string(md,0,1,'IOps')

        [tn_c, tn_index] = rf.find_string(md,0,1,'Target Name')
        #print([tn_c, tn_index[0]])

        [as_c, as_index] = rf.find_string(md,0,1,'Access Spec.')
        #print(as_index)

        try: 
            [avg_c, avg_index] = rf.find_string(md,tn_index[0],0,'AVG')
            
            if len(avg_index) == 0:
                [avg_c, avg_index] = rf.find_string(md,tn_index[0],0,' AVG')
        except: 
            print("Error in finding string \"AVG\"! ")

        ''' Finding Average IOps data for 4K & 256K tests ''' 
        import re

        avg_list=[]
        as_list=[]

        for i in range(len(avg_index)):

            temp = re.findall(r'\d+', str(md[avg_index[i], as_index[0]]))[0]
            #print(temp)
            if temp == '4' or temp == '256':
                as_list.append(md[avg_index[i], as_index[0]])
                avg_list.append(md[avg_index[i], iops_index[0]])
        
        #print('\nAccess Spec:')
        #print(as_list, len(as_list))
                
        ''' Swapping  #swapping element 1 with 2, to make it in order: READ, 67/33, WRITE '''
        as_list = rf.swap_func(as_list, 1,2)
        as_list = rf.swap_func(as_list, 4,5)

        avg_list = rf.swap_func(avg_list, 1,2)
        avg_list = rf.swap_func(avg_list, 4,5)
        
        
        ''' Generating Plot and Saving it given "file_path" '''
        fig1=plt.figure(1,figsize=(8,12))

        x = [1,2,3,4,5,6]

        plt.xticks(x, as_list, rotation=-45)

        plt.plot(x[0:3],avg_list[0:3],'ro-',x[3:6],avg_list[3:6],'b^-')
        plt.grid(b=True, which='major', color='0.65',linestyle='--')
        plt.legend(('4k Test','256k Test'),loc='best')
        plt.title('Average IOps(random)')
        plt.xlim((0,7))
        #plt.ylim((0,v))
        plt.ylabel('IOps')

        fig1.savefig(r''+str(file_path)+'_Modified.csv_Plot_1.png')
        plt.clf()
    
    

    ''' This function will generate MBps plot:
    It will plot MBps of all drive for 64k & 
    512 sequential read and write'''
    def create_mbps_drive_plot2(data, file_path):
        
        ''' Finding indices of IOps, Target Name et al
            which is used to extract data from modified 
            csv file '''
        
        md=np.array(data)

        [mbps_c, mbps_index] = rf.find_string(md,0,1,'MBps')


        [tn_c, tn_index] = rf.find_string(md,0,1,'Target Name')
        #print([tn_c, tn_index[0]])

        [as_c, as_index] = rf.find_string(md,0,1,'Access Spec.')
        #print(as_index)

        [dno_c, dno_index] = rf.find_string(md,0,1,'Drive #')

        try: 
            [avg_c, avg_index] = rf.find_string(md,tn_index[0],0,'AVG')
            if len(avg_index) == 0:
                [avg_c, avg_index] = rf.find_string(md,tn_index[0],0,' AVG')
        except: 
            print("Error finding \"AVG\" string!")
            
            
        ''' List of 64k & 512k tests '''    
        import re

        as_list=[]

        for i in range(len(avg_index)):

            temp = re.findall(r'\d+', str(md[avg_index[i], as_index[0]]))[0]
            if temp == '64' or temp == '512':
                as_list.append(md[avg_index[i], as_index[0]])
        
        #print(as_list)
        
        ''' Generating Plot and Saving it given "file_path" '''
        import matplotlib
        import matplotlib.pyplot as plt
        

        # Searching Number of Disks for plotting on X-axis
        [temp_c, temp_index] = rf.find_string(md,as_index[0],0,as_list[0])
        try:
            no_of_disk = [ temp_index[i] for i in range(len(temp_index)) if md[temp_index[i],dno_index[0]]  == 'DISK']
            if no_of_disk == 0:
                no_of_disk = [ temp_index[i] for i in range(len(temp_index)) if md[temp_index[i],dno_index[0]]  == ' DISK']
        except:
            #no_of_disk = [ temp_index[i] for i in range(len(temp_index)) if md[temp_index[i],dno_index[0]]  == 'DISK']
            print("Cannot find \"DISK\"!")
            
        #print(no_of_disk, len(no_of_disk))
        x = [x1 for x1 in range(1, len(no_of_disk)+1)]

        fig2=plt.figure(2,figsize=(12,15))

        # max value to set y-axis's range
        max_value = 0

        for i in range(len(as_list)):

            # indices of each test
            [temp_c, temp_index] = rf.find_string(md,as_index[0],0,as_list[i])
            #print(temp_index)

            # indices of each "DISK", to filter "AVG" values
            try:
                final_disk_index = [ temp_index[i] for i in range(len(temp_index)) if md[temp_index[i],dno_index[0]]  == 'DISK']
                if final_disk_index == 0:
                    final_disk_index = [ temp_index[i] for i in range(len(temp_index)) if md[temp_index[i],dno_index[0]]  == ' DISK']
 
            except:
                #final_disk_index = [ temp_index[i] for i in range(len(temp_index)) if md[temp_index[i],dno_index[0]]  == 'DISK']
                print("Cannot find \"DISK\"!")
                
            #print(final_disk_index)  

            temp_x = md[final_disk_index, tn_index]
            temp_y = md[final_disk_index, mbps_index]

            # converting to float from String
            temp_y = [float(temp_y[i]) for i in range(len(temp_y))]
            #print("\ntemp_y")
            #print(temp_y)  

            # Find maximum value of all data
            if max(temp_y) > max_value:
                max_value = max(temp_y)

            # For 0,1: Use "o-"    
            if i<2:
                plt.plot(x,temp_y, 'o-')

            # For 2,3: Use "^o-"
            else:
                plt.plot(x,temp_y, '^-')


        plt.legend(as_list,loc='best')

        plt.xticks(x, temp_x, rotation=-20)

        plt.grid(b=True, which='major', color='0.65',linestyle='--')
        plt.title('MBps(Sequential)')
        plt.xlim((0,len(as_list)+2))
        plt.ylim((0,max_value+50))
        plt.ylabel('MBps')
        plt.savefig(r''+str(file_path)+'_Modified.csv_Plot_2.png')
        plt.clf()
        
        
    ''' This function will check if File name 
    has any SSD string in it. If it has,
    then it is assumed that it is assumed 
    that it a SSD Performance file and 
    processed accordingly '''
    def detect_ssd(no_of_files, file_names, ssd_name_list):
        
        ssd_detection = []

        for i in range(no_of_files):

            file_directory, file_name = os.path.split(file_names[i])

            for s in range(len(ssd_name_list)):

                ssd_flag = 0 # 0 means its not SSD or its HDD
                if str(ssd_name_list[s]) in file_name:
                    print("\nSSD Performance file detected, File: " + str(i+1))
                    ssd_flag = 1 # 1 means it is a SSD
                    break
            ssd_detection.append(ssd_flag)
        
        return ssd_detection 
            
#####################################
#              END                  #
#####################################    