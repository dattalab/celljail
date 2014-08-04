from glob import glob
import tiffile
import pymorph
import os, sys
import imageIORoutines as io

try:
    datadir = sys.argv[1]
    print datadir
except:
    print "Missing arguments"
    datadir = "/Users/KeiMasuda/Desktop/internalCalciumMutagenesis/internalcalcium071114"

img_dir = os.path.join(datadir, '*')
print img_dir
files = glob(img_dir)
files = [file for file in files if 'LOG' not in file]
files = [file for file in files if 'TXT' not in file]
files = [file for file in files if 'INF' not in file]
files = [file for file in files if 'small' not in file]
files = [file for file in files if '.npz' not in file]

for file in files:
	print file
	try:
		temp = tiffile.imread(file)
		temp = io.downsample2d(temp, 3).astype('int16')
		outfile = file + '_small_x3'
		tiffile.imsave(outfile, temp)
	except:
		print "Downsample Failed:" + file
	print "done with: " + outfile

