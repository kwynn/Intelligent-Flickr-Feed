from random import randint
import flickr
import fileinput
import sys
import urllib
import webbrowser

INITIAL_WEIGHT = 10
INITIAL_LOW_WEIGHT = 2
INCREASE_LOW_WEIGHT = 2
INCREASE_HIGH_WEIGHT = 10
DECREASE_WEIGHT = 10
MULTIPLY_FACTOR_HIGH = 3
MULTIPLY_FACTOR_LOW = 2
DIVIDE_FACTOR = 2
WEIGHT_THRESHOLD = 1500
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
	"""random = randint(1,100)
	print "Random page number: " + str(random)
	tagList = []
	
	photoObjectList = flickr.photos_search(tags = tag, per_page = 1, page = random, content_type = 1)
	photoObject = photoObjectList[0]
	url = "https://farm"+photoObject.farm+".staticflickr.com/"+photoObject.server+"/"+photoObject.id+"_"+photoObject.secret+".jpg"
	image_name = "test_"+str(count)+".jpg"
	print "Image name: " + image_name

	#save image
	#urllib.urlretrieve(url, image_name)

	#get the tags and make them ascii compatible
	for t in photoObject.tags:
		t.strip('\'')
		t.lower()
		strTag = t.encode('ascii','ignore')
		if (len(strTag) > 2) and (numNumbers(strTag)<=4):
			tagList.append(strTag) 

	webbrowser.open(url)

	#print tagList
	return tagList"""

	random = randint(1,100)
	print "Random page number: " + str(random)
	tagList = []

	favoriteCount = 0
	#relatedTags = getRelatedTags

	photoObjectList = flickr.photos_search(tags = tag, per_page = 10, page = random, content_type = 1)
	finalPhotoObject = photoObjectList[0]
	for photoObject in photoObjectList:
		#get photo with highest favorite count
		photoObjectFavoriteCount = photoObject.getFavoriteCount()
		if (photoObjectFavoriteCount > favoriteCount):
			favoriteCount = photoObjectFavoriteCount
			finalPhotoObject = photoObject
	
		#get photo with highest consistency count
		#comparePhotosTagsAndRelatedTags(photoObject.)

	url = "https://farm"+finalPhotoObject.farm+".staticflickr.com/"+finalPhotoObject.server+"/"+finalPhotoObject.id+"_"+finalPhotoObject.secret+".jpg"
	#url = finalPhotoObject.getDirectURL()
		#get the tags and make them ascii compatible
	for t in finalPhotoObject.tags:
		t.strip('\'')
		t.lower()
		strTag = t.encode('ascii','ignore')
		if (len(strTag) > 2) and (numNumbers(strTag)<=4):
			tagList.append(strTag)

	webbrowser.open(url)

	print "Final favorite count: " + str(favoriteCount)
	return tagList

# get a tag's related tags
def getRelatedTags(tag):
	initial = flickr.tags_getrelated(tag)
	tagList = []

	for t in initial:
		t.lower()
		t.strip('\'')
		strTag = t.encode('ascii','ignore')
		if (len(strTag) > 2) and (numNumbers(strTag)<=4):
			tagList.append(strTag) 

	#print tagList
	return tagList

# adds a tag to the tagsAndWeights dict with INITIAL_WEIGHT
def addTagToTagsAndWeights(tag, weight):
	if not "stagram" in tag:
		if not "insta" in tag:
			tagsAndWeights[tag] = weight
			print "added tag"

def addListOfTags(tagList, weight):
	for tag in tagList:
		if tag not in tagsAndWeights:
			addTagToTagsAndWeights(tag, weight)

# for every tag in a tagList, increases the tag's weight in tagsAndWeights
def upweight(tagList):
	for tag in tagList:
		#check if the tag is in tagsAndWeights
		if tag in tagsAndWeights:
			# then check if the tag is one of the main 40 and multiply it by a low factor
			if tag in headerTags:
				if tagsAndWeights[tag] * MULTIPLY_FACTOR_LOW > WEIGHT_THRESHOLD:
					tagsAndWeights[tag] = WEIGHT_THRESHOLD
				else:
					tagsAndWeights[tag] *= MULTIPLY_FACTOR_LOW
			#else if the tag is not in one of the main 40, then multiply it by a high factor
			else:
				if tagsAndWeights[tag] * MULTIPLY_FACTOR_HIGH > WEIGHT_THRESHOLD:
					tagsAndWeights[tag] = WEIGHT_THRESHOLD
				else:
					tagsAndWeights[tag] *= MULTIPLY_FACTOR_HIGH

		# if the tag does not exist in tagsAndWeights, adds it with an initial low weight
		else:
			addTagToTagsAndWeights(tag, INITIAL_LOW_WEIGHT)
	print "upweighted"

# for ever tag in a tagList, increases the tag's weight in tagsAndWeights.
# if a tag does not exist, do not add the tag
def upweightWithoutAdding(tagList):
	for tag in tagList:
		if tag in tagsAndWeights:
			if tag in headerTags:
				if tagsAndWeights[tag] * MULTIPLY_FACTOR_LOW > WEIGHT_THRESHOLD:
					tagsAndWeights[tag] = WEIGHT_THRESHOLD
				else:
					tagsAndWeights[tag] *= MULTIPLY_FACTOR_LOW
			else:
				if tagsAndWeights[tag] * MULTIPLY_FACTOR_HIGH > WEIGHT_THRESHOLD:
					tagsAndWeights[tag] = WEIGHT_THRESHOLD
				else:
					tagsAndWeights[tag] *= MULTIPLY_FACTOR_HIGH
	print "upweighted without adding tag"

# for every tag in a tagList, decreases the tag's weight in tagsAndWeights
# if the tag does not exist in tagsAndWeights, nothing happens
# if the weight < 0 then remove the tag
def downweight(tagList):
	for tag in tagList:
		if tag in tagsAndWeights:
			tagsAndWeights[tag] /= DIVIDE_FACTOR
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
		tagVal = 0

		while(tagVal < 10):
			tag = getRandomTag()
			tagVal = tagsAndWeights[tag]

		additionalTagList = generatePhotoAndTags(tag, count)
		relatedTagList = getRelatedTags(tag)
		
		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			outFile1.close()
			break
		elif answer == "y":
			#if still training, do not add extra tags
			if sampling<10:
				upweightWithoutAdding(additionalTagList)
				sampling+=1
				outFile1.write("y ")
			#else upweight and add extra tags
			else:
				upweightWithoutAdding(additionalTagList)
				upweight(relatedTagList)
				outFile1.write("y ")
		elif answer == "n":
			#downweight the photos tags
			downweight(additionalTagList)
			#downweight all related tags if they are in tagsAndWeights
			downweight(relatedTagList)
			sampling+=1
			outFile1.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))

#upweight no adding model
def upweightModel():
	sameSession = True
	initializeWeights()
	count = 1
	sampling = 1

	while(sameSession):
		tagVal = 0

		while(tagVal < 10):
			tag = getRandomTag()
			tagVal = tagsAndWeights[tag]

		additionalTagList = generatePhotoAndTags(tag, count)
		relatedTagList = getRelatedTags(tag)
		
		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			outFile1.close()
			break
		elif answer == "y":
			#if still training, do not add extra tags
			if sampling<10:
				upweightWithoutAdding(additionalTagList)
				sampling+=1
				outFile1.write("y ")
			#else upweight and add extra tags
			else:
				upweightWithoutAdding(additionalTagList)
				upweightWithoutAdding(relatedTagList)
				outFile1.write("y ")
		elif answer == "n":
			#downweight the photos tags
			downweight(additionalTagList)
			#downweight all related tags if they are in tagsAndWeights
			downweight(relatedTagList)
			sampling+=1
			outFile1.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))

#no upweighting but adding model
def addingModel():
	sameSession = True
	initializeWeights()
	count = 1
	sampling = 1

	while(sameSession):
		tag = getRandomTag()
			
		additionalTagList = generatePhotoAndTags(tag, count)
		relatedTagList = getRelatedTags(tag)
		
		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			outFile1.close()
			break
		elif answer == "y":
			#if still training, do not add extra tags
			if sampling<10:
				sampling+=1
				outFile1.write("y ")
			#else upweight and add extra tags
			else:
				addListOfTags(relatedTagList, INITIAL_LOW_WEIGHT)
				outFile1.write("y ")
		elif answer == "n":
			sampling+=1
			outFile1.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))

def nullControlModel():
	sameSession = True
	initializeWeights()
	count = 1
	sampling = 1

	while(sameSession):
		tag = getRandomTag()
		
		additionalTagList = generatePhotoAndTags(tag, count)
		
		answer = raw_input('Do you like or dislike this photo? y/n or q to quit ')

		if answer == "q":
			sameSession == False
			outFile1.close()
			break
		elif answer == "y":
			if sampling<10:
				sampling+=1
				outFile1.write("y ")
			#else upweight and add extra tags
			else:
				outFile1.write("y ")
		elif answer == "n":
			sampling+=1
			outFile1.write("n ")
		else:
			print "Error; input not recorded for this image"
		
		count += 1
		print "Image #" + str(count)

	print "tag - weight"
	for key in tagsAndWeights.iterkeys():
		print key + " - " + (str(tagsAndWeights[key]))

#probabilisticModel()
#upweightModel()
#addingModel()
nullControlModel()
#getRelatedTags("cat")