####################################################
#                  Revision: 2.0                   #
#              Updated on: 12/18/2015              #
#                                                  #
# What's new:                                      #
#           Support for SSD Peformance files       #
####################################################

####################################################
#                                                  #
#   This File generate tables and Plots using      #
#   Original .csv file(s) for SSD Peformance files.#
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
from openpyxl import load_workbook
import csv
import os
import sys

c1_path = os.getcwd()

import matplotlib.pyplot as plt

import performance_ssd_functions
psf = performance_ssd_functions.Peformance_SSD_Functions

###################################
#  Importing from other Directory
###################################
#os.chdir('..')
c_path = os.getcwd()
sys.path.insert(0, r''+str(c_path)+'/Common Scripts')

import report_functions
rf = report_functions.Report_Functions

import fixed_data
required_columns = fixed_data.Fixed_Data.column_list


''' This function will read Original .csv file(s) 
    and generate Modified .csv files, IOps plot, 
    and MBps plot. '''

def Generate_Table_Plots_SSD(file_path):
    
    # reading data of given file
    data = psf.read_csv_file(file_path)
    
    # Find Number of "DISK" associated with each "WORKER"
    [wrkr_index, each_disk_count] = psf.find_disk_associated_with_worker(rf, data)
    #print("\neach_disk_count:")
    #print(each_disk_count)
    
    # Generate Non-repeatative Test list
    test_list = psf.create_nonrepeatative_list(data, wrkr_index)
    #print("\ntest_list")
    #print(test_list)

    # A dictionary, keys are Required Column names and values are their index.
    req_dict = psf.create_dictionary_of_columns_index(rf, data, required_columns)
    #print("req_dict")
    #print(req_dict)
    #print('\n\n')

    all_test_indices = psf.find_indices_of_testlist(rf, data, req_dict, each_disk_count, test_list)
    #print("\nall_test_indices:")
    #print(all_test_indices)
    
    # Extracting Alignment Info from 1st test. 
    align_info = psf.find_alignment_info(data)

    extracted_data = psf.extract_all_data(data, all_test_indices, req_dict, required_columns, align_info)

    header = "Align,Drive #,Target Name,Access Spec.,IOps,MBps,Avg. Latency,Max. Latency,Q.D.,Read Errors,Write Errors"

    psf.write_csv_file(file_path, extracted_data, header)

     

    ###################################################
    #
    #  Generating Plots
    # 
    ###################################################
    m_data = pandas.read_csv(open(r'' + str(file_path)+"_Modified.csv"),header=None)

    # create Plot 1
    psf.create_avg_iops_plot1(m_data, file_path)

    psf.create_mbps_drive_plot2(m_data, file_path)


#####################################
#              END                  #
#####################################
