import os

def listdir_nohidden(searchList):
    for s in searchList:
    	print s
        if not s.startswith('.' or '/' or 'd'):
            return s

pythonScript = "bsub -q short -W 60 -R 'rusage[mem=10000]' -R 'select[transfer]' python downsize.py"
directory = "/files/Neurobio/DattaLab/Paul/screendataforkei"
orchestraDirectory = "/files/Neurobio/DattaLab/Paul/screendataforkei"
for bigDirectory in os.listdir(directory):
	if not bigDirectory.startswith('.'):
		for screenDay in os.listdir(directory+'/'+bigDirectory):
			if not screenDay.startswith('.'):
				for ms4 in os.listdir(directory+'/'+bigDirectory+'/'+screenDay):
					if not ms4.startswith('.'):
						for mix in os.listdir(directory+'/'+bigDirectory+'/'+screenDay+'/'+ms4):
							if not mix.startswith('.'):
								print pythonScript+' '+orchestraDirectory+'/'+bigDirectory+'/'+screenDay+'/'+ms4+'/'+mix+'/'


