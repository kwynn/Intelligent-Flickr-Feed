import os, sys
import flickr
import webbrowser
import algo
import control
from random import randint
from Tkinter import *
from PIL import Image, ImageTk

def runFilter():
	print "\n"
	print "Running Particle Filter"
	try:
		algo.probabilisticModel()
	except:
		print "Unable to run Particle Filter"

def runControl():
	print "\n"
	print "Running Control Test"
	try:
		algo.randomModel()
	except:
		print "Unable to run Control Test"

def displayImage():
	canvas = Canvas(root)
	canvas.grid(row = 0, column = 0)
	photo = ImageTk.PhotoImage(file = 'Winter_1.jpg')
	canvas.create_image(0,0, image=photo)

def likeImage():
	sys.stdout.write("y")
	#print "y"
	#return "y"

def dislikeImage():
	sys.stdout.write("n")
	#print "n"
	#return "n"

# create window
root = Tk()
root.wm_attributes("-topmost", 1)

# settings
root.title("Intelligent Flickr Feed")
root.geometry("400x100")

app = Frame(root)
app.grid()

#root.bind('<l>', likeImage)
#root.bind('<d>', dislikeImage)

# particle filter button
filterButton = Button(root, text = "Run Probabilistic Model")
filterButton.configure(height = 2, width = 15, command = algo.probabilisticModel)
filterButton.grid(row = 1, column = 0)
filterButton.pack()

# control test button
controlButton = Button(root, text = "Run Random Model")
controlButton.configure(height = 2, width = 15, command = algo.randomModel)
controlButton.grid(row = 1, column = 1)
controlButton.pack()

# like button
likeButton = Button(app, text = "Like")
likeButton.configure(height = 2, width = 10, command = likeImage)
likeButton.grid(row = 2, column = 1)

# dislike button
dislikeButton = Button(app, text = "Dislike")
dislikeButton.configure(height = 2, width = 10, command = dislikeImage)
dislikeButton.grid(row = 2, column = 2)

# start
root.mainloop()