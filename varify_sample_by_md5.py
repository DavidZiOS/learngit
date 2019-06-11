#!usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :6/6/2019
# @Author   : zhangdawei@yikongenomics.com

import os
import re
import sys
import subprocess
import argparse


def read_old_md5(MD5_old_file):
    line_number_MD5 = {}
    MD5_raw_name = {}
    line_num = 0
    with open(MD5_old_file,'r',encoding='gbk') as OLD:
        for line in OLD.readlines():
            line = line.strip()
            line_num += 1
            line_number_MD5[line_num] = line

    for number_MD5 in line_number_MD5.keys():
        if re.search('fastq',line_number_MD5[number_MD5]):
            temp_list = line_number_MD5[number_MD5].split('\\')
            fastq_name = temp_list[-1]
            fastq_name = re.sub('.fastq.*', '', fastq_name)
            temp_list_Md5 = line_number_MD5[number_MD5 + 1].split(' ')
            Md5_raw_value = "".join(temp_list_Md5)
            #print(fastq_name, Md5_raw_value)
            MD5_raw_name[fastq_name] = Md5_raw_value

    return(MD5_raw_name)
    
def generate_new_md5(old_value_dir, new_MD5_file):
    all_files = os.listdir(old_value_dir)
    for file in all_files:
        if re.search('fastq', file):
            print(file)
            file_path = old_value_dir + '/' + file
            file_MD5_sh = 'md5sum ' + file_path + ">>" + new_MD5_file
            subprocess.call(file_MD5_sh,shell=True)
            

def read_new_md5(new_MD5_file):
    MD5_new_name = {}
    new_MD5_info = open(new_MD5_file,'r')
    for line_02 in new_MD5_info.readlines():
        line_02 = line_02.strip()
        temp_list_Md5_new = line_02.split('  ')
        fastq_name_new = temp_list_Md5_new[1].split('/')[-1]
        fastq_name_new = re.sub('.fastq.*', '', fastq_name_new)
        #print(fastq_name_new, temp_list_Md5_new[0])
        MD5_new_name[fastq_name_new] = temp_list_Md5_new[0]
    return(MD5_new_name)

def verify_md5(MD5_raw_name, MD5_new_name):
    samples = []
    for fastq_name_last in MD5_raw_name.keys():
        #print(fastq_name_last)
        if fastq_name_last in MD5_new_name.keys():
            if MD5_raw_name[fastq_name_last] == MD5_new_name[fastq_name_last]:
                print(fastq_name_last, ' verified pass')
                samples.append(fastq_name_last)
                pass
            else:
                print(fastq_name_last + ' need to copy the file again')
        else:
            if re.match('Undetermined',fastq_name_last):
                pass
            else:
                print(fastq_name_last + ' no this sample ')
    return(samples)

def gzip_verifies_fastq(data_dir, verified_samples):
    for sample in verified_samples:
        sample_fastq = data_dir + '/' + sample + '.fastq'
        if os.path.exists(sample_fastq):
            print('gzip ', sample_fastq, ' &')

def main():
    parser = argparse.ArgumentParser(description="use md5 to verifies the integrities of the file")
    parser.add_argument('--old_md5_file', action="store", required=True,help="The old MD5 file.")
    parser.add_argument('--data_dir', action="store", required=True,help="The data dir")
    args = parser.parse_args()
    old_md5 = args.old_md5_file
    data_dir = args.data_dir

# 1. get the old_md5
    dict_old_md5 = read_old_md5(old_md5)

# 2. use md5sum to generate new_md5
    new_md5 = data_dir + 'new_md5.txt'
    if os.path.exists(new_md5):
        pass
    else:
        generate_new_md5(data_dir, new_md5)

# 3. parse new_md5, new/old all name:md5
    dict_new_md5 = read_new_md5(new_md5)

# 4. use the same key to check value
    verified_samples = verify_md5(dict_old_md5, dict_new_md5)

# 5. for verified samples, if fastq do gzip
    gzip_verifies_fastq(data_dir, verified_samples)

if __name__ == '__main__':
    main()



