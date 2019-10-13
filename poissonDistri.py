import math
import subprocess
with open('predict2.txt','r') as file_object:
	line = file_object.readline()
	#Init variables to store lines
	systemLoad = []
	data = []
	while line:
		#Reading line and writing to list
		myList = line.split(" ") #To be changed
		systemLoad.append(myList[1]) #To be changed
		#------------------------------------------
		subprocess.call(["g++", "poissonDistri.cpp"])
		tmp=subprocess.call("./a.out " + myList[1], shell=True)
		
		with open('distributedData.txt', 'r') as obj:
			linex = obj.readline()
			while linex:
				data.append(linex)
				linex = obj.readline()
		#------------------------------------------
		line = file_object.readline()
print("Printing the data")
for a in data:
	print(str(a))
file = open('finaldata.txt','w')
for a in data:
	file.write(str(a))
	file.write('\n')
