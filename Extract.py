import time
import re
import string
import os
import csv

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json
Current_A=0
Current_B=0
filename_A=0
filename_B=0

def Find_Timelines_A(source, Dest):
    missed_list = []
    word_sequence = 0
    main_sequence=0
    global Current_A
    global filename_A
    writer = csv.writer(Dest)
    prev_line=None
    for line in Dest:
        line_split = line.split("\t")
        category = line_split[1]
        text = line_split[-1]
        if (category == 'A'):
            if (prev_line == text):
                continue
            prev_line = text
            Text_A=text
            length_A=len(Text_A.split())
            i=0
            count=0
            missed_words=0
            Intervals=['?', '?']
            Text_A=re.sub('um', 'uh', Text_A)
            Text_A_split = Text_A.split(' ')
            for line_num, line_text in enumerate(filename_A):
                if (line_num >= Current_A):
                    line_text_split = line_text.split(' ')
                    # pattern to match [ * ] which is a noise
                    line_text_split[-1]=re.sub('-','',line_text_split[-1])
                    line_text_split[-1]=re.sub('um','uh',line_text_split[-1])
                    pattern = re.compile(".*\[.*\].*")
                    match=pattern.match(line_text_split[-1].strip('\n'))
                    if(match):
                        count = count + 1
                        continue
                    elif (line_text_split[-1].strip('\n')==Text_A_split[i].strip('\n')):
                        if(i==0):
                            Intervals[0]=float(line_text_split[1])
                        i=i+1
                        main_sequence += 1
                        if(word_sequence>0 and main_sequence>2):
                            missed_list[:] = []
                            word_sequence = 0
                        if('\n' in Text_A_split[i-1] and (length_A<2 or main_sequence>2)):
                            Intervals[1]=float(line_text_split[1])
                            missed_list[:] = []
                            word_sequence = 0
                            main_sequence=0
                            break
                    else:
                        missed_list.append(Text_A_split[i].strip('\n'))
                        for wcount, missed_word in enumerate(missed_list):
                            if(missed_word==line_text_split[-1].strip('\n')):
                                word_sequence+=1
                                break
                                '''if (word_sequence==3):
                                    missed_list[:]=[]
                                    word_sequence=0'''
                        missed_words = missed_words + 1
                        '''if((len(line_text_split[-1].strip('\n'))<3)):
                            i=i+1
                            #break
                        if (len(Text_A_split[i].strip('\n'))<3):
                            i=i+2
                        if(line_num>length_A+count+Current_A):
                            break'''
                        #if(Text_A=='yeah\n'):
                            #break
                    #if (line_text_split[-1]=='[silence]'):
                        #continue

                '''
                    if(line_text[-1]==Text_A_split[i]):
                        i=i+1
                    if(length_A==i-1)'''
        writer.writerow(str(Intervals[0])+'\t'+str(Intervals[1]))
        writer.writerow("\n")
    return Intervals;

def Find_Timelines_B(Text_B):
    global Current_B
    global filename_B
    return;

# We use the file saved from last step as example
new_path='/home/vivek/Nishitha/swb_ms98_transcriptions'
for root, dirs, files in os.walk('/home/vivek/Nishitha/swda_files'):
    for file in files:
        with open(os.path.join(root, file), 'ab+') as swda_file:
            dir_name=file.split(".")[0]
            file_A=new_path+'/'+dir_name[:2]+'/'+dir_name+'/'+'sw'+dir_name+'A-ms98-a-word.text'
            file_B = new_path + '/' + dir_name[:2] + '/' + dir_name + '/' + 'sw' + dir_name + 'B-ms98-a-word.text'
            filename_A=open(file_A,'r')
            filename_B = open(file_B, 'r')
            Current_A = 0
            Current_B = 0
            Find_Timelines_A(filename_A,swda_file)
            Find_Timelines_A(filename_B,swda_file)
            '''for line in swda_file:
                line_split=line.split("\t")
                category=line_split[1]
                text=line_split[-1]
                if (category=='A'):
                    Interval_A=Find_Timelines_A(text)
                elif(category=='B'):
                    Interval_B=Find_Timelines_B(text)'''

            '''for root1, dirs1, files1 in os.walk('/home/vivek/Nishitha/swb_ms98_transcriptions'):
                if dir_name in root1:
                    for file1 in files1:
                        with open(os.path.join(root1, file1), 'r') as tweets_file1:
                            if (file.split(".")[0] in root):
                                print "test"'''