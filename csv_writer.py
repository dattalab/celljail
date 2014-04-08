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
                for name in splitName:
                    if 'screenN' in name:
                        temp_dict['screenN'] = name
                    elif 'screenday' in name:
                        temp_dict['screenday'] = name
                    elif 'mix' in name:
                        temp_dict['mix'] = name
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
# pp.pprint(data)

def sub_dict(somedict, somekeys, default=None):
    return dict([ (k, somedict.get(k, default)) for k in somekeys ])

def copyf(dictlist, key, valuelist):
    return [dictio for dictio in dictlist if dictio[key] in valuelist]

#open csv file in new directory
outfile = directory + "/" + "csvOutputs"
if not os.path.exists(outfile):
    os.makedirs(outfile)

NofScreen = ["screenNof1","dataforscreenNof2"]
categories = ['totalCells', 'Num_5std', 'Num_20std', 'Num_50std', 'MeanMax5std','MeanMax20std','MeanMax50std', 'top10dff_Mean','top25dff_Mean', 'top10dff_MeanMax', 'top25dff_MeanMax','top100dff_MeanMax'] 
for screenN in NofScreen:

    screenNList = [screenN]
    print [screenNList]
    NofScreenData = [dictio for dictio in data if dictio.has_key('screenN') is True]
    # pp.pprint(NofScreenData)
    NofScreenData = [dictio for dictio in NofScreenData if dictio['screenN'] in screenNList]
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
                        if slide['ms4'] not in (s.lower() for s in headerRow):
                        # if slide['ms4'] not in headerRow:
                            headerRow.append(slide['ms4'])
        # headerRow = sorted(headerRow)
        headerRow_withTitle = []
        headerRow_withTitle = headerRow[:]
        headerRow_withTitle[:0] = ["Mix Names"]
        print headerRow_withTitle
        # writer.writerow(headerRow_withTitle)

        #find mix names
        mixNames = []
        for slide in data:
            if 'screenN' in slide:
                if slide['screenN'] == screenN:
                    if 'mix' in slide:
                        if slide['mix'] not in mixNames:
                            mixNames.append(slide['mix'])
        # print mixNames
        # mixNames = sorted(mixNames)


        #add data
        #for each headerRow category

        for mix in mixNames:
            tempRow = []
            tempRow.append(mix)
            for ms4 in headerRow:
                datum = None

                for slide in NofScreenData:
                    # if 'screenN' in slide:
                        if 'mix'in slide:
                            if 'ms4' in slide:
                                if (slide['screenN'] == screenN and slide['mix'] == mix and slide['ms4'] == ms4):
                                    datum = slide[category]
                # for slide in data:
                #     if 'screenN' in slide:
                #         if slide['screenN'] == screenN:
                #             if 'mix' in slide:
                #                 if slide['mix'] == mix:
                #                     if 'ms4' in slide:
                #                         if slide['ms4'] == ms4:
                #                             tempRow.append(slide[category])
                #                         else:
                #                             tempRow.append("---")

                if datum is not None:
                    tempRow.append(datum)
                else:
                    tempRow.append('')
            # print tempRow
            # writer.writerow(tempRow)

        output.close()















        # categoryData = [dictio for dictio in NofScreenData if dictio.has_key(category) is True]
        # categoryList = [category]
        # for slide in categoryData:
        #     if slide = categoryData
        #     pp.pprint(slide)


        # categoryData = [dictio for dictio in categoryData if dictio[str(category)] in categoryList]
        # pp.pprint(categoryData)
        # pp.pprint(categoryData2)
        # if category is 'totalCells':
        #     print "totalCells"

        # toCSV = []
        # keylist = ['mix','ms4',category]
        # categoryData = [dictio for dictio in NofScreenData if dictio.has_key(category) is True]
        # for dictio in categoryData:
        #     for k in dictio.keys(): 
        #         if k not in keylist: 
        #             del dictio[k]
        # toCSV.append(dictio)
        # pp.pprint(toCSV)
            
        

        # output = open(outfile+"/"+screenN+"_"+category+".csv", "wb")
        # print output
        # dict_writer = csv.DictWriter(output, headerRow_withTitle)
        # dict_writer.writer.writerow(headerRow_withTitle)
        # dict_writer.writerows(toCSV)
        # output.close()

#==========================================
# NofScreen = ["screenNof1","dataforscreenNof2"]
# categories = ['totalCells', 'Num_5std', 'Num_20std', 'Num_50std', 'MeanMax5std','MeanMax20std','MeanMax50std', 'top10dff_Mean','top25dff_Mean', 'top10dff_MeanMax', 'top25dff_MeanMax','top100dff_MeanMax'] 
# for screenN in NofScreen:
#     for category in categories:
#         output = open(outfile+"/"+screenN+"_"+category+".csv", "wb")
#         print output
#         writer = UnicodeWriter(output)

#         # add header row
#         headerRow = []
#         for slide in data:
#             if 'screenN' in slide:
#                 if slide['screenN'] == screenN:
#                     if 'ms4' in slide:
#                         if slide['ms4'] not in headerRow:
#                             headerRow.append(slide['ms4'])
#         headerRow = sorted(headerRow)
#         headerRow_withTitle = []
#         headerRow_withTitle = headerRow[:]
#         headerRow_withTitle[:0] = ["Mix Names"]
#         writer.writerow(headerRow_withTitle)

#         #find mix names
#         mixNames = []
#         for slide in data:
#             if 'screenN' in slide:
#                 if slide['screenN'] == screenN:
#                     if 'mix' in slide:
#                         if slide['mix'] not in mixNames:
#                             mixNames.append(slide['mix'])
#         mixNames = sorted(mixNames)

#         #add data
#         #for each headerRow category

#         for mix in mixNames:
#             tempRow = []
#             tempRow.append(mix)
#             for ms4 in headerRow:
#                 datum = None

#                 for slide in data:
#                     if 'screenN' in slide:
#                         if 'mix'in slide:
#                             if 'ms4' in slide:
#                                 if (slide['screenN'] == screenN and slide['mix'] == mix and slide['ms4'] == ms4):
#                                     datum = slide[category]
#                 # for slide in data:
#                 #     if 'screenN' in slide:
#                 #         if slide['screenN'] == screenN:
#                 #             if 'mix' in slide:
#                 #                 if slide['mix'] == mix:
#                 #                     if 'ms4' in slide:
#                 #                         if slide['ms4'] == ms4:
#                 #                             tempRow.append(slide[category])
#                 #                         else:
#                 #                             tempRow.append("---")

#                 if datum is not None:
#                     tempRow.append(datum)
#                 else:
#                     tempRow.append('-')
#             writer.writerow(tempRow)

#         output.close()
print "Done with CSV Writer."