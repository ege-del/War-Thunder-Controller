from sys import exec_prefix
from tracemalloc import start
import win32gui
import win32api
import time
import math

print("ok")
dc = win32gui.GetDC(0)
red = win32api.RGB(255, 0, 0)

class e_pixel:
	x = 0
	y = 0
	color = 0

	def __init__(self, x,y,color):
		self.x = x
		self.y = y
		if color == "red":
			self.color = win32api.RGB(255, 0, 0)
		if color == "blue":
			self.color = win32api.RGB(0, 0, 255)


class line:
	strt_p = None	
	end_p = None
	old = []
	def __init__(self, start_p, end_p):
		self.strt_p = start_p
		self.end_p = end_p

	def draw(self):
		# hyp = int(math.sqrt( (self.strt_p.x-self.end_p.x)**2 + (self.strt_p.y-self.end_p.y)**2 ))
		hyp = abs(self.strt_p.x-self.end_p.x)
		slope = (self.end_p.y - self.strt_p.y) / (self.end_p.x - self.strt_p.x)
		
		self.old = []
		for i in range(0,hyp):
			y = int(self.strt_p.x + (slope*i))
			self.old.append(win32gui.GetPixel(dc,self.strt_p.x+i,y))
			win32gui.SetPixel(dc, self.strt_p.x+i, y, red)
	
	def clean(self):
		# hyp = int(math.sqrt( (self.strt_p.x-self.end_p.x)**2 + (self.strt_p.y-self.end_p.y)**2 ))
		hyp = abs(self.strt_p.x-self.end_p.x)
		slope = (self.end_p.y - self.strt_p.y) / (self.end_p.x - self.strt_p.x)
		

		for i in range(0,hyp):
			y = int(self.strt_p.x + (slope*i))
			win32gui.SetPixel(dc, self.strt_p.x+i, y, self.old[i])
		self.old = []


class circle:
	center = None	
	radius = 0
	old = []
	def __init__(self, center, radius):
		self.center = center
		self.radius = radius

	def draw(self):
		self.old = []


		for th in range(0,360):
			x  =  int(self.center.x) + int((self.radius * math.cos(th)) / 4)
			y  =  int(self.center.y) + int((self.radius * math.sin(th)) / 4)
			# print(x,y,red)
			self.old.append(win32gui.GetPixel(dc,x,y))
			win32gui.SetPixel(dc, x,y,red) 

	def clean(self):
		for th in range(0,360):
			x  =  int(self.center.x) + int((self.radius * math.cos(th)) / 4)
			y  =  int(self.center.y) + int((self.radius * math.sin(th)) / 4)
			win32gui.SetPixel(dc, x,y,self.old[th]) 
		self.old = []
# x =[]



# def draw_loop():


# def clean():


# a = e_pixel()
# b = e_pixel()
# a.x = 100
# a.y = 100
# b.x = 1920
# b.y = 1080
# ed = line(a,b)
# ed.draw()


# a = e_pixel()
# a.x = 1920 / 2
# a.y = 1080 / 2
# ed = circle(a,25)

# lines = []
# circles = []

# while True:
# 	for i in lines:
# 		i.draw()
# 	for i in circles:
# 		i.draw()
# 	lines = []
# 	circles = []
	# ed.draw()

# square = 441
# draw random sized circles while playing warthunder
# lets see if we can write before game clears buffer

# print("collecting")
# for i in range(0,25):
# 	for z in range(0,25):
# 		buf = e_pixel()
# 		buf.x = i
# 		buf.y = z
# 		buf.color = win32gui.GetPixel(dc, i, z)
# 		x.append(buf)

# print("writing")
# for i in range(0,25):
# 	for z in range(0,25):
# 		win32gui.SetPixel(dc, i, z, red)  # draw red at 0,0pip install pywin32

# time.sleep(0.1)
# print("cleaning")
# for i in x:
# 	win32gui.SetPixel(dc, i.x,i.y,i.color) 
	