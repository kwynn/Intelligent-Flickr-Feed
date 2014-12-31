import flickr

inFile = open("allTags.txt", "r")
outFile = open("allTagsFiltered.txt","w")

# Initialize dict
tags = {}

# Iterate through each line
for line in inFile:
	#Iterate through each word
	for word in line.split():
		if len(word) > 2:
			# If an entry for a word has been recorded, increment the value
			if word in tags:
				tags[word] += 1
			# If an entry for a word has not been recorded, initialize it to 1
			else:
				tags[word] = 1

for key in tags.iterkeys():
	info = []
	# Filter tags that appear only once
	if tags[key] > 1:
		outFile.write(key + " ")

print len(tags)
	
inFile.close()
outFile.close()