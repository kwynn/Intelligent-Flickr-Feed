from random import randint
import flickr
import fileinput
import sys
import urllib
import webbrowser

INITIAL_WEIGHT = 10
INITIAL_LOW_WEIGHT = 5
INCREASE_LOW_WEIGHT = 3
INCREASE_HIGH_WEIGHT = 20
DECREASE_WEIGHT = 5
tagsAndWeights = {}
headerTags = []

outFile1 = open('filterResults.txt', 'w')
outFile2 = open('controlResults.txt', 'w')

# find how many lines are in a file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def numNumbers(word):
	count = 0
	for char in word:
		if char.isdigit():
			count+=1

	return count


# initialize all tags in tags.txt to weight of INITIAL_WEIGHT
def initializeWeights():
	initialFile = open("tags.txt","r")

	for line in initialFile:
		for word in line.split():
			tagsAndWeights[word.lower()] = INITIAL_WEIGHT
			headerTags.append(word.lower())

# generates and saves a new image and returns its tags
def generatePhotoAndTags(tag, count):
	random = randint(1,100)
	print "Random page number: " + str(random)
	tagList = []
	
	photoObjectList = flickr.photos_search(tags = tag, per_page = 1, page = random, content_type = 1)
	for photoObject in photoObjectList:
		url = "https://farm"+photoObject.farm+".staticflickr.com/"+photoObject.server+"/"+photoObject.id+"_"+photoObject.secret+".jpg"
		image_name = "test_"+str(count)+".jpg"
		print "Image name: " + image_name

		#save image
		urllib.urlretrieve(url, image_name)

		for t in photoObject.tags:
			t.strip('\'')
			t.lower()
			strTag = t.encode('ascii','ignore')
			if (len(strTag) > 2) and (numNumbers(strTag)<=4):
				tagList.append(strTag) 

		if len(tagList) <=20:
			webbrowser.open(url)

	#print tagList
	return tagList

# adds a tag to the tagsAndWeights dict with INITIAL_WEIGHT
def addTagToTagsAndWeights(tag, weight):
	if not "stagram" in tag:
		if not "insta" in tag:
			tagsAndWeights[tag] = weight
			print "added tag"

# for every tag in a tagList, increases the tag's weight in tagsAndWeights
# if the tag does not exist in tagsAndWeights, adds it and then increases its weight
def upweight(tagList):
	for tag in tagList:
		if tag in tagsAndWeights:
			if tag in headerTags:
				tagsAndWeights[tag] += INCREASE_HIGH_WEIGHT
			else:
				tagsAndWeights[tag] += INCREASE_LOW_WEIGHT
		else:
			addTagToTagsAndWeights(tag, INITIAL_LOW_WEIGHT)
	print "upweighted"

def upweightWithoutAdding(tagList):
	for tag in tagList:
		if tag in tagsAndWeights:
			if tag in headerTags:
				tagsAndWeights[tag] += INCREASE_HIGH_WEIGHT
			else:
				tagsAndWeights[tag] += INCREASE_LOW_WEIGHT
	print "upweighted without adding tag"

# for every tag in a tagList, decreases the tag's weight in tagsAndWeights
# if the tag does not exist in tagsAndWeights, nothing happens
# if the weight < 0 then remove the tag
def downweight(tagList):
	for tag in tagList:
		if tag in tagsAndWeights:
			tagsAndWeights[tag] -= DECREASE_WEIGHT
			if tagsAndWeights[tag] <= 0:
				del tagsAndWeights[tag]

	print "downweighted"

def getRandomTag():
	sumObj = 0
	finalTag = ""

	while (finalTag == ""):
		for tag in tagsAndWeights:
			sumObj += tagsAndWeights[tag]
		random = randint(1,sumObj)
		print "Random particle generator: " + str(random)

		tempSum = 0
		for tag in tagsAndWeights:
			tempSum += tagsAndWeights[tag]
			if tempSum<random:
				finalTag = tag


	print "Sum of particles: " + str(sumObj)
	print "Chosen tag: " + str(finalTag)
	return str(finalTag.lower())

# ----- MAIN ----- #
def probabilisticModel():
	sameSession = True
	initializeWeights()
	count = 1
	sampling = 1

	while(sameSession):
		tag = getRandomTag()

		#make sure fewer than 15 tags in photo
		while True:
			tempTagList = generatePhotoAndTags(tag, count)
			tagCounter = len(tempTagList)
			if tagCounter<=20 and tagCounter>0:
				break

		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			outFile1.close()
			break
		elif answer == "y":
			if sampling<10:
				upweightWithoutAdding(tempTagList)
				sampling+=1
				outFile1.write("y ")
			else:
				upweight(tempTagList)
				outFile1.write("y ")
		elif answer == "n":
			downweight(tempTagList)
			sampling+=1
			outFile1.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))

def randomModel():
	sameSession = True
	initializeWeights()
	count = 1
	sampling = 1

	while(sameSession):
		tag = getRandomTag()

		#make sure fewer than 20 tags in photo
		while True:
			tempTagList = generatePhotoAndTags(tag, count)
			tagCounter = len(tempTagList)
			if tagCounter<=20 and tagCounter>0:
				break

		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			outFile2.close()
			break
		elif answer == "y":
			if sampling<10:
				sampling+=1
				outFile2.write("y ")
			else:
				for tag in tempTagList:
					addTagToTagsAndWeights(tag, INCREASE_HIGH_WEIGHT)
				sampling+=1
				outFile2.write("y ")
		elif answer == "n":
			sampling+=1
			outFile2.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))
	# generate a random image, take in y/n input, and then reweight algorithm
	# fileLineLength = file_len("outputFiltered.txt")

#randomModel()
#probabilisticModel()