import sys

inFile = open('filterResults.txt', 'r')

# Initialize values
likes1 = 0
total1 = 0
list1 = []

# Iterate through each line
for line in inFile:
	#Iterate through each word
	for word in line.split(" "):
		total1 += 1
		if word == "y":
			likes1 += 1
		if total1 % 5 == 0:
			list1.append(float(likes1)/float(total1))

print "Percentage of likes: " + str(float(likes1)/float(total1))
"Percentage of likes over time: "
for val in list1:
	print val

print "Number of likes: " + str(likes1)
print "Number of images: " + str(total1)
	
inFile.close()