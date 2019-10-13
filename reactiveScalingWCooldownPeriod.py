import math
with open('data.txt','r') as file_object:
	line = file_object.readline()
	#Init variables to store lines
	systemLoad = []
	while line:
		#Reading line and writing to list
		myList = line.split(" ") #To be changed
		systemLoad.append(myList[1]) #To be changed
		line = file_object.readline()

scaleUpThreshold = 0.80
scaleDownThreshold = 0.10
VNFAInstanceCapacity = 50 #Requests per second
#VNFBInstanceCapacity = 10 #Requests per second
VNFAScaleUp = scaleUpThreshold * VNFAInstanceCapacity
VNFAScaleDown = scaleDownThreshold * VNFAInstanceCapacity
#VNFBScaleUp = scaleUpThreshold * VNFBInstanceCapacity
#VNFBScaleDown = scaleDownThreshold * VNFBInstanceCapacity
VNFInstanceCreationDelay = 60 #Seconds
VNFInstanceDeletionDelay = 5 #seconds
i = 0
check = 0

numberOfInstances = 1;
defaultSystemLoad = systemLoad[:]
numberOfTimestamp = len(systemLoad)
instanceCreationTimevsNumber = [] 
instanceDeletionTimevsNumber = []
instances = []

while i < numberOfTimestamp-1:
	if float(systemLoad[i]) < VNFAScaleUp:
		#print("Load is less than 80%")
		i = i + 1
	if float(systemLoad[i]) > VNFAScaleDown:
		#print("Load is greater than 10%")
		i = i + 1
	if float(systemLoad[i]) > VNFAScaleUp:
		for x in range(1, 2):
			if float(systemLoad[i+x]) < VNFAScaleUp:
				check = 1
				break;
		if check == 0:
			print("New Instance Created")
			calcNumberOfInstance = math.ceil(((float(systemLoad[i+1]) + float(systemLoad[i+2]) + float(systemLoad[i+3])) / 3) / 80.00)
			numberOfInstances = numberOfInstances + calcNumberOfInstance
			systemLoad = defaultSystemLoad[:]
			#systemLoad = systemLoad / numberOfInstances
			systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
			print("Next load on " + str(numberOfInstances) + " VNF Instance(s) is " + str(systemLoad[i+1]))
			instanceCreationTimevsNumber.append(tuple((i, numberOfInstances)))
			for j in range(1, 60):
				instances.append(tuple((i+j, numberOfInstances)))
			i = i + VNFInstanceCreationDelay
	if float(systemLoad[i]) < VNFAScaleDown:
		print("Instance Deleted")
		numberOfInstances = numberOfInstances - 1
		systemLoad = defaultSystemLoad[:]
		#systemLoad = systemLoad / numberOfInstances
		systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
		print("Next load on " + str(numberOfInstances) + " VNF Instance(s) is " + str(systemLoad[i+1]))
		instanceDeletionTimevsNumber.append(tuple((i, numberOfInstances)))
		i = i + VNFInstanceDeletionDelay
	instances.append(tuple((i, numberOfInstances)))
	
print("Operation completed with " + str(numberOfInstances) + " instances!")
for a,b in instanceCreationTimevsNumber:
	print("Time " + str(a) + " instances " + str(b))
file = open('scaleuptimecool.txt','w')
for a,b in instances:
	file.write(str(a) + " " + str(b))
	file.write('\n')
