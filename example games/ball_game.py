from iGame import *

App.start()

window = Screen(background_img = "images/backgrounds/galaxy.png") 

window.set_timer_interval(25)

line = Figure(x = window.width/2, y = window.height - 30, image = 'images/pictures/line.png', weight = 100000)
ball = Figure(x = 250, y = 250, speed = 20, image = 'images/pictures/ball.png')

for i in range(9):
	window.add_tile(x=150 + i*100, y=100, width=100, height=50, speed=0, image=None, color='green')

for i in range(7):
	window.add_tile(x=250 + i*100, y=150, width=100, height=50, speed=0, image=None, color='green')

for i in range(5):
	window.add_tile(x=350 + i*100, y=200, width=100, height=50, speed=0, image=None, color='green')

def motion(x, y):
	line.set_position(x = x)

window.set_motion_function(motion)
ball.set_velocity(random.randrange(100, 150), random.randrange(100, 150))

def main():

	if ball.collides(line):
		# ball.set_velocity(random.choice([1, -1])*random.randrange(1, 3), -ball.velocity_y)
		ball.bounce(line)

	if ball.collides_with_wall('BOTTOM'):

		ball.set_position(x = window['width']/2, y = window['height']/2)
		ball.set_velocity(random.choice([1, -1]) * random.randrange(80, 100), random.choice([1, -1]) * random.randrange(80, 100))

	if ball.collides_with_wall('TOP') or ball.collides_with_wall('LEFT') or ball.collides_with_wall('RIGHT'):
		ball.bounce()


	for tile in window.get_tile_array():
		if ball.collides(tile):
			# ball.set_velocity(random.choice([1, -1])*ball.velocity_x, -ball.velocity_y)
			ball.bounce(tile)

			window.delete_object(tile)
			# window.get_tile_array().remove(tile)
			break

	ball.make_step()

	if len(window.get_tile_array()) == 0:
		window.win() 


window.add_func(main)
