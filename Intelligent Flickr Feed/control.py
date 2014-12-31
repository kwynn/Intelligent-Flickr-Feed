from random import randint
import flickr
import fileinput
import sys
import urllib
import webbrowser

INITIAL_WEIGHT = 100
INITIAL_LOW_WEIGHT = 20
INCREASE_LOW_WEIGHT = 20
INCREASE_HIGH_WEIGHT = 75
DECREASE_WEIGHT = 50
tagsAndWeights = {}

headerTags = []

outFile = open("controlResults.txt", "w")

# find how many lines are in a file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

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
	tagList = []
	
	photoObjectList = flickr.photos_search('','',tag,'','','','','','','',1,random)
	for photoObject in photoObjectList:
		url = "https://farm"+photoObject.farm+".staticflickr.com/"+photoObject.server+"/"+photoObject.id+"_"+photoObject.secret+".jpg"
		webbrowser.open(url)
		"""image_name = "test_"+str(count)+".jpg"
		print "Image name: " + image_name

		#save image
		urllib.urlretrieve(url, image_name)"""

		for t in photoObject.tags:
			t.strip('\'')
			t.lower()
			strTag = t.encode('ascii','ignore')
			if len(strTag) > 2:
				tagList.append(strTag)

	#print tagList
	return tagList

# adds a tag to the tagsAndWeights dict with INITIAL_WEIGHT
def addTagToTagsAndWeights(tag):
	if not "stagram" in tag:
		if not "insta" in tag:
			tagsAndWeights[tag] = INITIAL_LOW_WEIGHT
			#print "added tag"

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
			addTagToTagsAndWeights(tag)
			tagsAndWeights[tag] += INCREASE_LOW_WEIGHT

	print "upweighted"

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
	return finalTag.lower()

# ----- MAIN ----- #

def start():
	sameSession = True
	initializeWeights()
	count = 1

	while(sameSession):
		tag = getRandomTag()

		tempTagList = generatePhotoAndTags(tag, count)

		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			break
		elif answer == "y":
			#upweight(tempTagList)
			outFile.write("y ")
		elif answer == "n":
			#downweight(tempTagList)
			outFile.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))

outFile.close()

# generate a random image, take in y/n input, and then reweight algorithm
# fileLineLength = file_len("outputFiltered.txt")