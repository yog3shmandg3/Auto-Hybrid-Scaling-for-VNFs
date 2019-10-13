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
		
VNFInstanceCapacity = 50 #Requests per second
defaultVNFInstanceCapacity = 50 #Requests per second
horizontalVNFInstanceCreationDelay = 60 #Seconds
horizontalVNFInstanceDeletionDelay = 5 #Seconds
verticalVNFInstanceUpDelay = 0.05 #Seconds
verticalVNFInstanceDownDelay = 0.01 #Seconds
VNFInstanceCapacityFraction = VNFInstanceCapacity / 10

scaleUpThreshold = 0.80
scaleUpThreshold_V = 0.80
scaleDownThreshold = 0.30
VNFScaleUp = scaleUpThreshold * VNFInstanceCapacity
VNFScaleUp_V = scaleUpThreshold_V * VNFInstanceCapacity
VNFScaleDown = scaleDownThreshold * VNFInstanceCapacity

numberOfInstances = 1
numberOfTimestamp = len(systemLoad)
defaultSystemLoad = systemLoad[:]
i = 0
j = 0
k = 0

instances = []
resources = []

while i < numberOfTimestamp-1:
	if i == 0:
		if float(systemLoad[i]) > VNFScaleUp:
			print("Scale Out at i!")
			calcNumberOfInstance = math.ceil(float(systemLoad[i]) / 80.00)
			numberOfInstances = numberOfInstances + calcNumberOfInstance
			systemLoad = defaultSystemLoad[:]
			systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
			print("Number of instances " + str(numberOfInstances) + "\n")
	if j == 20 and i < 19980: #Condition to be checked and updated later	
		if float(systemLoad[i+20]) > VNFScaleUp:
				print("Scale Out at i+10!")
				calcNumberOfInstance = math.ceil(float(systemLoad[i+20]) / 80.00)
				numberOfInstances = numberOfInstances + calcNumberOfInstance
				systemLoad = defaultSystemLoad[:]
				systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
				print("Number of instances " + str(numberOfInstances) + "\n")
				
		if float(systemLoad[i+20]) < VNFScaleDown:
				print("Scale In at i+10!")
				numberOfInstances = numberOfInstances - 1
				systemLoad = defaultSystemLoad[:]
				systemLoad[:] = [float(x) / numberOfInstances for x in systemLoad]
				print("Number of instances " + str(numberOfInstances) + "\n")

		j = 0
	
	if k >= 0:
		if float(systemLoad[i+1]) > VNFScaleUp_V:
			print("Scale Up at i+1!")
			VNFInstanceCapacity = VNFInstanceCapacity + defaultVNFInstanceCapacity
			VNFScaleUp = scaleUpThreshold * VNFInstanceCapacity
			VNFScaleDown = scaleDownThreshold * VNFInstanceCapacity
		if float(systemLoad[i+1]) < VNFScaleUp:
			print("Scale Down at i+1!")
			VNFInstanceCapacity = defaultVNFInstanceCapacity
			VNFScaleUp = scaleUpThreshold * VNFInstanceCapacity
			VNFScaleDown = scaleDownThreshold * VNFInstanceCapacity
		k = 0
	instances.append(tuple((i, numberOfInstances)))
	resources.append(tuple((i, VNFInstanceCapacity * numberOfInstances)))
	i = i + 1
	j = j + 1
	k = k + 1

print("Operation completed with " + str(numberOfInstances) + " instances!")
file = open('proposedInstances_4.txt','w')
for a,b in instances:
	file.write(str(a) + " " + str(b))
	file.write('\n')
file = open('proposedResources.txt','w')
for a,b in resources:
	file.write(str(a) + " " + str(b))
	file.write('\n')
