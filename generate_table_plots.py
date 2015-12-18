####################################################
#                  Revision: 1.0                   #
#              Updated on: 11/06/2015              #
####################################################

####################################################
#                                                  #
#   This File generate tables and Plots using      #
#   Original .csv file(s)                          #
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
import fixed_data
import matplotlib.pyplot as plt

import report_functions
import extract_lists
import user_inputs


###################################################
#
#   This function will read Original .csv file(s)
#   and generate Modified .csv files, IOps plot,
#   and MBps plot.
# 
###################################################
def Generate_Table_Plots(file):

    file=str(file).replace('"','')
    d = pandas.read_csv(r''+str(file),skiprows=13,header=None)

    rf = report_functions.Report_Functions
    
    
    ###################################################
    #
    #   Finding only disk drives indices and total
    #   their count to find number of Steps.
    # 
    ###################################################
    data= np.array(d)
    [disk_count,disk_index]= rf.find_string(data,0,0,'DISK') # Finding only disk drives
    
    
    ###################################################
    #
    #   Finding no.of steps 
    # 
    ###################################################
    [steps,disk_no]=rf.no_of_steps(disk_index,disk_count)
    
    
    ###################################################
    #
    #   Deriving only required data
    # 
    ###################################################
    new_data1=data[disk_index,:] #Body
    header=data[0,:] # with all columns

    new_data=np.vstack((header,new_data1)) # Data with required Rows and header
    
    
    ###################################################
    #
    #  Finding indices of unnecessary data to eliminate 
    #  it.
    # 
    ###################################################
    d1 = d

    [c1,i1]=rf.find_string(d1,0,0,'\'Target Type')
    [c2,i2]=rf.find_string(d1,0,0,'ALL')
    [c3,i3]=rf.find_string(d1,0,0,'MANAGER')
    [c4,i4]=rf.find_string(d1,0,0,'PROCESSOR')
    [c5,i5]=rf.find_string(d1,0,0,'WORKER')
    [c6,i6]=rf.find_string(d1,0,0,'DISK')
    [c7,i7]=rf.find_string(d1,0,0,'\'Time Stamp')

    cumm_total=c1+c2+c3+c4+c5+c6+(c7*9) # Multiple 9 because "Time Stamp" has 9 lines
    f_total=int(cumm_total/steps)    
    
    
    ###################################################
    #
    #  Finding Access Specification from the file
    # 
    ###################################################
    a_spec=[]
    for i in range(steps):
        t1=((f_total)*i)+1
        temp1=np.array(d1)
        #print(temp1)
        a1=temp1[t1,2]
        a_spec.append(str(a1))


    for i in range(steps):
        temp2=[a_spec[i]]
        access_spec=temp2*(disk_no)
        #access_spec
        t1=1+(disk_no*i)
        t2=disk_no+1+(disk_no*i)
        #print(t1,t2,temp2)
        new_data[t1:t2,2]=access_spec
        
    
    ###################################################
    #
    #  Selecting required columns from input file.
    #  Required column's list is present in "fixed_data"
    #  file.
    # 
    ###################################################
    l=fixed_data.Fixed_Data.column_list
    
    req_col=[]

    for i in range(len(l)):
        [count,index]=rf.find_string(new_data,0,1,l[i])
        #print(count,index)
        req_col+=index
        
    req_col=np.array(req_col).T
    final_data=new_data[:,req_col]

    
    ###################################################
    #
    #  Generating a Array with array of all steps
    # 
    ###################################################
    final_mat=[]
    for i in range(steps):
        m1=1+(i*disk_no)
        m2=disk_no+(i*disk_no)+1

        avg_mat=[]
        
        for j in range(3,len(final_data[0,:])):
            avg_mat.append(rf.avg_of_disks(final_data[m1:m2,:],j,disk_no))
            
        augment_mat=['MANAGER','AVG',''+a_spec[i]]
        final_mat1=augment_mat+avg_mat
        final_mat1=np.array(final_mat1)
        final_mat1=final_mat1[:,np.newaxis]
        final_mat1=final_mat1.T
        final_mat+=final_mat1 #avg matrix

    final_mat=np.array(final_mat)

    
    ###################################################
    #
    #  Changing  Heading names, because we want these 
    #   names in our Report.
    # 
    ###################################################
    final_data[0,0]='Drive #'
    final_data[0,2]='Access Spec.'
    final_data[0,5]='Avg. Latency'
    final_data[0,6]='Max. Latency'
    final_data[0,7]='Q.D.'
    
    
    ###################################################
    #
    #  Inserting final(average) matrix in Final_data
    # 
    ###################################################
    for i in range(1,steps+1):
        final_data=np.insert(final_data, (disk_no+1)*i, final_mat[i-1], axis=0)


    ###################################################
    #
    #  Pulling Alignment Info from input file
    # 
    ###################################################
    d1=np.array(d1)
    index=[]
    for i in range(len(d1[0,:])):
        [c_a,i_a]=rf.find_string(d1,i,0,'align')
        index.append(i_a)

    col_index=index.index(max(index))
    row_index=max(index)

    alignment=[d1[row_index[0]+1,col_index]]

    align=alignment*((steps*(disk_no+1)))
    a=['Align']
    align_mat=a+align
    align_mat=np.array(align_mat)
    align_mat=align_mat[:,np.newaxis]

    final_data=np.hstack((align_mat,final_data)) 
    # tacking in first column
    #final_data[0,6]='Q.D.'
    

    ###################################################
    #
    #  Writing Modified data in our .csv file
    # 
    ###################################################
    exp=str(file)
    final=final_data
    with open(r'' + str(exp)+"_Modified.csv","w") as out_file:
        out_string= ""
        for i in range(len(final[:,0])): #7

            for j in range(len(final[0,:])): #13

                if j == len(final[0,:])-1:
                    out_string += str(final[i,j]) 
                    
                else:
                    out_string += str(final[i,j]) + "," 

            out_string += "\n"        
        
        out_file.write(out_string) 
        
        
    
    ###################################################
    #
    #  Generating Plots
    # 
    ###################################################
    m_data = pandas.read_csv(open(r''+str(file)+'_Modified.csv'),header=None)

    
    ########################
    #
    #  1st PLOT: IOps 
    # 
    ########################
    md=np.array(m_data)
    [c1,i1]=rf.find_string(md,0,1,'IOps')
    i11=np.array(i1)
    i1=i11-1


    final_mat_n=final_mat[0:,i1].tolist() 
    #converting array to lists of list

    new_d = [i[0] for i in final_mat_n] 
    #converting lists of list to list(i.e. Flattening the list)

    avg = []
    for item in new_d:
        avg.append(float(item)) 
        # converting into float

    v=(max(avg[0:6]))+50

    avg=rf.swap_func(avg,1,2) 
    #swapping element 1 with 2, to make it in order: READ, 67/33, WRITE
    avg=rf.swap_func(avg,4,5)

    x=[1,2,3,4,5,6]
    fig1=plt.figure(1,figsize=(8,12))
    my_xticks=['4k Test Read','4k Test 67/33','4k Test Write','256k Test Read','256k Test 67/33','256k Test Write']
    plt.xticks(x, my_xticks, rotation=-45)
    plt.plot(x[0:3],avg[0:3],'ro-',x[3:6],avg[3:6],'b^-')
    plt.grid(b=True, which='major', color='0.65',linestyle='--')
    plt.legend(('4k Test','256k Test'),loc='best')
    plt.title('Average IOps(random)')
    plt.xlim((0,7))
    plt.ylim((0,v))
    plt.ylabel('IOps')

    fig1.savefig(r''+str(file)+'_Modified.csv_Plot_1.png')
    plt.clf() 


    ########################
    #
    #  2nd PLOT: MBps 
    # 
    ########################
    [c1,i1]=rf.find_string(md,0,1,'Access Spec.')
    i=np.array(i1)
    i1=i
    x1=[1,2,3,4,5,6]

    [m_count1,m1]=rf.find_string(md,0,1,'MBps')
    m1=np.array(m1)

    [z1,seq_write_64k]=rf.find_string(md,3,0,'64k_seq_write')
    [z2,seq_write_512k]=rf.find_string(md,3,0,'512k_seq_write')
    [z3,seq_read_64k]=rf.find_string(md,3,0,'64k_seq_read')
    [z4,seq_read_512k]=rf.find_string(md,3,0,'512k_seq_read')
    comb_index = (seq_write_64k + seq_write_512k + seq_read_64k + seq_read_512k)

    sw64k_list = []
    sw64k=(md[seq_write_64k[:6],m1].tolist())
    for item in sw64k:
        sw64k_list.append(float(item)) # converting into float

    sw512k_list = []
    sw512k=(md[seq_write_512k[:6],m1].tolist())
    for item in sw512k:
        sw512k_list.append(float(item)) # converting into float
       
    sr64k_list = []
    sr64k=(md[seq_read_64k[:6],m1].tolist())
    for item in sr64k:
        sr64k_list.append(float(item)) # converting into float
       

    sr512k_list = []
    sr512k=(md[seq_read_512k[:6],m1].tolist())
    for item in sr512k:
        sr512k_list.append(float(item)) # converting into float

    comb_data=(np.array(md[comb_index,m1]))
    max_value=float(np.amax(comb_data))+50

    [count,target_index]=rf.find_string(m_data,0,1,'Target Name')
    [count,disk_index]=rf.find_string(m_data,1,0,'DISK')
    lst=(np.array(md[disk_index[:disk_no],target_index]))
    ticks_list=[]

    for i in range(disk_no):
        ticks_list.append(lst[i])


    fig2=plt.figure(2,figsize=(12,15))
   
    plt.xticks(x1, ticks_list, rotation=-20)
    plt.plot(x1,sw64k_list,'ro-',x1,sw512k_list,'bo-',x1,sr64k_list,'g^-',x1,sr512k_list,'y^-')
    plt.legend(('seq_write_64k','seq_write_512k','seq_read_64k','seq_read_512k'),loc='best')
    plt.grid(b=True, which='major', color='0.65',linestyle='--')
    plt.title('MBps(Sequential)')
    plt.xlim((0,7))
    plt.ylim((0,max_value))
    plt.ylabel('MBps')
    plt.savefig(r''+str(file)+'_Modified.csv_Plot_2.png')
    plt.clf()

    
#####################################
#              END                  #
#####################################
