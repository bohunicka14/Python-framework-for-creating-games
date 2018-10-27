from iGame import *

App.start()

window = Screen(background_img = "images/backgrounds/space.png") 

window.add_tile(100, 0, 75, window['height'] - 100)
window.add_tile(400, 0, 75, window['height'] - 100)
window.add_tile(700, 0, 75, window['height'] - 100)

window.add_tile(250, 250, 75, window['height']-250)
window.add_tile(550, 250, 75, window['height']-250)

aim = window.add_tile(x = window['width'] - 50, y = window['height'] - 50, width = 50, height = 50, color = 'red')

ball = Figure(x = 45, y = 45, speed = 15, image = 'images/pictures/ball.png')

def main():
    if get_key_pressed() == 'Right':
        ball.move('RIGHT')
        if ball.collides(window.get_tiles_by_color('green')):
            ball.move('LEFT')
    if get_key_pressed() == 'Left':
        ball.move('LEFT')
        if ball.collides(window.get_tiles_by_color('green')):
            ball.move('RIGHT')
    if get_key_pressed() == 'Up':
        ball.move('UP')
        if ball.collides(window.get_tiles_by_color('green')):
            ball.move('DOWN')
    if get_key_pressed() == 'Down':
        ball.move('DOWN')
        if ball.collides(window.get_tiles_by_color('green')):
            ball.move('UP')
    if ball.collides_with_wall():
        ball.step_back()

    if ball.touching_color(window.get_tile_array(), 'red'):
        aim.change_color('purple')
        window.win()
    
window.add_func(main)
