# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import csv, re, cStringIO, codecs, string
import sys, time, os
import re
import pprint

#unicode writer
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def clean_unicode(s):
    return s.encode('ascii','ignore')

def extractIntData(line, category, temp_dict, indexOfData):
    digits = re.findall(r"[-+]?\d*\.\d+|\d+",line)
    if indexOfData>=len(digits):
        temp_dict[category] = "n/a"
    else:
        temp_dict[category] = digits[indexOfData]
    return temp_dict

print "Welcome to CSV writer:"
# find .txt files
# directory = "/home/fkm4/results/analysis"
directory = "/Users/KeiMasuda/Desktop/2013DattaLab/Datta_Python/analysis"
# directory = "/Users/KeiMasuda/Desktop/2013DattaLab/Datta_Python/Results"
data = []
for folder in os.listdir(directory):
    if not folder.startswith('.'):
        for filename in os.listdir(directory+'/'+folder):
            if ".txt" in filename:
                #parsing .txt file into object
                text_file = open(directory+'/'+folder+'/'+filename, "r")
                lines = text_file.readlines()
                temp_dict = {}

                #parse out screendayN, ms4, odor mix
                temp_dict['filename'] = filename[:-4]
                splitName = filename[:-5].split("_")
                #strange mix names
                strangeMixNames = ['guan','co2','cs2','uroguan']
                for name in splitName:
                    if 'screenN' in name:
                        temp_dict['screenN'] = name
                    elif 'screenday' in name:
                        temp_dict['screenday'] = name
                    elif 'mix' in name:
                        temp_dict['mix'] = name
                    elif 'guan' in name:
                        temp_dict['mix'] = name
                    elif 'co2' in name:
                        temp_dict['mix'] = name
                    elif 'cs2' in name:
                        temp_dict['mix'] = name
                    elif 'uroguan' in name:
                        temp_dict['mix'] = name
                    elif 'uan' in name:
                        temp_dict['mix'] = 'guan'
                    else:
                        temp_dict['ms4'] = name


                #Data Read out categories from txt file
                categories = ['Total Cells:', 'Number of 5 std:', 'Number of 20 std:','Number of 50 std:', 'Average Normalized Max Response for 5 std:','Average Normalized Max Response for 20 std:','Average Normalized Max Response for 50 std:', 'Top 10%% df/f mean:','Top 25%% df/f mean:','Top 10%% df/f mean of max:','Top 25%% df/f mean of max:','Top 100%% df/f mean of max:']
                categoryNames = ['totalCells', 'Num_5std', 'Num_20std', 'Num_50std', 'MeanMax5std','MeanMax20std','MeanMax50std', 'top10dff_Mean','top25dff_Mean', 'top10dff_MeanMax', 'top25dff_MeanMax','top100dff_MeanMax']
                dataIndices = [0,1,1,1,1,1,1,1,1,1,1,1]
                # categories = ['Total Cells:']
                # categoryNames = ['totalCells']
                # dataIndices = [0]

                #check if data lists same size
                if not len(categories)==len(categoryNames)==len(dataIndices):
                    print "Exited: lists of cagetories, names, and dataIndices not the same size"
                    sys.exit()

                #read data into temp_dict
                for line in lines:
                    for i in range(len(categories)):
                        if categories[i-1] in line:
                            extractIntData(line, categoryNames[i-1], temp_dict, dataIndices[i-1])

                # pass temp dict into data
                data.append(temp_dict)
                text_file.close()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(data)


# <codecell>

#open csv file in new directory
outfile = directory + "/" + "csvOutputs"
if not os.path.exists(outfile):
    os.makedirs(outfile)

# <codecell>

screenNList = []
for dictionary in data:
    for key, value in dictionary.iteritems():
        if key is "screenN" and value not in screenNList:
            screenNList.append(value)
print screenNList

categories = []
for dictionary in data:
    keys = dictionary.keys()
    categories= list(set(categories) | set(keys))
print categories

# <codecell>

# data_categories = ['totalCells', 'Num_5std', 'Num_20std', 'Num_50std', 'MeanMax5std','MeanMax20std','MeanMax50std', 'top10dff_Mean','top25dff_Mean', 'top10dff_MeanMax', 'top25dff_MeanMax','top100dff_MeanMax'] 

# <codecell>

def dataHunter(data, screenN, category, mix, ms4):
    datum = ''
    for slide in data:
        if 'screenN' in slide:
            if slide['screenN'] == screenN:
                if 'mix' in slide:
                    if slide['mix'] == mix:
                        if 'ms4' in slide:
                            if slide['ms4'] == ms4:
                                if category in slide:
                                    datum = slide[category]
                                    break
    return datum

# <codecell>

# def dataHunter(data, screenN, category, mix, ms4):
#     datum = ''
#     for slide in data:
#         if slide['screenN'].lower() == screenN.lower():
#             if slide['mix'].lower() == mix.lower():
#                 if slide['ms4'].lower() == ms4.lower():
#                     if category.lower() in slide.lower():
#                         datum = slide[category]
#                         break
#     return datum

# <codecell>

for screenN in screenNList:
    print "+++++++++++" + screenN + "++++++++++++++++++++++"
    NofScreenData = [dictio for dictio in data if dictio.has_key('screenN') is True]
    filteredNofScreenData = []
    for dictio in NofScreenData:
        if dictio['screenN'] == screenN:
            filteredNofScreenData.append(dictio)
    for category in categories:
        print "==========" + category + "==========="
        output = open(outfile+"/"+screenN+"_"+category+".csv", "wb")
        print output
        writer = UnicodeWriter(output)
        
        # add header row
        headerRow = []
        for slide in data:
            if 'screenN' in slide:
                if slide['screenN'] == screenN:
                    if 'ms4' in slide:
                        if slide['ms4'].lower() not in headerRow:
                            headerRow.append(slide['ms4'].lower())
        # headerRow = sorted(headerRow)
        headerRow_withTitle = []
        headerRow_withTitle = headerRow[:]
        headerRow_withTitle[:0] = ["Mix Names"]
        print headerRow_withTitle
        writer.writerow(headerRow_withTitle)
        
        #find mix names
        mixNames = []
        for slide in data:
            if 'screenN' in slide:
                if slide['screenN'] == screenN:
                    if 'mix' in slide:
                        if slide['mix'].lower() not in mixNames:
                            mixNames.append(slide['mix'].lower())
        print mixNames
        # mixNames = sorted(mixNames)
    
        #add data
        #for each headerRow category
        
        for mix in mixNames:
            tempRow = []
            tempRow.append(mix)
            for ms4 in headerRow:
                tempRow.append(dataHunter(data, screenN, category, mix, ms4))
            writer.writerow(tempRow)
        output.close()

# <codecell>

print "Done with CSV Writer."

# <codecell>

 

