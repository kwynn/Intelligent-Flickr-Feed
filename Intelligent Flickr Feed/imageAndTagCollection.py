import flickr
import fileinput
import sys
import urllib

totalTagList = []
outputFile = open("output.txt","wt")
allTags = open("allTags.txt","wt")

# takes in an input file where there is a tag on each line
for tag in fileinput.input(sys.argv[1:]):
	tag = tag.rstrip('\n')
	print tag
	# does a request to flickr to pull images with the given tag
	count = 1
	for i in range(1,51,5):
		photoObjectList = flickr.photos_search('','',tag,'','','','','','','',1,i)

		# for each retrieved photoObject get the url
		# save the image out with the name image_name
		for photoObject in photoObjectList:
			url = "https://farm"+photoObject.farm+".staticflickr.com/"+photoObject.server+"/"+photoObject.id+"_"+photoObject.secret+".jpg"
			image_name = tag+"_"+str(count)+".jpg"

			outputFile.write(image_name+": ")
			
			#save image
			urllib.urlretrieve(url, image_name)

			# get tags and add to tagList
			tagList = [image_name]
			for t in photoObject.tags:
				t.strip('\'')
				strTag = t.encode('ascii','ignore')
				tagList.append(strTag)
				totalTagList.append(strTag)
				outputFile.write(strTag+" ")
				allTags.write(strTag+" ")
			#print tagList

			# INSERT WRITING OUT THE IMAGE_NAME AND TAG_LIST HERE

			outputFile.write("\n")

			count+=1

outputFile.close()
allTags.close()
#print len(remove_duplicates(totalTagList))
