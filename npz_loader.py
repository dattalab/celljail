# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import pdb
import sys
import numpy as np
import scipy.ndimage as ndimage
import skimage
import os
import tiffile
from glob import glob
from joblib import Parallel, delayed
from itertools import product
from pylab import *
import sys
sys.path.append('/home/fkm4/dattacode/')
import traces as tm
import imaging.segmentation as seg
from skimage.morphology import watershed, disk
from skimage import data
from skimage.filter import rank
from skimage.util import img_as_ubyte
from skimage import filter


FRAMES = 120
GRAPHSIZE = 120
FRAMEDELAY = 0
STIM_1_START = 30+FRAMEDELAY
STIM_1_END = 60+FRAMEDELAY
STIM_2_START = 0+FRAMEDELAY
STIM_2_END = 0+FRAMEDELAY


filename = sys.argv[1]
# data = np.load("/Users/KeiMasuda/Desktop/2013DattaLab/Datta_Python/Results/"+filename)
data = np.load("/home/fkm4/results/"+filename)

for key, value in data.iteritems():
    print key
    
traces = data["traces"]
label_mask = data["label_mask"]

num_cells = traces.shape[1]

# print traces
print "Found %d unique cells" % traces.shape[1]

#outfile directory setup
outfile_dir_parent = "/home/fkm4/results/analysis/"
os.makedirs(outfile_dir_parent + filename)
outfile_dir = outfile_dir_parent + filename+ "/"

#trace processing, splined baseline, and normalization
m = tm.mask_deviations(traces, 2.25)
bs = tm.baseline_splines(m, 5)
frame = 1.0/GRAPHSIZE;
normed_traces = (traces-bs)/bs

#================================
#save out images
figure(figsize=(15,3))
title = filename[:-5] + "_Raw Traces"
suptitle(title)
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_1_START, frame*STIM_1_END, alpha=0.25);
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_2_START, frame*STIM_2_END, alpha=0.25);
plot(traces);
savefig(outfile_dir+title+".png")

figure(figsize=(15,3))
title = filename[:-5]+"_baselines"
suptitle(title)
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_1_START, frame*STIM_1_END, alpha=0.25);
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_2_START, frame*STIM_2_END, alpha=0.25);
plot(bs);
savefig(outfile_dir+title+".png")


figure(figsize=(15,3))
title = filename[:-5]+"_Normalized"
suptitle(title)
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_1_START, frame*STIM_1_END, alpha=0.25);
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_2_START, frame*STIM_2_END, alpha=0.25);
plot(normed_traces);
savefig(outfile_dir+title+".png")

#smoothed normed traces
figure(figsize=(15,3))
title = filename[:-5]+"_Smoothed"
suptitle(title)
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_1_START, frame*STIM_1_END, alpha=0.25);
axhspan(normed_traces.min(), normed_traces.max(),frame*STIM_2_START, frame*STIM_2_END, alpha=0.25);
for cell in range(1,num_cells):
    _ = plot(tm.smooth(normed_traces[:,cell], window_len=11, window='flat'))
savefig(outfile_dir+title+".png")

figure(figsize=(20,20))
title = filename[:-5]+"_Image Mask"
suptitle(title)
imshow(label_mask)
savefig(outfile_dir+title+".png")

# num_cells = traces.shape[1]
# base_range1 = slice(5,30) #range for baseline
# stds = traces[base_range1,:].std(axis=0)
# means = traces[base_range1,:].mean(axis=0)
# cutoffs_5 = means + 5*stds #here set number of stdvs above mean you want to call responses
# cutoffs_20 = means + 20*stds
# cutoffs_50 = means + 50*stds



# responders_5 = []
# responders_20 = []
# responders_50 = []
# for i, trace in enumerate(np.rollaxis(traces, 1, 0)):
#     over_5 = np.argwhere(trace[30:90]>cutoffs_5[i]).flatten() #range of where I want to restrict the responses
#     over_20 = np.argwhere(trace[30:90]>cutoffs_20[i]).flatten() 
#     over_50 = np.argwhere(trace[30:90]>cutoffs_50[i]).flatten() 
#     if np.any(over_5):
#         responders_5.append(i)
#     if np.any(over_20):
#         responders_20.append(i)
#     if np.any(over_50):
#         responders_50.append(i)



# print "Total Cells: " + str(num_cells) + "\n"
# print "Number of 5 std: " + str(len(responders_5))
# print "5 std cells: " + str(responders_5)+ "\n"
# print "Number of 20 std: " + str(len(responders_20))
# print "20 std cells: " + str(responders_20)+ "\n"
# print "Number of 50 std: " + str(len(responders_50))
# print "50 std cells: " + str(responders_50)



# figure()
# if len(responders_5) > 0:
#     plot(traces[:,np.array(responders_5)]/means[np.array(responders_5)])
# title = filename[:-5]+"_responders_5std"
# suptitle(title)
# savefig(outfile_dir+title+".png")



# figure()
# if len(responders_20) > 0:
#     plot(traces[:,np.array(responders_20)]/means[np.array(responders_20)])
# title = filename[:-5]+"_responders_20std"
# suptitle(title)
# savefig(outfile_dir+title+".png")



# figure()
# if len(responders_50) > 0:
#     plot(traces[:,np.array(responders_50)]/means[np.array(responders_50)])
# title = filename[:-5]+"_responders_50std"
# suptitle(title)
# savefig(outfile_dir+title+".png")


# if not np.array(responders_5).any():
#     max_traces_5 = []
#     print max_traces_5
#     print max_traces_5
# else:
#     response_traces_5 = traces[30:90,np.array(responders_5)]/means[np.array(responders_5)]
#     num_traces_5 = response_traces_5.shape[1]
#     max_traces_5 = []
#     for i in range(num_traces_5):
#         max_traces_5.append(max(trace[i] for trace in response_traces_5))
#     print max_traces_5
#     print mean(max_traces_5)


# if not np.array(responders_20).any():
#     max_traces_20 = []
#     print max_traces_20
#     print max_traces_20
# else:
#     response_traces_20 = traces[30:90,np.array(responders_20)]/means[np.array(responders_20)]
#     num_traces_20 = response_traces_20.shape[1]
#     max_traces_20 = []
#     for i in range(num_traces_20):
#         max_traces_20.append(max(trace[i] for trace in response_traces_20))
#     print max_traces_20
#     print mean(max_traces_20)

# if not np.array(responders_50).any():
#     max_traces_50 = []
#     print max_traces_50
#     print max_traces_50
# else:
#     response_traces_50 = traces[30:90,np.array(responders_50)]/means[np.array(responders_50)]
#     num_traces_50 = response_traces_50.shape[1]
#     max_traces_50 = []
#     for i in range(num_traces_50):
#         max_traces_50.append(max(trace[i] for trace in response_traces_50))
#     print max_traces_50
#     print mean(max_traces_50)


# #====================OUTFILE==================
# #====================OUTFILE==================

# #calculate deltaF/f
# dff_traces = np.zeros_like(traces)
# for cell in range(num_cells):
#     dff_traces[:,cell] = (traces[:,cell]-traces[:30,cell].mean()) / traces[:30,cell].mean()

# #plot deltaF/F
# figure(figsize=(15,3))
# title = filename[:-5] + "_deltaFF"
# suptitle(title)
# plot(dff_traces);
# savefig(outfile_dir+title+".png")

# mean_dff = {}
# for cell in range(len(dff_traces)):
#     if not np.array(dff_traces[cell, 45:90]).any():
#         mean_dff = {}
#     else:
#         mean_dff["Cell #"+str(cell)]= mean(dff_traces[cell, 45:90])
# max_dff = {}
# for cell in range(len(dff_traces)):
#     if not np.array(dff_traces[cell, 45:90]).any():
#         max_dff = {}
#     else:
#         max_dff["Cell #"+str(cell)]= max(dff_traces[cell, 45:90])


# sorted_mean_dff = sorted(mean_dff.items(), key=lambda x:x[1], reverse=True)
# for i in range(len(sorted_mean_dff)):
#     print sorted_mean_dff[i]
# sorted_max_dff = sorted(max_dff.items(), key=lambda x:x[1], reverse=True)
# for i in range(len(sorted_max_dff)):
#     print sorted_max_dff[i]


# def topPercentileMean(percent, mean_dff):
#     num_cells = len(mean_dff)
#     returnCellsCutOff = int(round(percent*num_cells))
#     cutOffValues = sorted(mean_dff.values(), reverse=True)
#     return mean(cutOffValues[:returnCellsCutOff])

# def topPercentileMax(percent, max_dff):
#     num_cells = len(max_dff)
#     returnCellsCutOff = int(round(percent*num_cells))
#     cutOffValues = sorted(max_dff.values(), reverse=True)
#     return mean(cutOffValues[:returnCellsCutOff])


# mean_10 = topPercentileMean(0.1, mean_dff)
# print "Top 10% df/f mean:" + str(mean_10)
# mean_25 = topPercentileMean(0.25, mean_dff)
# print "Top 25% df/f mean:" + str(mean_25)
# mean_100 = topPercentileMean(1, mean_dff)
# print "Top 100% df/f mean:" + str(mean_100)
# print ""
# max_10 = topPercentileMean(0.1, max_dff)
# print "Top 10% df/f mean of max:" + str(max_10)
# max_25 = topPercentileMean(0.25, max_dff)
# print "Top 25% df/f mean of max:" + str(max_25)
# max_100 = topPercentileMean(1, max_dff)
# print "Top 100% df/f mean of max:" + str(max_100)



# #====================OUTFILE==================
# #====================OUTFILE==================
# #====================OUTFILE==================

# outfile = outfile_dir+filename[:-4] + ".txt"

# f = open(outfile, "w")
# f.write(outfile+"\n")
# f.write("Total Cells: " + str(num_cells) + "\n"+ "\n")
# f.write("Number of 5 std: " + str(len(responders_5))+ "\n")
# f.write("5 std cells: " + str(responders_5)+ "\n"+ "\n")
# f.write("Number of 20 std: " + str(len(responders_20))+ "\n")
# f.write("20 std cells: " + str(responders_20)+ "\n"+ "\n")
# f.write("Number of 50 std: " + str(len(responders_50))+ "\n")
# f.write("50 std cells: " + str(responders_50)+ "\n"+ "\n")
# # f.write("Max Normalized response values for 5 std: " + str((max_traces_5)+ "\n")
# # f.write("Average Normalized Max Response for 5 std: " + str(mean(max_traces_5)+ "\n"+ "\n")
# # f.write("Max Normalized response values for 20 std: " + str((max_traces_20)+ "\n")
# # f.write("Average Normalized Max Response for 20 std: " + str(mean(max_traces_20))+ "\n"+ "\n")
# # f.write("Max Normalized response values for 50 std: " + str((max_traces_50)+ "\n")
# # f.write("Average Normalized Max Response for 50 std: " + str((mean(max_traces_50)+ "\n"+ "\n")
# f.write("Top 10%% df/f mean:" + str(mean_10)+ "\n")
# f.write("Top 25%% df/f mean:" + str(mean_25)+ "\n"+ "\n")
# f.write("Top 10%% df/f mean of max:" + str(max_10)+ "\n")
# f.write("Top 25%% df/f mean of max:" + str(max_25)+ "\n")
# f.write("Top 100%% df/f mean of max:" + str(max_100)+ "\n"+ "\n")
# f.write("Sorted Mean DeltaF/F per Cell:"+ "\n")
# for i in range(len(sorted_mean_dff)):
#     f.write(str(sorted_mean_dff[i])+ "\n")
# f.write("Sorted Max DeltaF/F per Cell:"+ "\n")
# for i in range(len(sorted_max_dff)):
#     f.write(str(sorted_max_dff[i])+ "\n")
# f.close()







