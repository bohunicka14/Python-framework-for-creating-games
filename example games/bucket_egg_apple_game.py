from iGame import *
import random

App.start()

window = Screen(background_img = "images/backgrounds/garden_narrow.png") 
score = Variable(x = 100, y = 20, name = 'Score', color = 'white', value = 0, font = 'Arial', font_size = 18)

player = Figure(x = window['width']/2, y = window['height'] - 75, speed = 30, image = 'images/pictures/bucket.png')
window.game_score = 0
window.set_timer_interval(100)

def main():
	if window.waited(2):
		window.add_figure_object(x = random.randrange(50, window['width']), y = 20, speed = 5, image = 'images/pictures/apple.png', tag = 'apple')
	
	if window.waited(2):
		window.add_figure_object(x = random.randrange(50, window['width']), y = 20, speed = 5, image = 'images/pictures/rotten_egg.png', tag = 'rotten_egg')

	if get_key_pressed() == 'Right':
		player.move('RIGHT')
		
	if get_key_pressed() == 'Left':
		player.move('LEFT')
		
	if get_key_pressed() == 'Up':
		player.move('UP')
		
	if get_key_pressed() == 'Down':
		player.move('DOWN')

	for apple in window.get_figure_array('apple'):
		if apple:
			apple.move('DOWN')
			if apple.collides(player):
				window.delete_object(apple)
				window.game_score += 1
				score.change_value(window.game_score)

	for egg in window.get_figure_array('rotten_egg'):
		if egg:
			egg.move('DOWN')
			if egg.collides(player):
				window.delete_object(egg)
				window.game_score -= 1
				score.change_value(window.game_score)
	
	for apple in window.get_figure_array('apple'):
		if apple:
			if apple.is_out_of_screen():
				window.delete_object(apple)

	for egg in window.get_figure_array('rotten_egg'):
		if egg:
			if egg.is_out_of_screen():
				window.delete_object(egg)
		
	if window.game_score == 10:
		window.win()

	if window.game_score < 0:
		window.game_over()
	
window.add_func(main)
 