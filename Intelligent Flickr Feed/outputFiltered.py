# generates photo names and their associated
import flickr

dictionary = open("allTagsFiltered.txt", "r")
inFile = open("output.txt","r")
outFile = open("outputFiltered.txt","w")

# Initialize dict
tags = []

#Iterate through each word
for line in dictionary:
	for word in line.split():
		tags.append(word)

for line in inFile:
	for word in line.split():
		if word.endswith(".jpg:"):
			outFile.write("\n" + word + " ")
		else:
			if word in tags:
				outFile.write(word + " ")


dictionary.close()	
inFile.close()
outFile.close()