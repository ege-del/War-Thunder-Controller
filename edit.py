import pyautogui
import matplotlib.pyplot as plt


from random import Random
from PIL import Image,ImageEnhance
import keyboard
import matplotlib.pyplot as plt
import imutils
import numpy as np
import cv2
from skimage import measure

search_size = 1080

class Circle:
	x = 0
	y = 0
	r = 0
	id = ""	
	collide_count = 0

	def __init__(self, x,y,r):
		self.x=x
		self.y=y
		self.r=r
		self.id = str(x)+str(y)+str(r)

	def __eq__(self, other):
		if self.x == other.x and self.y == other.y:
			return True
		else:
			return False

	def colliding(self,target):
		if target in self.collision_list:
			return True
		else:
			return False

	def intersecting(self,target):
		if self != target:
			distSq = (self.x - target.x) * (self.x - target.x) + (self.y - target.y) * (self.y - target.y)
			radSumSq = (self.r + target.r) * (self.r + target.r)
			if distSq == radSumSq:
				self.collide_count +=1
				target.collide_count +=1
				return True
			elif distSq > radSumSq:
				return False
			else:
				self.collide_count +=1
				target.collide_count +=1
				return True
		else:
			return False


def overlay_routine(original,data):
	original_arr = np.asarray(original)

	circle_arr = []
	# loop over the contours
	for (i, c) in enumerate(data):
		# draw the bright spot on the image
		(x, y, w, h) = cv2.boundingRect(c)
		((cX, cY), radius) = cv2.minEnclosingCircle(c)
		cv2.circle(original_arr, (int(cX), int(cY)), int(radius),(0, 0, 255), 3)

		circle_arr.append(Circle(cX,cY,radius))
		cv2.putText(original_arr, "#{}".format(i + 1), (x, y - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
		print("draw circle")

	matches = []
	buf_circle_arr = circle_arr
	while len(buf_circle_arr)> 0 :
		c1 = buf_circle_arr.pop()
		for c2 in circle_arr:
			if c1.intersecting(c2):
				cv2.line(original_arr,(int(c1.x),int(c1.y)), (int(c2.x),int(c2.y)), (0,0,255), 2)

				if c1.collide_count == 1 and c2.collide_count == 1:
					a = (int((c1.x + c2.x)/2),int((c1.y + c2.y)/2))
					b = (int((c1.x + c2.x)/2)+60,int((c1.y + c2.y)/2))

					cv2.line(original_arr,a, b, (0,255,0), 2)


				print(c1.collide_count)
				print("found one")

	
	# show the output image
	return original_arr


def mine_image(target_i):
	labels = measure.label(target_i, connectivity=2, background=0)

	# print(type(worked_image_arr))
	mask = np.zeros(target_i.shape, dtype=np.uint8)
	# loop over the unique components
	for label in np.unique(labels):
		# if this is the background label, ignore it
		if label == 0:
			continue
		# otherwise, construct the label mask and count the
		# number of pixels 
		labelMask = np.zeros(target_i.shape, dtype=np.uint8)
		labelMask[labels == label] = 255
		numPixels = cv2.countNonZero(labelMask)
		# if the number of pixels in the component is sufficiently
		# large, then add it to our mask of "large blobs"
		if numPixels > 1000 and numPixels < 2000:
		# if numPixels > 3000 and numPixels < 5000:
			mask = cv2.add(mask, labelMask)

	# print(type(mask))
	# print(type(mask.copy()))
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	return cnts

def ench(a,factor):
	return a.enhance(factor)

def augment_image(target_i):
	# out = i_work(ImageEnhance.Contrast(out),2)
	# plt.figure()
	# plt.imshow(target_i)

	worked_image = ench(ImageEnhance.Sharpness(target_i),0.4)
	# lower = np.array([0, 0, 0])
	# upper = np.array([0, 0, 255])
	# thresh = cv2.inRange(np.asarray(worked_image), lower, upper)
		
	# # Change non-red to white
	# result = np.asarray(worked_image).copy()
	# result[thresh != 255] = (255,255,255)
	# worked_image = result
	# red   = [0,0,255]
	# Rmask = np.all(np.asarray(worked_image) == red,  axis=-1)

	# # Make all non-red pixels black
	# np.asarray(worked_image)[~Rmask] = red


	#VALUABLE
	# PROFILE FOR WHITE INSIDE RED BORDER TEXT 
	# lower_bound = np.array([0,0,0])
	# upper_bound = np.array([113,255,255])

	lower_bound = np.array([0,0,0])
	upper_bound = np.array([135,255,255])

	#VALUABLE
	#FULL RED TEXT
	# lower_bound = np.array([0,53,0])
	# upper_bound = np.array([38,158,255])
	#FULL RED TEXT V2
	# lower_bound = np.array([0,0,0])
	# upper_bound = np.array([255,139,255])

	hsv = cv2.cvtColor(np.asarray(worked_image), cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv,lower_bound,upper_bound) # modify your thresholds
	inv_mask = cv2.bitwise_not(mask)
	worked_image = cv2.bitwise_and(np.asarray(worked_image),np.asarray(worked_image), mask = inv_mask)



	# plt.figure("after color")
	# plt.imshow(worked_image)
	
	# PROFILE FOR WHITE WITH RED BORDER
	worked_image = cv2.threshold(np.asarray(worked_image), 225, 255, cv2.THRESH_BINARY)[1]
	
	# worked_image = cv2.threshold(np.asarray(worked_image), 0, 255, cv2.THRESH_BINARY)[1]

	print(worked_image.shape)
	# plt.figure("after binary ")
	# plt.imshow(worked_image)

	# right now only usefull for white with red border
	# worked_image[np.where((worked_image==[255,255,255]).all(axis=2))] = [0,0,0]
	# plt.figure("after replace ")
	# plt.imshow(worked_image)

	worked_image = cv2.cvtColor(worked_image, cv2.COLOR_RGB2GRAY)
	# plt.figure("after binary")
	# plt.imshow(worked_image)



	worked_image = cv2.dilate(worked_image, None, iterations=10)
	# plt.figure("after dilate")
	# plt.imshow(worked_image)


	return worked_image

def get_image_center(target_i,size):
	left = int(target_i.size[0]/2-size/2)
	upper = int(target_i.size[1]/2-size/2)
	right = left + size
	lower = upper +  size
	return  target_i.crop((left, upper,right,lower))


while(True):
    
    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('You Pressed A Key!')
            break  # finishing the loop
    else:
        image = pyautogui.screenshot('game_1.jpg')
    
    

        cropped = get_image_center(Image.open('game_1.jpg'),search_size)
        augmented = augment_image(cropped)
        mined = mine_image(augmented)
        result = overlay_routine(cropped,mined)
        #plt.figure()
    # plt.imshow(result)
    # plt.show()q
        plt.savefig("myimage.png")
    

    

