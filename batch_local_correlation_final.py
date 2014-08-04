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
print "=========START CODE=========="

try:
    # args = [sys.argv[1], sys.argv[2]]
    datadir = sys.argv[1]
    cpu_number = int(sys.argv[2])
except:
    print "Missing args: local_correlation_method.py [path_to_images] [cpu_number]"
    datadir = "/Users/KeiMasuda/Desktop/2013DattaLab/Datta_Python/celljail/4c/mix7b/"
    cpu_number = 1

# Specify where the images are

img_dir = os.path.join(datadir, '*small*')
img_files = glob(img_dir)
img_files = sorted(img_files)
for i in img_files:
    print i.split("/")

# print img_files, img_dir
# Load in the images
# for i in img_files:
#     Isa = np.rollaxis(np.dstack(tiffile.imread(i)), 2, 0)
Is = np.rollaxis(np.dstack([tiffile.imread(i) for i in img_files]), 2, 0)
movie = Is
Is = Is[:,::2,::2].astype('float64')

# Calculate the maximum across all frames
accum = np.log(Is.max(axis=0))

import skimage.segmentation, skimage.feature, skimage.morphology.watershed
I = accum.copy()
# I = ndimage.grey_opening(I,(3,3))
maxes = skimage.feature.peak_local_max(I, min_distance=1, threshold_abs=5.2, indices=False)

I_show = accum.copy()

I_mask = ndimage.grey_dilation(maxes,(1,2)).astype('float32')
I_mask[I_mask == True] = I_show.max()*1.01
# imshow(I_show+I_mask, cmap='jet'); colorbar()

frames, x, y = Is.shape
label_mask, num_cells = ndimage.label(I_mask.astype(bool))
print frames
print num_cells

traces = np.zeros((frames, num_cells))

print traces.dtype
print Is.dtype

baselined_traces = np.zeros_like(traces)
normed_traces = np.zeros_like(traces)
for cell in range(1,num_cells):
    traces[:,cell] = Is[:,label_mask==cell].mean(axis=1)
    baselined_traces[:,cell] = traces[:,cell] - traces[:30,cell].mean()
    normed_traces[:,cell] = traces[:,cell] / traces[:30,cell].mean()
print "Found %d unique cells" % traces.shape[1]

print normed_traces

# pdb.set_trace()
mixName = datadir.split('/')
saveMixName = '_'.join(mixName[-5:])
# saveFileName = os.path.join(datadir, saveMixName)
saveFileName = os.path.join("/home/fkm4/results/", saveMixName)
np.savez(saveFileName, traces=traces, baselined_traces=baselined_traces, normed_traces=normed_traces, label_mask=label_mask)
tiffile.imsave(saveFileName+'.tif', movie, compress=0)
print "saved " + saveFileName

# Use np.savez to save `traces` and `label_mask` and the mask out. 




