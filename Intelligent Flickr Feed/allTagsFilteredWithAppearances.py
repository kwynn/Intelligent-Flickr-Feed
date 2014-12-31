import flickr

inFile = open("allTags.txt", "r")
outFile = open("allTagsFilteredWithAppearances.txt","w")

# Initialize dict
tags = {}

# Iterate through each line
for line in inFile:
	#I terate through each word
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
	# Filter tags that only appear once
	if tags[key] > 1:
		outFile.write(key + "   ")
		outFile.write(str(tags[key]))
		outFile.write("\n")

print len(tags)
	
inFile.close()
outFile.close()