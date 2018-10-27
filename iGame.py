####################################################
##                   IMPORTS
####################################################

import tkinter
from tkinter import *
import random
from PIL import Image, ImageTk
from abc import ABC, abstractmethod
import os
import _thread
import math
import time

####################################################
##     GLOBAL VARIABLES - PREDEFINED PARAMETERS
####################################################

test_array1 = [Image.open('images/animations/vtak/vtak{}.png'.format(i)) for i in range(8)] 
test_array2 = [Image.open('images/animations/clovek/{}.png'.format(i)) for i in range(1,9)]
test_image = 'images/animations/pes/0.png'

CANVAS_DIMENSIONS = {'width' : 800, 'height' : 600}
KEY_EVENTS = ['LEFT', 'RIGHT', 'UP', 'DOWN', 'JUMP']
DIRECTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
ANIM_PARAMS = {'x' : 400, 'y' : 300, 'speed': 100, 'array1' : test_array1, 'direction1' : 'RIGHT', 'array2' : None, 'direction2' : None, 'file_name' : None, 'phases_num' : 0, 'tag' : None, 'weight' : 1}
ANIM_SET_IMAGES_PARAMS = {'array1' : None, 'direction1' : None, 'array2' : None, 'direction2' : None, 'file_name1' : None, 'phases_num' : 0, 'file_name2' : None}
FIGURE_PARAMS = {'x' : 400, 'y' : 300, 'speed' : 100, 'image' : test_image, 'tag' : None, 'weight' : 1}
SCREEN_PARAMS = {'background_img' : None, 'init_file' : None, 'width' : None, 'height' : None}
VARIABLE_PARAMS = {'x' : 100, 'y' : 10, 'name' : 'Variable', 'color' : 'black', 'value' : None, 'font' : 'Times', 'font_size' : 10, 'font_style' : 'bold'}
STATES = ['moving', ]
CANVAS = None
TIMER_MILISECS = 2

INIT_FILE_KEYWORDS = ['Tile', 'Background', 'Figure', 'Anim']
LAST_PHYSICS = 0

global time_passed
time_passed = 0
global epsilon
epsilon = 0.001



########################################################################################################
##                                          GLOBAL FUNCTIONS 
########################################################################################################

def get_key_pressed():
		key = CANVAS.get_button_pressed()
		if key:
			return key.keysym
		else:
			return None

def is_key_pressed():
	return CANVAS.key_pressed()

def is_clicked():
	return CANVAS.clicked()


########################################################################################################
##                                  		PHYSICS PACKAGE 
########################################################################################################



class Vector2D():

	def __init__(self, x = 0, y = 0):
		self.x = x
		self.y = y

	def __add__(self, vector):
		return Vector2D(self.x + vector.x, self.y + vector.y)

	def __sub__(self, vector):
		return Vector2D(self.x - vector.x, self.y - vector.y)

	def __mul__(self, c):
		return Vector2D(self.x * c, self.y * c)

	def __truediv__(self, c):
		return Vector2D(self.x / c, self.y / c)

	def __iadd__(self, vector):
		self.x += vector.x
		self.y += vector.y
		return self

	def __isub__(self, vector):
		self.x -= vector.x
		self.y -= vector.y
		return self

	def __imul__(self, c):
		self.x *= c
		self.y *= y
		return self

	def __itruediv__(self, c):
		self.x /= c
		self.y /= y
		return self

	@staticmethod
	def random(minX, maxX, minY, maxY):
		return Vector2D(random.uniform(minX, maxX), random.uniform(minY, maxY))

	def dot(self, vector):
		return self.x * vector.x + self.y * vector.y

	def lengthSqr(self):
		return self.x**2 + self.y**2

	def length(self):
		return math.sqrt(self.lengthSqr())

	def normalized(self):
		lengthSquared = self.lengthSqr();
		if abs(lengthSquared) < epsilon:
			return Vector2D(1, 0)

		length = math.sqrt(lengthSquared)
		x = self.x / length
		y = self.y / length
		return Vector2D(x, y)


class RigidBody():
	
	def __init__(self, obj = None, position = Vector2D(), size = Vector2D(25, 25), mass = 1, speed = Vector2D(), friction = 1):
		self.obj = obj
		self.position = position
		self.size = size
		self.mass = mass
		self.speed = speed
		self.friction = friction

	def top(self):
		return self.position.y - self.size.y

	def left(self):
		return self.position.x - self.size.x

	def right(self):
		return self.position.x + self.size.x

	def bottom(self):
		return self.position.y + self.size.y

	def energy(self):
		return (self.mass * self.speed.lengthSqr()) / 2

class Physics():

	@staticmethod
	def move(body, dt):
		body.position += body.speed * dt
		# body.obj.canvas.move(body.obj.id, body.position.x - body.obj.x, body.position.y - body.obj.y)
		# body.obj.x = body.position.x
		# body.obj.y = body.position.y
		if body.friction < 1:
			body.speed *= (body.friction**dt)

	@staticmethod
	def intersects_x(B1, B2, tolerance = 0):
		if B1.left() > B2.right() + tolerance:
			return False
		if B1.right() < B2.left() - tolerance:
			return False

		return True

	@staticmethod
	def intersects_y(B1, B2, tolerance = 0):
		if B1.bottom() < B2.top() + tolerance:
			return False
		if B1.top() > B2.bottom() - tolerance:
			return False

		return True

	@staticmethod
	def intersects(B1, B2, tolerance = 0):
		return Physics.intersects_x(B1, B2, tolerance) and Physics.intersects_y(B1, B2, tolerance)

	@staticmethod
	def intersects_after_offset(B1, B2, dt, tolerance = 0):
		# CB1 = RigidBody(None, B1.position, B1.size, B1.mass, B1.speed, B1.friction)
		# CB2 = RigidBody(None, B2.position, B2.size, B2.mass, B2.speed, B2.friction)

		# CB1 = RigidBody(None, Vector2D(copy.deepcopy(B1.position.x), copy.deepcopy(B1.position.y)), B1.size, B1.mass, B1.speed, B1.friction)
		# CB2 = RigidBody(None, Vector2D(copy.deepcopy(B2.position.x), copy.deepcopy(B2.position.y)), B2.size, B2.mass, B2.speed, B2.friction)

		Physics.move(B1, dt)
		Physics.move(B2, dt)
		
		# Physics.move(B1, dt)
		# Physics.move(B2, dt)
		value = Physics.intersects(B1, B2, tolerance)
		Physics.move(B1, -dt)
		Physics.move(B2, -dt)
		return value
		# return Physics.intersects(B1, B2, tolerance)

	@staticmethod
	def intersection_x(B1, B2):
		if not Physics.intersects_x(B1, B2):
			return 0

		return abs(min(B1.right(), B2.right()) - max(B1.left(), B2.left()))


	@staticmethod
	def intersection_y(B1, B2):
		if not Physics.intersects_y(B1, B2):
			return 0

		return abs(max(B1.top(), B2.top()) - min(B1.bottom(), B2.bottom()))	

	@staticmethod
	def check_right_wall(body, wall):
		if body.right() < wall:
			return
		body.speed.x = -abs(body.speed.x)

	@staticmethod
	def check_left_wall(body, wall):
		
		if body.left() > wall:
			return
		body.speed.x = abs(body.speed.x)

	@staticmethod
	def check_top_wall(body, wall):
		
		if body.top() > wall:
			return
		body.speed.y = abs(body.speed.y)

	@staticmethod
	def check_bottom_wall(body, wall):
		
		if body.bottom() < wall:
			return
		body.speed.y = -abs(body.speed.y)

	@staticmethod
	def collide(B1, B2, dt):
		#STEP 0: check if there is any collision to solve
		if not Physics.intersects(B1, B2):
			return
		m1 = B1.mass
		m2 = B2.mass

		#STEP 1: move one out of another (by rolling back the time or simply moving), so they don't intersect anymore
		ddt = 0;
		if Physics.intersects_after_offset(B1, B2, -dt, -0.1):
			offset = ( B2.position - B1.position ).normalized()
			
			for i in range(500):
				B1.position -= offset * m2 / (m1 + m2)
				B2.position += offset * m1 / (m1 + m2)
				if not Physics.intersects(B1, B2):
					break

		else:
			tMin = -dt
			tMax = 0

			for i in range(10):
				ddt = (tMin + tMax) / 2
				if Physics.intersects_after_offset(B1, B2, ddt):
					tMax = ddt 
				else:
					tMin = ddt
			
			ddt = (tMin + tMax) / 2
			Physics.move(B1, ddt)
			Physics.move(B2, ddt)

		#STEP 2: to get normal vector, determine from which side objects hit

		if Physics.intersection_x(B1, B2) > Physics.intersection_y(B1, B2):
			normal = Vector2D(0, 1)
		else: 
			normal = Vector2D(1, 0)
		tangent = Vector2D(-normal.y, normal.x)	#xy -> -yx gives orthogonal direction
		#STEP 3: recalculate speeds
		surfaceFriction = 1#0.25
		v1 = B1.speed
		v2 = B2.speed	
		#split to tangent and normal components
		vn1 = normal * normal.dot(v1)
		vt1 = tangent * tangent.dot(v1)
		vn2 = normal * normal.dot(v2)
		vt2 = tangent * tangent.dot(v2) 
		#perform 1D elastic collisions
		_vn1 = (vn1 * (m1 - m2) + vn2 * m2 * 2) / (m1 + m2)
		_vn2 = (vn2 * (m2 - m1) + vn1 * m1 * 2) / (m1 + m2)
		# _vt1 = (vt1 * (m1 - m2) + vt2 * m2 * 2) / (m1 + m2)
		# _vt2 = (vt2 * (m2 - m1) + vt1 * m1 * 2) / (m1 + m2)
		# v1 = _vn1 + (_vt1 * surfaceFriction + vt1 * (1-surfaceFriction))
		# v2 = _vn2 + (_vt2 * surfaceFriction + vt2 * (1-surfaceFriction))

		v1 = _vn1 + vt1
		v2 = _vn2 + vt2

		B1.speed = v1
		B2.speed = v2

		if ddt != 0: 
			Physics.move(B1, -ddt) 
			Physics.move(B2, -ddt)


########################################################################################################
##                                  IMPLEMENTATION - HELPER MODULES 
########################################################################################################

class WrongParameterError(Exception): pass


class ImageCutter():
	
	@staticmethod
	def crop(input_file, output_folder, output_name, rows, cols):
		dir = os.path.dirname(input_file)
		filename = os.path.join(dir, output_folder)
		if not os.path.exists(filename):
			os.makedirs(filename)

		img = Image.open(input_file)
		width, height = img.width, img.height
		result_img_width, result_img_height = width/cols, height/rows
		
		tmp = 0
		for i in range(rows):
			for j in range(cols):
				x, y = i*result_img_width, j*result_img_height

				new_img = img.crop((x, y, x + result_img_width, y + result_img_height))
				if new_img.load():
					new_img.save(output_folder + '/{}{}.png'.format(output_name, tmp))

				tmp += 1

# ImageCutter.crop('animacie/potvorka1.png', 'animacie/potvorka1', 'potvorka', 1, 4)

class GifParser():

	@staticmethod
	def parse(output_folder, input_file, output_name):
		dir = os.path.dirname(input_file)
		filename = os.path.join(dir, output_folder)
		if not os.path.exists(filename):
			os.makedirs(filename)
		result = []
		gif = Image.open(input_file)
		i = 0
		while True:
			result.append(gif.save(output_folder + '/{}{}.png'.format(output_name, i)))
			try:
				i += 1
				gif.seek(i)
			except EOFError:
				break

		return result

class ImageTkConverter():

	@staticmethod
	def convert(array):
		for i in range(len(array)):
			array[i] = ImageTk.PhotoImage(array[i])

class ParamsSetter():

	@staticmethod
	def set(cls, kwargs):
		params = dict()
		if isinstance(cls, Anim):
			params = ANIM_PARAMS
		elif isinstance(cls, Figure):
			params = FIGURE_PARAMS
		elif isinstance(cls, Variable):
			params = VARIABLE_PARAMS
		elif isinstance(cls, Screen):
			params = SCREEN_PARAMS

		for param in params:
			if param not in kwargs:
				kwargs[param] = params[param]

class ParamsChecker():

	@staticmethod
	def check(cls, kwargs):
		params = dict()
		if isinstance(cls, Anim):
			params = ANIM_PARAMS
		elif isinstance(cls, Figure):
			params = FIGURE_PARAMS
		elif isinstance(cls, Variable):
			params = VARIABLE_PARAMS
		elif isinstance(cls, Screen):
			params = SCREEN_PARAMS

		for param in kwargs:
			if param not in params:
				return False
		return True

class ArrayCopier():

	@staticmethod
	def copy(input, output):
		for item in input:
			output.append(item)

class App():

	@staticmethod
	def start():
		global app
		app = tkinter.Tk()

class CanvasTkinter():

	def __init__(self, background_img = None, size = (None, None)):
		# private members
		self.clicked_x = None
		self.clicked_y = None
		self.pressed_key = None

		if background_img is not None:
			self.canvas = tkinter.Canvas(width = background_img.width(), height = background_img.height())
			self.__width = background_img.width() 
			self.__height = background_img.height()
		elif size != (None, None):
			self.canvas = tkinter.Canvas(width = size[0], height = size[1])
			self.__width = size[0]
			self.__height = size[1]
		else:
			self.canvas = tkinter.Canvas(width = CANVAS_DIMENSIONS['width'], height = CANVAS_DIMENSIONS['height'])
			self.__width = CANVAS_DIMENSIONS['width']
			self.__height = CANVAS_DIMENSIONS['height']

		self.canvas.pack()
		self.canvas.bind('<Button-1>', self.click)
		self.canvas.bind_all('<Key>', self.button_pressed)
		# self.canvas.bind("<B1-Motion>", self.drag)

	def width(self):
		return self.__width

	def height(self):
		return self.__height

	def click(self, event):
		# private
		self.clicked_x = event.x
		self.clicked_y = event.y

	def button_pressed(self, event):
		# private
		self.pressed_key = event

	def key_pressed(self):
		'''
			Returns True if any key was pressed else returns False
		'''
		return True if self.pressed_key is not None else False

	def clicked(self):
		'''
			Returns True if click event occured else returns False
		'''
		return True if self.clicked_y != None or self.clicked_x != None else False


	## __________GETTERS__________

	def get_click_coords(self):
		# public
		return (self.clicked_x, self.clicked_y)

	def get_button_pressed(self):
		# public
		return self.pressed_key

	def get_canvas_obj(self):
		# public
		return self.canvas

	## __________SETTERS__________

	def set_default_click(self):
		# public
		self.clicked_x = None
		self.clicked_y = None

	def set_default_key(self):
		# public
		self.pressed_key = None


########################################################################################################
##                                  IMPLEMENTATION OF MAIN OBJECTS
########################################################################################################

class Variable():

	def __init__(self, **kwargs):
		if not ParamsChecker.check(self, kwargs):
			raise NameError('wrong params given')
		ParamsSetter.set(self, kwargs)
		font = kwargs['font'] + ' ' + str(kwargs['font_size'])
		if kwargs['font_style']:
			font += ' ' + kwargs['font_style']
		
		self.id = CANVAS.get_canvas_obj().create_text(kwargs['x'], kwargs['y'], font = font, text = kwargs['name'] + ' : ' + str(kwargs['value']), fill = kwargs['color'])
		self.text = kwargs['name'] + ' : '
		self.color = kwargs['color']
		self.x = kwargs['x']
		self.y = kwargs['y']
		self.font = kwargs['font']
		self.font_size = kwargs['font_size']
		self.font_style = kwargs['font_style']

	def change_value(self, value):
		CANVAS.get_canvas_obj().itemconfig(self.id, text = self.text + str(value))

	def change_position(self, **kwargs):
		if 'x' in kwargs:
			if not isinstance(kwargs['x'], int) and not isinstance(kwargs['x'], float):
				raise ValueError('Wrong x coordinate given. It should be integer or float.')
			CANVAS.get_canvas_obj().move(self.id, kwargs['x'] - self.x, 0)
			self.x = kwargs['x']
		if 'y' in kwargs:
			if not isinstance(kwargs['y'], int) and not isinstance(kwargs['y'], float):
				raise ValueError('Wrong y coordinate given. It should be integer or float.')
			CANVAS.get_canvas_obj().move(self.id, 0, kwargs['y'] - self.y)
			self.y = kwargs['y']

	def change_color(self, color):
		self.color = color
		CANVAS.get_canvas_obj().itemconfig(self.id, fill = self.color)

	def change_font_size(self, size):
		if not isinstance(size, int) and not isinstance(size, float):
			raise ValueError('Wrong size given. It should be integer or float.')

		self.size = size
		CANVAS.get_canvas_obj().itemconfig(self.id, font = self.font + ' ' + str(self.size) + ' ' + self.font_style if self.font_style else '')

	def change_font_style(self, style):
		self.font_style = style
		CANVAS.get_canvas_obj().itemconfig(self.id, font = self.font + ' ' + str(self.size) + ' ' + self.font_style if self.font_style else '')

	def change_font(self, font):
		self.font = font
		CANVAS.get_canvas_obj().itemconfig(self.id, font = self.font + ' ' + str(self.size) + ' ' + self.font_style if self.font_style else '')


class State():
	"""This is the template for all the other states"""

	def __init__(self):
		self.states = dict()

	def __setitem__(self, key, value):
		self.states[key] = value

	def __getitem__(self, key):
		return self.states[key]

	def set_default(self, sprite):
		if isinstance(sprite, Figure):
			self.set_default_figure()
		elif isinstance(sprite, Anim):
			self.set_default_anim()
		# to do

	def set_default_figure(self):
		# malo by byt private   
		self.states['standing'] = False
		self.states['moving'] = True

	def set_default_anim(self):
		self.states['moving'] = False


class Base(ABC):

	master = None
	canvas = None
	screen = None

	def __init__(self, x, y, speed, image, weight):
		self.attributes = dict()

		if image:
			self.base_image = Image.open(image)
			self.image = ImageTk.PhotoImage(self.base_image)
			self.id = self.canvas.create_image(x, y, image=self.image)
			self.attributes['width'] = self.image.width()
			self.attributes['height'] = self.image.height()
		else:
			self.image = self.base_image = None
			self.id = None

		self.x = x
		self.y = y  
		self.speed = speed
		self.grid_style = False
		self.dx = speed
		self.dy = speed
		self.click_drag_flag = False

		self.direction = None

		self.was_clicked = False
		self.time_passed = 0
		self.states = State()
		self.velocity_x = 0
		self.velocity_y = 0

	def is_out_of_screen(self):
		'''    
			This function finds out wheter sprite is on screen or out.
		'''
		if (
				0 < self.x + self['width'] and self.x - self['width'] < self.screen['width'] and
				0 < self.y + self['height'] and self.y - self['height'] < self.screen['height']
		   ):
			return False
		return True

	def set_velocity(self, x = 0, y = 0):
		'''
			Sets x and y of vector.
		'''
		self.velocity_x = x
		self.velocity_y = y
		self.body.speed.x = x
		self.body.speed.y = y

	def make_step(self):
		'''
			Moves given length according to vector.
		'''
		global LAST_PHYSICS
		if LAST_PHYSICS == 0:
			LAST_PHYSICS = time.time()
			dt = 0
		else:
			curr_time = time.time()
			dt = curr_time - LAST_PHYSICS
			LAST_PHYSICS = curr_time
		Physics.move(self.body, dt)
		self.canvas.move(self.id, self.body.position.x - self.body.obj.x, self.body.position.y - self.body.obj.y)
		self.x = self.body.position.x
		self.y = self.body.position.y
		
		# self.canvas.move(self.id, self.body.position.x - self.x, self.body.position.y - self.y)

		# self.x = self.body.position.x
		# self.y = self.body.position.y

		# self.x += self.velocity_x
		# self.y += self.velocity_y
		# self.canvas.move(self.id, self.velocity_x, self.velocity_y)

	def waited(self, time_in_seconds):
		'''
			Returns True after given time.
		'''
		if self.time_passed == time_in_seconds*1000:
			self.time_passed = 0
			return True
		else:
			self.time_passed += TIMER_MILISECS
			return False

	def __setitem__(self, key, value):
		self.attributes[key] = value

	def __getitem__(self, key):
		return self.attributes[key]

	def get_id(self):
		return self.id

	def delete(self):
		'''
			Erase sprite from canvas.
		'''
		self.canvas.delete(self.id)

	def is_clicked(self):
		'''
			Returns boolean value whether sprite was clicked or not.
		'''
		x, y = CANVAS.get_click_coords()
		if x is not None and y is not None:
			if (    
					x >= self.x - self.attributes['width']/2 and 
					x <= self.x + self.attributes['width']/2 and 
					y >= self.y - self.attributes['height']/2 and
					y <= self.y + self.attributes['height']/2
			   ):
				return True
		return False


	def set_position(self, **kwargs):
		'''
			Sets sprite to given coordinates.
		'''
		if 'x' in kwargs:
			if not isinstance(kwargs['x'], int) and not isinstance(kwargs['x'], float):
				raise ValueError('Wrong x coordinate given. It should be integer or float.')
			self.canvas.move(self.id, kwargs['x'] - self.x, 0)
			self.x = kwargs['x']
			self.body.position.x = self.x
		if 'y' in kwargs:
			if not isinstance(kwargs['y'], int) and not isinstance(kwargs['y'], float):
				raise ValueError('Wrong y coordinate given. It should be integer or float.')
			self.canvas.move(self.id, 0, kwargs['y'] - self.y)
			self.y = kwargs['y']
			self.body.position.y = self.y
		

	def set_state(self, key, value):
		self.states[key] = value

	def get_state(self, key):
		return self.states[key]

	def set_grid_style(self):
		self.grid_style = True

	def set_non_grid_style(self):
		self.grid_style = False

	def set_direction(self, direction):
		if direction in DIRECTIONS:
			self.direction = direction 
		else:
			raise ValueError('Wrong direction given. It should be one of {}, but your input was {}.'.format(DIRECTIONS, direction))

	def show(self):
		'''
			Shows sprite on canvas if sprite was hidden before.
		'''
		if self.hidden:
			self.id = self.canvas.create_image(self.x, self.y, image = self.image)
			self.hidden = False

	def hide(self):
		'''
			Hides sprite from canvas if sprite was visible before.
		'''
		self.hidden = True
		self.canvas.delete(self.id)

	@abstractmethod
	def move(self):
		pass

	## ___________________________COLISIONS______________________________    

	def touching_color(self, tile_array, color): 
		'''
			Returns True if sprite collides with tile of given color. Default color for tile is green.
		'''
		for tile in tile_array:
			if (
					abs(self.x - tile.x) <= self.attributes['width']/2 + tile['width']/2 and
					abs(self.y - tile.y) <= self.attributes['height']/2 + tile['height']/2 and
					tile.color == color
			   ):
				return True
		return False

	def collides(self, sprites):
		'''
			Returns True if sprite is in collicion with given sprites in entry parameter.

		'''
		try:
			if len(sprites):
				for sprite in sprites:
					if (
						abs(self.x - sprite.x) <= self.attributes['width']/2 + sprite['width']/2 and
						abs(self.y - sprite.y) <= self.attributes['height']/2 + sprite['height']/2
						):
						return True
				return False
		except TypeError:
			if (
				abs(self.x - sprites.x) <= self.attributes['width']/2 + sprites['width']/2 and
				abs(self.y - sprites.y) <= self.attributes['height']/2 + sprites['height']/2
				):
				return True
			return False


	def bounce(self, obj = None):
		'''
			Bounces sprite from given object. Object can be Anim, Figure or Tile. If object is None, sprite is bounced from the edge of window.
		'''
		# if obj:
		# 	if self.check_hit_from_side(obj):
		# 		self.set_velocity(x = -self.velocity_x, y = self.velocity_y)
		# 	else:
		# 		self.set_velocity(x = self.velocity_x, y = -self.velocity_y)
		# 	while self.collide(obj):
		# 		print(self.velocity_x, self.velocity_y)
		# 		self.make_step()
		# else:
		# 	if self.get_wall_collision() == 'left' or self.get_wall_collision() == 'right':
		# 		self.set_velocity(x = -self.velocity_x, y = self.velocity_y)
		# 	elif self.get_wall_collision() == 'up' or self.get_wall_collision() == 'down':
		# 		self.set_velocity(x = self.velocity_x, y = -self.velocity_y)
		# 	while self.get_wall_collision():
		# 		self.make_step()
		
		# if not (self.velocity_y != 0 and self.velocity_x != 0):
		# 	self.make_step()

		if obj is None:
			Physics.check_left_wall(self.body, 0)
			Physics.check_right_wall(self.body, self.screen['width'])
			Physics.check_bottom_wall(self.body, self.screen['height'])
			Physics.check_top_wall(self.body, 0)
		else:
			Physics.collide(self.body, obj.body, TIMER_MILISECS)

	def check_hit_from_side(self, obj):
		x1 = self.x + self['width']/2
		y1 = self.y + self['height']/2

		x2 = self.x + self['width']/2
		y2 = self.y - self['height']/2

		x3 = self.x
		y3 = self.y

		x4 = obj.x
		y4 = obj.y

		denominator_uab = (y4 - y3)*(x2 - x1) - (x4 - x3)*(y2 - y1)

		if denominator_uab == 0:
			# side line and drawbar are parallel
			return False

		ua = ((x4 - x3)*(y1 - y3) - (y4 - y3)*(x1 - x3))/denominator_uab
		if 0 < ua and ua < 1:
			return True
		# ub = ((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3))/denominator_uab
		# if 0 < ub and ub < 1:

		#     return True
		return False

	def get_wall_collision(self):
		if self.x <= self.attributes['width']/2: 
			return 'left'
		elif self.x >= CANVAS.width() - self.attributes['width']/2: 
			return 'right'
		elif self.y <= self.attributes['height']/2: 
			return 'up'
		elif self.y >= CANVAS.height() - self.attributes['height']/2: 
			return 'down'
		else: 
			return None 

	def collides_with_wall(self, wall = None):
		'''
			Returns True if sprite is on the edge of window or given side of window.
		'''
		if wall is None:
			if (
					self.x <= self.attributes['width']/2 or self.x >= CANVAS.width() - self.attributes['width']/2 or
					self.y <= self.attributes['height']/2 or self.y >= CANVAS.height() - self.attributes['height']/2 
			   ):
				return True
			else:
				return False

		if wall == 'LEFT':
			if self.x <= self.attributes['width']/2:
				return True
			return False

		elif wall == 'RIGHT':
			if self.x >= CANVAS.width() - self.attributes['width']/2:
				return True
			return False

		elif wall == 'TOP':
			if self.y <= self.attributes['height']/2:
				return True
			return False

		elif wall == 'BOTTOM':
			if  self.y >= CANVAS.height() - self.attributes['height']/2:
				return True
			return False

		else:
			raise WrongParameterError('You gave undefined side of window. Expected: TOP, LEFT, RIGHT or BOTTOM. But you set {}'.format(wall))


	## _________________________MOTION FUNCTIONS_________________________

	def move_right(self, x = 0):
		if x == 0:
			self.x += self.dx
			self.velocity_x = self.dx
			self.canvas.move(self.id, self.dx, 0)
		else: 
			self.x += x
			self.velocity_x = x
			self.canvas.move(self.id, x, 0)
		self.velocity_y = 0
		self.body.position.x = self.x

	def move_left(self, x = 0):
		if x == 0:
			self.x -= self.dx
			self.velocity_x = -self.dx
			self.canvas.move(self.id, -self.dx, 0)
		else:
			self.x -= x
			self.velocity_x = -x
			self.canvas.move(self.id, -x, 0)
		self.velocity_y = 0
		self.body.position.x = self.x

	def move_up(self, x = 0):
		if x == 0:
			self.y -= self.dy
			self.velocity_y = -self.dy
			self.canvas.move(self.id, 0, -self.dy)
		else:
			self.y -= x
			self.velocity_y = -x
			self.canvas.move(self.id, 0, -x)
		self.velocity_x = 0
		self.body.position.y = self.y

	def move_down(self, x = 0):
		if x == 0:
			self.y += self.dy
			self.velocity_y = self.dy
			self.canvas.move(self.id, 0, self.dy)
		else:
			self.y += x
			self.velocity_y = x
			self.canvas.move(self.id, 0, x)
		self.velocity_x = 0
		self.body.position.y = self.y
		# mozno aj self.body.speed.x = 0

	def step_back(self):
		if self.direction == 'RIGHT':
			self.move_left()

		elif self.direction == 'LEFT':
			self.move_right()

		elif self.direction == 'UP':
			self.move_down()

		elif self.direction == 'DOWN':
			self.move_up()


class Sprite(Base, ABC):
	
	def __init__(self, x, y, speed, image, weight):
		super().__init__(x, y, speed, image, weight)
		self.angle = 0
		self.hidden = False
		if self.image:
			self.img_array = [self.base_image]
			self.img_array_index = 0
		else:
			self.img_array = []
			self.img_array_index = None


	def lift(self):
		'''
			Sets object to the top layer of the screen.
		'''
		# self.canvas.lift(sprite.get_id())
		self.canvas.tag_raise(self.id)

	def lower(self):
		'''
			Sets object to the bottom layer of the screen.
		'''
		# self.canvas.lower(sprite.get_id())
		self.canvas.tag_lower(self.id)

	def change_image(self, new_image = None):
		if new_image:
			self.base_image = Image.open(new_image)
			self.image = ImageTk.PhotoImage(self.base_image)
			self.canvas.itemconfig(self.id, image = self.image)
			self.attributes['width'] = self.image.width()
			self.attributes['height'] = self.image.height()
		else:
			raise WrongParameterError("Wrong input given. Expected png file. Your input: {}.".format(new_image))  

	def rotate(self, angle = 0):
		if not isinstance(angle, int) and not isinstance(angle, float):
			raise ValueError('Wrong angle given. It should be integer or float.')
		
		self.angle += angle
		self.canvas.delete(self.id)
		self.image = ImageTk.PhotoImage(self.base_image.rotate(self.angle))
		self.id = self.canvas.create_image(self.x, self.y, image=self.image)  

	def calculate_coords(self, angle):
		self.angle += angle
		self.velocity_x = self.speed * round(math.cos(math.pi * (self.angle/180)), 1)
		self.velocity_y = self.speed * round(math.sin(math.pi * (self.angle/180)), 1)        

	def forward(self, distance):
		if not isinstance(distance, int) and not isinstance(distance, float):
			raise ValueError('Wrong distance given. It should be integer or float.')
		
		self.body.speed.x = self.velocity_x = distance * round(math.cos(math.pi * (self.angle/180)), 1)
		self.body.speed.y = self.velocity_y = distance * round(math.sin(math.pi * (self.angle/180)), 1)

		self.make_step()

	def backward(self, distance):
		if not isinstance(distance, int) and not isinstance(distance, float):
			raise ValueError('Wrong distance given. It should be integer or float.')

		self.body.speed.x = self.velocity_x = -distance * round(math.cos(math.pi * (self.angle/180)), 1)
		self.body.speed.y = self.velocity_y = -distance * round(math.sin(math.pi * (self.angle/180)), 1)

		self.make_step()

	def add_img(self, img):
		if img:
			self.img_array.append(Image.open(img))
		else:
			raise ValueError('You forgot to set image parameter. Image parameter can not be empty.')

	def next_img(self):
		if self.img_array_index is None:
			self.img_array_index = 0
		else:
			self.img_array_index += 1
			self.img_array_index = self.img_array_index % len(self.img_array)
		self.base_image = self.img_array[self.img_array_index]
		self.image = ImageTk.PhotoImage(self.base_image)
		CANVAS.get_canvas_obj().itemconfig(self.id, image = self.image)

	@abstractmethod
	def move(self):
		pass


class Anim(Base):
	
	def __init__(self, **kwargs):
		if not ParamsChecker.check(self, kwargs):
			raise NameError('wrong params given')
		ParamsSetter.set(self, kwargs)
		super().__init__(kwargs['x'], kwargs['y'], kwargs['speed'], None, kwargs['weight'])
		self.id = self.canvas.create_image(kwargs['x'], kwargs['y'])

		self.left_array = []
		self.right_array = []
		self.down_array = []
		self.up_array = []

		if kwargs['array1'] == test_array1 and kwargs['file_name'] != None and kwargs['phases_num'] != 0:
			fname = kwargs['file_name'].split('.')[0]
			fformat = kwargs['file_name'].split('.')[1]
			kwargs['array1'] = [Image.open(fname + '{}'.format(i) + '.' + fformat) for i in range(kwargs['phases_num'])] 

		self.set_arrays(kwargs['array1'], kwargs['direction1'], kwargs['array2'], kwargs['direction2'])
		self.set_direction(kwargs['direction1'])

		self.automatic_animation = True
		self.moving = False #default setting
		self.phase = 0
 
		self.states.set_default(self)   

		self.set_step_count()

		self.update_img()

		if kwargs['tag'] in self.screen.anim_array.keys():
			self.screen.anim_array[kwargs['tag']].append(self)   
		else:
			self.screen.anim_array[kwargs['tag']] = [self] 

		self.body = RigidBody(self, Vector2D(self.x, self.y), Vector2D(self.attributes['width']/2, self.attributes['height']/2), kwargs['weight'], Vector2D(x=0, y=0))
		

	def set_images(self, **kwargs):
		self.left_array = []
		self.right_array = []
		self.down_array = []
		self.up_array = []

		for param in ANIM_SET_IMAGES_PARAMS:
			if param not in kwargs:
				kwargs[param] = ANIM_SET_IMAGES_PARAMS[param]

		if (kwargs['file_name1'] and kwargs['array1']) or (kwargs['file_name2'] and kwargs['array2']):
			raise WrongParameterError('You can not set file and array of images at once.')

		if kwargs['direction1'] is None and kwargs['direction2'] is None:
			raise WrongParameterError('Direction must be set. You forgot to set direction.')

		if kwargs['file_name1'] != None and kwargs['phases_num'] != 0:
			fname = kwargs['file_name1'].split('.')[0]
			fformat = kwargs['file_name1'].split('.')[1]
			kwargs['array1'] = [Image.open(fname + '{}'.format(i) + '.' + fformat) for i in range(kwargs['phases_num'])] 

		if kwargs['file_name2'] != None and kwargs['phases_num'] != 0:
			fname = kwargs['file_name2'].split('.')[0]
			fformat = kwargs['file_name2'].split('.')[1]
			kwargs['array2'] = [Image.open(fname + '{}'.format(i) + '.' + fformat) for i in range(kwargs['phases_num'])]         

		self.set_arrays(kwargs['array1'], kwargs['direction1'], kwargs['array2'], kwargs['direction2'])
		self.set_direction(kwargs['direction1'])
		self.set_step_count()


	def set_arrays(self, array1, direction1, array2 = None, direction2 = None):
		if array1:
			if direction1 == 'RIGHT':
				ArrayCopier.copy(array1, self.right_array)
			elif direction1 == 'LEFT':
				ArrayCopier.copy(array1, self.left_array)
			elif direction1 == 'UP':
				ArrayCopier.copy(array1, self.up_array)
			elif direction1 == 'DOWN':
				ArrayCopier.copy(array1, self.down_array)
			else:
				self.make_static()

		if array2:
			if direction2 == 'RIGHT':
				ArrayCopier.copy(array2, self.right_array)
			elif direction2 == 'LEFT':
				ArrayCopier.copy(array2, self.left_array)
			elif direciton2 == 'UP':
				ArrayCopier.copy(array2, self.up_array)
			elif direction2 == 'DOWN':
				ArrayCopier.copy(array2, self.down_array)
			else:
				raise NameError('Direction name not recognized!')
	   
		if self.left_array:
			self.attributes['width'] = self.left_array[0].width
			self.attributes['height'] = self.left_array[0].height
			self.create_right_animation()
			ImageTkConverter.convert(self.left_array) # after transition it is necessary to convert the original array of images to ImageTk.PhotoImage
		elif self.right_array:
			self.attributes['width'] = self.right_array[0].width
			self.attributes['height'] = self.right_array[0].height
			self.create_left_animation()
			ImageTkConverter.convert(self.right_array)

		if self.up_array:
			self.attributes['width'] = self.up_array[0].width
			self.attributes['height'] = self.up_array[0].height
			self.create_down_animation()
			ImageTkConverter.convert(self.up_array)
		elif self.down_array:
			self.attributes['width'] = self.down_array[0].width
			self.attributes['height'] = self.down_array[0].height
			self.create_up_animation()
			ImageTkConverter.convert(self.down_array)
	

	def create_left_animation(self):
		self.left_array = []
		for img in self.right_array:
			self.left_array.append(ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)))

	def create_right_animation(self):
		self.right_array = []
		for img in self.left_array:
			self.right_array.append(ImageTk.PhotoImage(img.transpose(Image.FLIP_LEFT_RIGHT)))

	def create_up_animation(self):
		self.up_array = []
		for img in self.down_array:
			self.up_array.append(ImageTk.PhotoImage(img.transpose(Image.FLIP_TOP_BOTTOM)))

	def create_down_animation(self):
		self.down_array = []
		for img in self.up_array:
			self.down_array.append(ImageTk.PhotoImage(img.transpose(Image.FLIP_TOP_BOTTOM)))

	def animate_automatically(self, value):
		if value:
			self.automatic_animation = True
		else:
			self.automatic_animation = False
			self.moving = False

	def make_static(self):
		self.moving = False

	def make_movable(self):
		self.moving = True

	def set_default_direction(self):
		if self.right_array is not None:
			self.direction = 'RIGHT'
		elif self.up_array is not None:
			self.direction = 'UP'

	def step_count_minus(self):
		if self.step_count == 0:
			self.states['moving'] = False
			self.set_step_count()
			self.phase = 0
			self.update_img()
			return False
		else:
			self.step_count -= 1
			return True

	def set_step_count(self):
		if self.direction in ['LEFT', 'RIGHT']:
			self.phases_num = self.step_count = len(self.right_array)
		elif self.direction in ['UP', 'DOWN']:
			self.phases_num = self.step_count = len(self.up_array)

	def update_img(self):
		if self.direction == 'RIGHT':
			img = self.right_array[self.phase]
		elif self.direction == 'LEFT':
			img = self.left_array[self.phase]
		elif self.direction == 'UP':
			img = self.up_array[self.phase]
		else:
			img = self.down_array[self.phase]
			
		self.canvas.itemconfig(self.id, image=img)

	def next_phase(self):
		self.update_img()
		self.phase = (self.phase + 1) % self.phases_num 

	def animate(self, direction = None):
		if not self.automatic_animation:
			if direction != None:
				self.set_direction(direction)
			self.states['moving'] = True
		else:
			raise NameError('You set this object automatically animated. It is not necessary to call this function.')
			
	def move(self, direction = None):
		'''
			Moves anim object given direction
		'''
		if direction != None:
				self.set_direction(direction)

		if self.direction == 'RIGHT':
			if self.id is not None:
				#self.canvas.move(self.id, abs(self.dx/len(self.east_array)), 0)
				if self.screen.grid_size:
					self.move_right(self.screen.grid_size)    
				else:
					# self.move_right(self.dx/len(self.right_array))
					self.move_right(self.speed)
		elif self.direction == 'LEFT':
			if self.id is not None:
				if self.screen.grid_size:
					self.move_left(self.screen.grid_size) 
				else:
					# self.move_left(self.dx/len(self.left_array))
					self.move_left(self.speed)
		elif self.direction == 'UP':
			if self.id is not None:
				if self.screen.grid_size:
					self.move_up(self.screen.grid_size) 
				else:
					# self.move_up(self.dx/len(self.up_array))
					self.move_up(self.speed)
		elif self.direction == 'DOWN':
			if self.id is not None:
				if self.screen.grid_size:
					self.move_down(self.screen.grid_size) 
				else:
					# self.move_down(self.dx/len(self.down_array))
					self.move_down(self.speed)

	def make_step(self):
		self.states['moving'] = True
			

class Figure(Sprite):
   
	def __init__(self, **kwargs):
		if not ParamsChecker.check(self, kwargs):
			raise NameError('wrong params given')
		ParamsSetter.set(self, kwargs)

		super().__init__(kwargs['x'], kwargs['y'], kwargs['speed'], kwargs['image'], kwargs['weight'])
		
		if kwargs['image'] == None:
			self.id = self.canvas.create_rectangle(kwargs['x'] - 5, kwargs['y'] - 20, kwargs['x'] + 5, kwargs['y'] + 20, fill = 'black')
			self.attributes['width'] = 10
			self.attributes['height'] = 40
		if self.grid_style:
			self.loop_count = self.help_loop_count = int(kwargs['speed']/10)
		else:
			 self.loop_count = self.help_loop_count = kwargs['speed']
		
		self.can_do_jumping = True

		if self.grid_style:
			self.help_speed = int(self.speed/10) 
		else:
			self.help_speed = self.speed

		self.states.set_default(self)
		self.states['falling'] = False

		if kwargs['tag'] in self.screen.figure_array.keys():
			self.screen.figure_array[kwargs['tag']].append(self)   
		else:
			self.screen.figure_array[kwargs['tag']] = [self] 

		self.body = RigidBody(self, Vector2D(self.x, self.y), Vector2D(self.attributes['width']/2, self.attributes['height']/2), kwargs['weight'], Vector2D())
	

	def update_grid_attr(self):
		if self.grid_style:
			self.help_speed = int(self.speed/10)
			self.loop_count = self.help_loop_count = int(self.speed/10)

	def move_left(self, x = 0):
		self.direction = 'LEFT'
		super().move_left(x)

	def move_right(self, x = 0):
		self.direction = 'RIGHT'
		super().move_right(x)

	def move_up(self, y = 0):
		self.direction = 'UP'
		super().move_up(y)

	def move_down(self, y = 0):
		self.direction = 'DOWN'
		super().move_down(y)

	def move(self, direction = None):
		# public
		if direction == None:
			direction = self.direction
		if direction not in DIRECTIONS:
			raise NameError('Wrong direction given.')  # given: daco, expected: daco
		if direction == 'RIGHT':
			self.move_right()
		elif direction == 'LEFT':
			self.move_left()
		elif direction == 'DOWN':
			self.move_down()
		elif direction == 'UP':
			self.move_up()
	
	def jump(self): 
		# prec
		if self.can_do_jumping:         
			if self.help_loop_count != 0:
				self.states['standing'] = False
				self.states['moving'] = True
				self.states['jumping'] = True
				self.canvas.move(self.id, 0, -self.help_speed)
				self.help_loop_count -= 1
				self.y -= self.help_speed
				self.help_speed -= 0.5
			else:
				self.states['jumping'] = False  # pred tym false
				self.help_loop_count = self.loop_count
				if self.grid_style:
					self.help_speed = self.speed/10 # !!!!!!!!!!!!!!!!!!!!!!! TU
				else:
					self.help_speed = self.speed


class Tile(Base):
	
	def __init__(self, x, y, width = 50, height = 50, speed = 0, image = None, color = 'green', tag = None):
		super().__init__(x + width/2, y + height/2, speed, image, 100000)
		if image == None:
			self.id = self.canvas.create_rectangle(x, y , x + width, y + height, fill = color)
		self.attributes['width'] = width
		self.attributes['height'] = height
		self.color = color

		if tag in self.screen.tile_array.keys():
			self.screen.tile_array[tag].append(self)   
		else:
			self.screen.tile_array[tag] = [self] 

		self.body = RigidBody(self, Vector2D(self.x, self.y), Vector2D(self.attributes['width']/2, self.attributes['height']/2), 100000, Vector2D(self.dx, self.dy))
 
	def __getitem__(self, key):
		return self.attributes[key]

	def change_color(self, color):
		self.color = color
		self.canvas.itemconfig(self.id, fill = self.color)

	def move(self):
		pass

class Screen:

	def __init__(self, **kwargs):

		if not ParamsChecker.check(self, kwargs):
			raise NameError('wrong params given')
		ParamsSetter.set(self, kwargs)
	
		self.grid = None
		self.figure_array = dict()
		self.anim_array = dict()
		self.tile_array = dict()
		self.grid_size = 0

		# check right format of input files
		if kwargs['init_file']:
			if kwargs['init_file'].split('.')[1] != 'txt':
				raise WrongParameterError('Input file has to be in .txt format. Your input file has {} format.'.format(kwargs['init_file'].split('.')[1]))
		# if kwargs['background_img']:
		#     if kwargs['background_img'].split('.')[1] != 'png':
		#         raise WrongParameterError('Input image has to be in .png format. Your input image has {} format.'.format(kwargs['background_img'].split('.')[1]))

		if kwargs['width']:
			if not isinstance(kwargs['width'], int) and not isinstance(kwargs['width'], float):
				raise ValueError('Wrong width given. It should be integer or float.')
		if kwargs['height']:
			if not isinstance(kwargs['height'], int) and not isinstance(kwargs['height'], float):
				raise ValueError('Wrong height given. It should be integer or float.')



		if kwargs['init_file'] is None and kwargs['background_img'] is None:
			# self.canvas = tkinter.Canvas(width=600, height=600)
			self.__init_canvas(None, (kwargs['width'], kwargs['height']))
			self.__set_canvases()

		elif kwargs['init_file'] is not None:
			if kwargs['init_file'].split('.')[1] != 'txt':
				raise WrongParameterError('Input file has to be in .txt format. Your input file has {} format.'.format(kwargs['init_file'].split('.')[1]))
			# background from init
			# if kwargs['background_img'] is not None:
			#     # copied images, also window initialized from txt file

			
			self.grid = self.read_grid_file(kwargs['init_file'], kwargs['background_img'])
		  
		elif kwargs['background_img'] and kwargs['width'] and kwargs['height']:
			self.__init_canvas(None, (kwargs['width'], kwargs['height']))
			self.__set_canvases()
			self.draw_bckgrnd_images(kwargs['background_img'])

		else:
			# image = background
			self.bg = tkinter.PhotoImage(file=kwargs['background_img'])
			self.__init_canvas(self.bg)
			self.__set_canvases()
			self.width = self.bg.width()
			self.height = self.bg.height()
			self.id_bg = self.canvas.create_image(0, 0, image=self.bg, anchor='nw')

		# self.canvas.pack()
		
		# Sprite.master = master
		
		self.canvas.bind("<B1-Motion>", self.drag)
		self.canvas.bind("<ButtonRelease-1>", self.release)
		self.canvas.bind("<Motion>", self.motion)

		self.attributes = dict()
		self.attributes['width'] = int(self.canvas['width'])
		self.attributes['height'] = int(self.canvas['height'])
		self.current_key = None
		self.collisions = []

		self.funcs = []
		self.drag_func = None
		self.release_func = None
		self.motion_func = None

		self.time_passed = 0

		self.dt = 0
		
		self.timer()

	def set_timer_interval(self, secs):
		'''
			Sets timer interval in miliseconds.
		'''
		global TIMER_MILISECS
		TIMER_MILISECS = secs

	def waited(self, time_in_seconds):
		'''
			Returns True after given time
		'''
		if self.time_passed == time_in_seconds*1000:
			self.time_passed = 0
			return True
		else:
			self.time_passed += TIMER_MILISECS
			return False

	def get_grid(self):
		'''
			Returns grid as 2 dimensional array.
		''' 
		return self.grid

	def __set_canvases(self):
		self.canvas = CANVAS.get_canvas_obj()
		Base.canvas = CANVAS.get_canvas_obj()
		# Base.canvas = CANVAS.get_canvas_obj()
		Base.screen = self;

	def __init_canvas(self, image = None, size = (None, None)):
		global CANVAS
		CANVAS = CanvasTkinter(image, size)

	def read_grid_file(self, grid_file, background_img):
		screen_reading = False
		grid = []
		settings = dict()
		tile_size = 0
		
		with open(grid_file, 'r') as file:
			lines = file.read().strip().split('\n')
			self.grid_size = tile_size = int(lines[0])
			for line in lines[1:]:
				if line[0] == '_':
					screen_reading = True
					continue
				if screen_reading is False:
					tmp_line = line.split()
					if tmp_line[2] not in INIT_FILE_KEYWORDS:
						raise NameError('Wrong keyword given in init txt file.')
					settings[tmp_line[0]] = tmp_line[2]
				else:
					grid.append(list(line))
		
		result = [[None for i in range(len(grid))] for j in range(len(grid[0]))]
		self.__init_canvas(None, (tile_size*len(grid), tile_size*len(grid[0])))
		self.__set_canvases()
		if background_img:
			self.draw_bckgrnd_images(background_img)
		
		for i in range(len(grid)):
			for j in range(len(grid[i])):
				obj = settings[grid[i][j]]
				if obj == 'Tile':
					tile = Tile(x = j*tile_size, y = i*tile_size, width = tile_size, height = tile_size)
					result[i][j] = tile
					# self.tile_array.append(tile)
				elif obj == 'Figure':
					figure = Figure(x = j*tile_size + tile_size/2, y = i*tile_size + tile_size/2, speed = self.grid_size)
					result[i][j] = figure
					# self.figure_array.append(figure)
				elif obj == 'Anim':
					anim = Anim(x = j*tile_size + tile_size/2, y = i*tile_size + tile_size/2, speed = self.grid_size)
					result[i][j] = anim
					# self.anim_array.append(anim)
		
		return result

	def draw_bckgrnd_images(self, img):
		self.background_images = []
		self.background = ImageTk.PhotoImage(Image.open(img))
		
		rows = int(self.canvas['height'])//self.background.width() + 1
		cols = int(self.canvas['width'])//self.background.width() + 1

		img_width = self.background.width()
		img_height = self.background.height()

		for i in range(rows):
			for j in range(cols):
				obj = self.canvas.create_image(j*img_width + img_width/2, i*img_height + img_height/2, image = self.background)
				self.background_images.append(obj)

	def delete_object(self, obj):
		'''
			Removes object from the screen.
		'''
		obj.delete()
		tag = self.get_tag(obj)
		if isinstance(obj, Anim):
			index = self.anim_array[tag].index(obj)
			self.anim_array[tag][index] = None  

		elif isinstance(obj, Figure):
			index = self.figure_array[tag].index(obj)
			self.figure_array[tag][index] = None

		elif isinstance(obj, Tile):
			index = self.tile_array[tag].index(obj)
			self.tile_array[tag][index] = None
		else:
			raise ValueError('Your object is not the right instance. Object should be instance of the following classes: Anim, Figure, Tile.')

	def get_tag(self, obj):
		'''
			Returns tag of the object.
		'''
		if isinstance(obj, Anim):
			for tag in self.anim_array.keys():
				if obj in self.anim_array[tag]:
					return tag 

		elif isinstance(obj, Figure):
			for tag in self.figure_array.keys():
				if obj in self.figure_array[tag]:
					return tag 

		elif isinstance(obj, Tile):
			for tag in self.tile_array.keys():
				if obj in self.tile_array[tag]:
					return tag 
		else:
			raise ValueError('Your object is not the right instance. Object should be instance of the following classes: Anim, Figure, Tile.')

	def __del_blank_items_from_arrays(self):
		for tag in self.anim_array.keys():
			while None in self.anim_array[tag]:
				self.anim_array[tag].remove(None)

		for tag in self.figure_array.keys():
			while None in self.figure_array[tag]:
				self.figure_array[tag].remove(None)

		for tag in self.tile_array.keys():
			while None in self.tile_array[tag]:
				self.tile_array[tag].remove(None)


	def motion(self, event):
		if self.motion_func is not None:
			self.motion_func(event.x, event.y)

	def release(self, event):
		if self.release_func is not None:
			self.release_func(event.x, event.y)

	def set_motion_function(self, func):
		self.motion_func = func

	def set_release_function(self, func):
		self.release_func = func

	def set_drag_function(self, func):
		self.drag_func = func

	def drag(self, event):
		if self.drag_func is not None:
			self.drag_func(event.x, event.y)

	def change_bg(self, new_image):
		if new_image:
			self.bg = tkinter.PhotoImage(file=new_image)
			self.canvas.itemconfig(self.id_bg, image = self.bg)
			self.width = self.bg.width()
			self.height = self.bg.height()
			# netreba zmenit aj width height parametre?..otestuj
		else:
			raise ValueError('Image parameter can not be empty.')

	def set_grid_size(self, size):
		self.grid_size = size

	def add_tile(self, x = 100, y = 100, width = 50, height = 50, speed = 0, image = None, color = 'green'):
		'''
			Adds new tile to the screen.
		'''
		tile = Tile(x, y, width, height, speed, image, color)
		return tile

	def add_anim_object(self, anim = None, **kwargs):
		'''
			Adds new anim object to the screen.
		'''
		if anim is not None:
			if isinstance(anim, Anim):
				self.anim_array.append(anim)
			else:
				raise NameError('wrong instance')
		else:
			for key in kwargs:
				if key not in ANIM_PARAMS:
					raise NameError('zly paramater zadany')
		   
			new_anim = Anim(**kwargs)
			return new_anim
	
	def add_figure_object(self, figure = None, **kwargs):
		'''
			Adds new figure object to the screen.
		'''
		if figure is not None:
			if not isinstance(figure, Figure):
				raise NameError('wrong instance')
		else:
			for key in kwargs:
				if key not in FIGURE_PARAMS:
					raise NameError('wrong parameter given')

			if self.grid_size != 0:
				kwargs['speed'] = self.grid_size

				new_fig = Figure(**kwargs)
				new_fig.dx = new_fig.dy = self.grid_size
				new_fig.set_grid_style()
				new_fig.update_grid_attr()
			else:
				new_fig = Figure(**kwargs)
			return new_fig

	def get_tile_array(self, tag = None):
		'''
			Returns array of tiles objects according to tag.
		'''
		if tag in self.tile_array.keys():
			return self.tile_array[tag]
		return []

	def get_tiles_by_color(self, color):
		'''
			Returns array of tiles objects according to color.
		'''
		result = []
		for tag in self.tile_array.keys():
			for tile in self.tile_array[tag]:
				if tile.color == color:
					result.append(tile)
		
		return result

	def get_figure_array(self, tag = None):
		'''
			Returns array of figure objects according to tag.
		'''
		if tag in self.figure_array.keys():
			return self.figure_array[tag]
		return []

	def get_anim_array(self, tag = None):
		'''
			Returns array of anim objects according to tag.
		'''
		if tag in self.anim_array.keys():
			return self.anim_array[tag]
		return []

	def get_key_pressed(self):
		'''
			Returns pressed key.
		'''
		key = CANVAS.get_button_pressed()
		if key:
			return key.keysym
		else:
			return None
	   
	def __getitem__(self, key):
		return self.attributes[key]

	def add_func(self, *kwargs):
		'''
			Adds function or functions to execute in timer.
		'''
		for func in kwargs:
			self.funcs.append(func)

	def game_over(self):
		'''
			Stops the game a prints 'GAME OVER!!!' in the midle of the screen.
		'''
		self.funcs = []
		self.final_text = self.canvas.create_text(self['width']/2, self['height']/2, font = 'Arial 25 bold', text = 'GAME OVER!!!')

	def win(self):
		'''
			Stops the game a prints 'YOU WIN!!!' in the midle of the screen.
		'''
		self.funcs = []
		self.final_text = self.canvas.create_text(self['width']/2, self['height']/2, font = 'Arial 25 bold', text = 'YOU WIN!!!')

	def timer(self): 
		# self.canvas.after(TIMER_MILISECS, self.timer)
		for func in self.funcs:
			func()
		
		for tag in self.anim_array.keys():
			for anim in self.anim_array[tag]:
				if anim:
					if anim.automatic_animation:
						anim.next_phase()
						if anim.moving:           
							anim.move()
					elif anim.states['moving']:
						if anim.step_count_minus():
							anim.next_phase()
							anim.move()

		# for tag in self.figure_array.keys():
		# 	for figure in self.figure_array[tag]:
		# 		if figure:
		# 			if figure.states['jumping']:
		# 				figure.jump()

		CANVAS.set_default_click()
		CANVAS.set_default_key()
		self.__del_blank_items_from_arrays()
		self.canvas.after(TIMER_MILISECS, self.timer)
		
