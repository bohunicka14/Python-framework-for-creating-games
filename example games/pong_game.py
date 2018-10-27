from iGame import *

App.start()

window = Screen(width = 1000, height = 600) 

player1 = Figure(x = 200, y = 300, image = 'images/pictures/player_pong_game.png', weight = 100000)
player2 = Figure(x = 800, y = 300, image = 'images/pictures/player_pong_game.png', weight = 100000)

ball = Figure(x = 500, y = 300, image = 'images/pictures/ball_pong_game.png')

score1 = Variable(x = window['width']/4, y = 50, name = 'player 1', color = 'green', value = 0, font = 'Arial', font_size = 18)
score2 = Variable(x = 3*window['width']/4, y = 50, name = 'player 2', color = 'green', value = 0, font = 'Arial', font_size = 18)

window.score1 = 0
window.score2 = 0

ball.set_velocity(random.choice([1, -1]) * random.randrange(80, 100), random.choice([1, -1]) * random.randrange(80, 100))

def main():

	if get_key_pressed() == 'w':
		player1.move_up(20)

	if get_key_pressed() == 's':
		player1.move_down(20)

	if get_key_pressed() == 'Up':
		player2.move_up(20)

	if get_key_pressed() == 'Down':
		player2.move_down(20)

	
	if ball.collides_with_wall('TOP') or ball.collides_with_wall('BOTTOM'):
		ball.bounce()

	if ball.collides_with_wall('LEFT'):

		window.score2 += 1
		score2.change_value(window.score2)

		ball.set_position(x = window['width']/2, y = random.randrange(10, window['height'] - 10))
		ball.set_velocity(random.choice([1, -1]) * random.randrange(80, 100), random.choice([1, -1]) * random.randrange(80, 100))

	if ball.collides_with_wall('RIGHT'):

		window.score1 += 1
		score1.change_value(window.score1)

		ball.set_position(x = window['width']/2, y = random.randrange(10, window['height'] - 10))
		ball.set_velocity(random.choice([1, -1]) * random.randrange(80, 100), random.choice([1, -1]) * random.randrange(80, 100))

	for player in player1, player2:
		if ball.collides(player):
			
			ball.bounce(player)

	ball.make_step()

	

window.add_func(main)