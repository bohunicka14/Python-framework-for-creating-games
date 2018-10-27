from iGame import *
from random import randrange as rr
App.start()

window = Screen(background_img = "images/backgrounds/les.png") 
window.set_timer_interval(100)

dog = Figure(x = 100, y = 300, image = 'images/animations/pes/0.png')

score = Variable(x = 100, y = 20, name = 'Score', color = 'white', value = 0, font = 'Arial', font_size = 18)

window.game_score = 0

def main():
	if window.waited(2):
		dog.hide()

	if window.waited(2):
		dog.set_position(x = random.rr(50, window.width - 50), y = random.rr(50, window.height - 50))
		dog.show()

	if dog.is_clicked() and dog.hidden == False:
		window.game_score += 1
		score.change_value(window.game_score)
	
	if window.game_score == 10:
		window.win()

window.add_func(main)
