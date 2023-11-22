from pyglet import window, clock
from pyglet.gl import *
from graphics import egi, KEY
from random import randint

from world import World
from soldier import Soldier, WEAPONS
from enemy import Enemy
from gun_stuff import *


def on_key_press(symbol, modifiers):
    if symbol == KEY.I:
        for object in world.objects:
            object.show_info = not object.show_info
    elif symbol == KEY.A:
        soldier = Soldier(
            world, randint(100, win_x - 100), randint(100, win_y - 100), 30
        )
        world.append_obj(soldier)
    elif symbol == KEY.S:
        enemy = Enemy(world, randint(100, win_x - 100), randint(100, win_y - 100), 30)
        world.append_obj(enemy)
    elif symbol in WEAPONS:
        for object in world.objects:
            if type(object) == Soldier:
                object.weapon = WEAPONS[symbol]


if __name__ == "__main__":
    win_x = 1000
    win_y = 800

    game_window = window.Window(width=win_x, height=win_y, vsync=True, resizable=False)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    egi.InitWithPyglet(game_window)
    fps_hud = window.FPSDisplay(game_window)

    game_window.push_handlers(on_key_press)

    world = World(width=win_x, height=win_y)

    while not game_window.has_exit:
        game_window.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_hud.draw()

        game_window.flip()
