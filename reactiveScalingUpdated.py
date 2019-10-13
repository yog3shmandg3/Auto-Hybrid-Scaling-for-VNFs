import math
with open('_data.txt','r') as file_object:
	line = file_object.readline()
	#Init variables to store lines
	systemLoad = []
	while line:
		#Reading line and writing to list
		myList = line.split(" ") #To be changed
		systemLoad.append(myList[1]) #To be changed
		line = file_object.readline()

scaleUpThreshold = 0.80
scaleDownThreshold = 0.20
VNFAInstanceCapacity = 50 #Requests per second
#VNFBInstanceCapacity = 10 #Requests per second
VNFAScaleUp = scaleUpThreshold * VNFAInstanceCapacity
VNFAScaleDown = scaleDownThreshold * VNFAInstanceCapacity
#VNFBScaleUp = scaleUpThreshold * VNFBInstanceCapacity
#VNFBScaleDown = scaleDownThreshold * VNFBInstanceCapacity
VNFInstanceCreationDelay = 60 #Seconds
VNFInstanceDeletionDelay = 5  #seconds
i = 0

numberOfInstances = 1;
defaultSystemLoad = systemLoad[:]
numberOfTimestamp = len(systemLoad)
instanceCreationTimevsNumber = [] 
instanceDeletionTimevsNumber = []
instances = []
resources = []
requests = []

while i < numberOfTimestamp-1:
	if i < 19990:
		if float(systemLoad[i]) < VNFAScaleUp:
			#print("Load is less than 80%")
			i = i + 1
		if float(systemLoad[i]) > VNFAScaleDown:
			#print("Load is greater than 10%")
			i = i + 1
		if float(systemLoad[i]) > VNFAScaleUp:
			print("New Instance Created")
			calcNumberOfInstance = math.ceil(float(systemLoad[i+1]) / 80.00)
			numberOfInstances = numberOfInstances + calcNumberOfInstance
			systemLoad = defaultSystemLoad[:]
			#systemLoad = systemLoad / numberOfInstances
			systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
			print("Next load on " + str(numberOfInstances) + " VNF Instance(s) is " + str(systemLoad[i+1]))
			instanceCreationTimevsNumber.append(tuple((i, numberOfInstances)))
			for j in range(1, 60):
				instances.append(tuple((i+j, numberOfInstances)))
				requests.append(tuple((i+j, systemLoad[i+j])))
				resources.append(tuple((i, VNFAInstanceCapacity * numberOfInstances)))
			i = i + VNFInstanceCreationDelay
		if float(systemLoad[i]) < VNFAScaleDown:
			print("Instance Deleted")
			numberOfInstances = numberOfInstances - 1
			if numberOfInstances < 1:
				numberOfInstances = 1
			systemLoad = defaultSystemLoad[:]
			#systemLoad = systemLoad / numberOfInstances
			systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
			print("Next load on " + str(numberOfInstances) + " VNF Instance(s) is " + str(systemLoad[i+1]))
			instanceDeletionTimevsNumber.append(tuple((i, numberOfInstances)))
			i = i + VNFInstanceDeletionDelay
			for j in range(1, 5):
				requests.append(tuple((i+j, systemLoad[i+j])))
		resources.append(tuple((i, VNFAInstanceCapacity * numberOfInstances)))
		instances.append(tuple((i, numberOfInstances)))
		if float(systemLoad[i]) - VNFAInstanceCapacity > 0:
			requests.append(tuple((i, float(systemLoad[i])-VNFAInstanceCapacity)))
		else:
			requests.append(tuple((i, "0")))
		print(i)
	else:
		break
print("Operation completed with " + str(numberOfInstances) + " instances!")
for a,b in instanceCreationTimevsNumber:
	print("Time " + str(a) + " instances " + str(b))
file = open('scaleuptime.txt','w')
for a,b in instances:
	file.write(str(a) + " " + str(b))
	file.write('\n')
file = open('resources.txt', 'w')
for a,b in resources:
	file.write(str(a) + " " + str(b))
	file.write('\n')
file = open('blockedrequests.txt', 'w')
for a,b in requests:
	file.write(str(a) + " " + str(b))
	file.write('\n')
