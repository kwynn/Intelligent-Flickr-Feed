import sys

inFile = open('filterResults.txt', 'r')

# Initialize values
likeTotal = 0
imageTotal = 0
likes = 0
images = 0
list1 = []

# Iterate through each line
for line in inFile:
	#Iterate through each word
	for word in line.split(" "):
		imageTotal += 1
		if word == "y":
			likeTotal += 1
		if imageTotal > 10:
			images += 1
			if word == "y":
				likes += 1
			if images % 5 == 0:
				list1.append(float(likes)/float(images))

print "Percentage of likes: " + str(float(likeTotal)/float(imageTotal))
print "Percentage of likes over time: "
for val in list1:
	print val

print "Number of likes: " + str(likeTotal)
print "Number of images: " + str(imageTotal)
	
inFile.close()