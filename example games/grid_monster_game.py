from iGame import *
import random

App.start()

window = Screen(background_img = "images/backgrounds/tile.png", init_file = 'monster_game_init_file.txt') 
# score = Variable(x = 100, y = 20, name = 'Score', color = 'white', value = 0, font = 'Arial', font_size = 18)

# player = Figure(x = window['width']/2, y = window['height'] - 75, speed = 30, image = 'pictures/bucket.png')
# window.game_score = 0

window.set_timer_interval(100)

grid = window.get_grid()

monster1 = grid[1][2]
monster2 = grid[3][4]
monster3 = grid[7][1]
monster4 = grid[1][10]
monster5 = grid[9][7]

player = grid[7][7]

monster1.set_images(file_name1 = 'images/animations/priserka/.png', file_name2 = 'images/animations/priserka/.png', phases_num = 4, direction1 = 'UP', direction2 = 'LEFT')
monster2.set_images(file_name1 = 'images/animations/priserka/.png', file_name2 = 'images/animations/priserka/.png', phases_num = 4, direction1 = 'UP', direction2 = 'LEFT')
monster3.set_images(file_name1 = 'images/animations/priserka/.png', file_name2 = 'images/animations/priserka/.png', phases_num = 4, direction1 = 'UP', direction2 = 'LEFT')
monster4.set_images(file_name1 = 'images/animations/priserka/.png', file_name2 = 'images/animations/priserka/.png', phases_num = 4, direction1 = 'UP', direction2 = 'LEFT')
monster5.set_images(file_name1 = 'images/animations/priserka/.png', file_name2 = 'images/animations/priserka/.png', phases_num = 4, direction1 = 'UP', direction2 = 'LEFT')

player.change_image('images/pictures/cat.png')

window.score = 0

score = Variable(x = 70, y = 20, name = 'Score', color = 'blue', value = 0, font = 'Arial', font_size = 18)

def main():

    if player.waited(0.5):
        new_apple = window.add_figure_object(x = random.randrange(1, 11)*75 - 37.5, y = random.randrange(1, 11)*75 - 37.5, speed = 0, image = 'images/pictures/apple.png', tag = 'apple')
        if new_apple.collides(window.get_tile_array()):
            window.delete_object(new_apple)

    for apple in window.get_figure_array('apple'):
        if apple:
            if player.collides(apple):
                window.score += 1
                score.change_value(window.score)
                window.delete_object(apple)

    for monster in monster1, monster2, monster3, monster4, monster5:
        if monster.collides(player):
            window.score -= 1
            score.change_value(window.score)
            player.set_position(x = 8*75 - 37.5, y = 8*75 - 37.5)

    if get_key_pressed() == 'Right':
        player.move('RIGHT')
        
    if get_key_pressed() == 'Left':
        player.move('LEFT')
        
    if get_key_pressed() == 'Up':
        player.move('UP')
        
    if get_key_pressed() == 'Down':
        player.move('DOWN')
        
    if player.collides(window.get_tiles_by_color('green')):
        player.step_back()

    if player.collides_with_wall():
        player.step_back()

    if window.waited(0.5):
        for monster in monster1, monster2, monster3, monster4, monster5:
            monster.direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
            monster.move()

        
        for monster in monster1, monster2, monster3, monster4, monster5:
            if monster.collides(window.get_tiles_by_color('green')):
                monster.step_back()

        
        for monster in monster1, monster2, monster3, monster4, monster5:
            if monster.collides_with_wall():
                monster.step_back()

    if window.score == 20:
        window.win()
   
    
window.add_func(main)
 