#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__ = '0.1'
__author__ = 'Andrey Derevyagin'
__maintainer__ = 'Andrey Derevyagin'
__email__ = '2derand+fractal@gmail.com'
__copyright__ = 'Copyright © 2013, Andrey Derevyagin'
__license__ = 'Use this code as you want'



from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import math
import threading
import Queue
import os


'''
# drawing area
xa = -2.0
xb = 1.0
ya = -1.5
yb = 1.5
'''

class ThreadClass(threading.Thread):
	def __init__(self, queue=None):
		threading.Thread.__init__(self)
		self.queue = queue

	def run(self):
		while True:
			frame_info = self.queue.get()

			frame = frame_info['frame']
			s_x, s_y, s_z = frame_info['start_point']
			sm_x, sm_y, sm_z = frame_info['frame_offset']

			c_x = s_x * math.pow(sm_x, frame)
			c_y = s_y * math.pow(sm_y, frame)
			c_z = s_z * math.pow(sm_z, frame)
			print 'frame %04d:'%frame, c_x, c_y, c_z
			self.generate_mandelbrot2('mandelbrot_%04d.jpg'%frame, c_x, c_y, c_z)

			self.queue.task_done()

	def generate_mandelbrot(self, filename, area_x=0.0, area_y=0.0, area_width=1.0, area_height=1.0, text=None):
		maxIt = 256 # max iterations allowed
		# image size
		imgx = 1280
		imgy = 720

		tmp = imgx * 2.0 / imgy 
		xa = area_x * tmp - tmp * 2.0 / 3.0
		xb = (area_x + area_width) * tmp - tmp * 2.0 / 3.0
		ya = area_y * 2.0 - 1.0
		yb = (area_y + area_height) * 2.0 - 1.0
		#print xa, xb, ya, yb
		image = Image.new("RGB", (imgx, imgy))
		for y in range(imgy):
			zy = y * (yb - ya) / (imgy - 1)  + ya
			for x in range(imgx):
				zx = x * (xb - xa) / (imgx - 1)  + xa
				z = zx + zy * 1j 
				c = z

				for i in range(maxIt):
					if abs(z) > 2.0: break 
					z = z * z + c
        
				#image.putpixel((x, y), (256 - i % 4 * 64, 256 - i % 8 * 32, 256 - i % 16 * 64))
				#image.putpixel((x, y), (256 - i % 16 * 16, 256 - i % 32 * 8, 256 - i % 64 * 4))
				image.putpixel((x, y), (256 - i  % 128 * 2, 256 - i % 256, 256 - i % 256))

				#print math.log(0)
				#image.putpixel((x, y), (x*y%512, (int)(math.log(x*y+1))%256, x*y%128))
				#image.putpixel((x, y), (256 - i % 4 * 64, 256 - i % 8 * 32, 256 - (int)(math.sqrt(x*y))%256))

		if text != None:
			font = ImageFont.truetype("Verdana.ttf", 14)
			draw = ImageDraw.Draw(image)
			draw.text((0, 0), text, (120, 20, 20), font=font)

		image.save(filename, "jpeg")
		#image.show()
		#print image.getbbox() 

	def generate_mandelbrot2(self, filename, area_center_x=0.5, area_center_y=0.5, area_zoom=1.0):
		zoom_v = 0.5 / area_zoom
		area_x = area_center_x - zoom_v
		area_y = area_center_y - zoom_v
		area_width = area_height = zoom_v * 2.0 
		self.generate_mandelbrot(filename, area_x, area_y, area_width, area_height, 'Zoom: %d%%'%(int)(area_zoom*100))



if __name__=='__main__':
	#ThreadClass().generate_mandelbrot('mandelbrot2.jpg', 0.25, 0.25, 0.25, 0.25)
	#ThreadClass().generate_mandelbrot2('mandelbrot.jpg', 0.3561, 0.397599, 5000000)
	#ThreadClass().generate_mandelbrot2('mandelbrot2.jpg', 0.5, 0.5, 2.0)
	#import sys
	#sys.exit()

	frames = 7
	# start point and zoom
	s_x = 0.5
	s_y = 0.5
	s_z = 1.0
	# end point and zoom
	e_x = 0.326097983272
	e_y = 0.38209901
	e_z = 10000000000000.0

	e_z = 7.0
	s_x = e_x
	s_y = e_y

	#sm_x = (e_x - s_x) / frames
	#sm_y = (e_y - s_y) / frames

	# calculate frame offset
	sm_x = math.pow(e_x / s_x, 1.0 / frames)
	sm_y = math.pow(e_y / s_y, 1.0 / frames)
	sm_z = math.pow(e_z / s_z, 1.0 / frames)

	'''
	for frame in range(frames+1):
		e_x = s_x * math.pow(sm_x, frame)
		e_y = s_y * math.pow(sm_y, frame)
		print 'frame %03d:'%frame, e_x, e_y, s_z
		generate_mandelbrot2('mandelbrot_%03d.jpg'%frame, e_x, e_y, s_z)
		s_z *= sm_z
	'''

	queue = Queue.Queue()
	for frame in range(frames+1):
		frame_info = {
			'start_point' : (s_x, s_y, s_z),
			'end_point' : (s_x, s_y, s_z),
			'frame_offset' : (sm_x, sm_y, sm_z),
			'frame' : frame,
			'frames' : frames
		}
		queue.put(frame_info)

	cores = os.sysconf('SC_NPROCESSORS_CONF')
	print "init %d threads"%cores
	for tid in range(cores):
		t = ThreadClass(queue)
		t.setDaemon(True)
		t.start()

	queue.join()
