import os

pythonScript = "bsub -q short -W 240 -R 'rusage[mem=10000]' -R 'select[transfer]' python npz_loader.py "
directory = "/home/fkm4/results"
# directory = "/Users/KeiMasuda/Desktop/2013DattaLab/Datta_Python/Results"
# directory = "/Volumes/Neurobio/DattaLab/Kei/OdorScreen_NPZ_04082014"
for filename in os.listdir(directory):
	if '.npz' in filename:
		print pythonScript + filename