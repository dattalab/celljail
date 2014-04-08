import os

def listdir_nohidden(searchList):
    for s in searchList:
    	print s
        if not s.startswith('.' or '/' or 'd'):
            return s

pythonScript = "bsub -q short -W 240 -R 'rusage[mem=10000]' -R 'select[transfer]' python batch_local_correlation_final.py"
# directory = "/Volumes/DattaLab/Paul/screendataforkei"
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
								print pythonScript+' '+orchestraDirectory+'/'+bigDirectory+'/'+screenDay+'/'+ms4+'/'+mix+'/ '+'12'
	# for screenDay in os.listdir(listdir_nohidden(bigDirectory)):
	# 	print screenDay
	# 	for mix in os.listdir(listdir_nohidden(screenDay)):
	# 		print pythonScript+" "+directory+folder+"/"+mix+"/ "+"12"

# folders = ["4B", "4C", "4D", "5", "6c", "6d", "7", "8a","cd20", "mcherry", "combo"]
# mixes = ["mix6a", "mix7b", "mix8a", "mix9a"]
# for folder in folders:
# 	for mix in mixes:
# 		print pythonScript+" "+directory+folder+"/"+mix+"/ "+"12"

