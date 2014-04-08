import os

pythonScript = "bsub -q short -W 240 -R 'rusage[mem=10000]' -R 'select[transfer]' python npz_loader.py "
# pythonScript = "bsub -q short -W 240 -R 'rusage[mem=10000]' -R 'select[transfer]' python npz_loader.py"
directory = "/home/fkm4/results"
# directory = "/Users/KeiMasuda/Desktop/2013DattaLab/Datta_Python/Results"
for filename in os.listdir(directory):
	print pythonScript + filename