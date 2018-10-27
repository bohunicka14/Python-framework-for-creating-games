from iGame import *
import random

App.start()

window = Screen(background_img = "images/backgrounds/space.png") 
score = Variable(x = 100, y = 20, name = 'Lives', color = 'white', value = 10, font = 'Arial', font_size = 18)

player = Figure(x = window['width']/7, y = window['height']/2, speed = 30, image = 'images/pictures/rocket.png')
window.lives = 10
window.set_timer_interval(100)

def main():
	if window.waited(1):
		window.add_figure_object(x = window['width'] - 25, y = random.randrange(50, window['height'] - 20), speed = 20, image = 'images/pictures/meteor.png', tag = 'meteor')
		
	if get_key_pressed() == 'Up':
		player.move('UP')
		
	if get_key_pressed() == 'Down':
		player.move('DOWN')

	for meteor in window.get_figure_array('meteor'):
		if meteor:
			meteor.move('LEFT')
			if meteor.collides(player):
				window.delete_object(meteor)
				window.lives -= 1
				score.change_value(window.lives)
	
	for meteor in window.get_figure_array('meteor'):
		if meteor:
			if meteor.is_out_of_screen():
				window.delete_object(meteor)

	if window.lives == 0:
		window.game_over()
	
window.add_func(main)
 