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
img_files = sorted(img_files)[:FRAMES]
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
import mahotas, pymorph
I_show = accum.copy()
#increase contrast
import ImageEnhance
I_contrast = pow(I_show.astype("uint16"), 3)
#find regional maxima
regionalMax = pymorph.regmax((I_contrast).astype("uint16"))
#find seeds and cell number
seeds,numCells = ndimage.label(regionalMax)
print numCells
#edge detection
T = mahotas.thresholding.otsu(I_contrast.astype("uint16"))
dist = ndimage.distance_transform_edt(I_contrast.astype("uint16") > T)
dist = dist.max() - dist
dist -= dist.min()
dist = dist/float(dist.ptp()) * 255
dist = dist.astype(np.uint8)
#watershed
I_mask = pymorph.cwatershed(dist, seeds)


frames, x, y = Is.shape
label_mask, num_cells = ndimage.label(I_mask.astype(bool))
print frames
print num_cells

traces = np.zeros((frames, num_cells))
baselined_traces = np.zeros_like(traces)
normed_traces = np.zeros_like(traces)
for cell in range(1,num_cells):
    traces[:,cell] = Is[:,label_mask==cell].mean(axis=1)
print "Found %d unique cells" % traces.shape[1]

print traces

# pdb.set_trace()
mixName = datadir.split('/')
saveMixName = '_'.join(mixName[-5:])
# saveFileName = os.path.join(datadir, saveMixName)
saveFileName = os.path.join("/home/fkm4/results/", saveMixName)
np.savez(saveFileName, traces=traces, baselined_traces=baselined_traces, normed_traces=normed_traces, label_mask=label_mask)
tiffile.imsave(saveFileName+'.tif', movie, compress=0)
print "saved " + saveFileName

# Use np.savez to save `traces` and `label_mask` and the mask out. 




