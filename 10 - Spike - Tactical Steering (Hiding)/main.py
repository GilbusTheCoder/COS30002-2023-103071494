"""Autonomous Agent Movement: Paths and Wandering

Created for COS30002 AI for Games by Clinton Woodward <cwoodward@swin.edu.au>

For class use only. Do not publicly share or post this code without permission.

This code is essentially the same as the base for the previous steering lab
but with additional code to support this lab.

"""
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit
from planet import Planet


def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)


def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            if agent.mode != "hunt":
                agent.mode = AGENT_MODES[symbol]
    elif symbol == KEY.A:
        world.agents.append(Agent(world, mode="wander"))
    elif symbol == KEY.R:
        for agent in world.agents:
            agent.randomize_path()
    elif symbol == KEY.I:
        world.show_info = not world.show_info
        for agent in world.agents:
            agent.show_info = not agent.show_info
        for planet in world.planets:
            planet.show_info = not planet.show_info


def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy


if __name__ == "__main__":
    # create a pyglet window and set glOptions
    win = window.Window(width=1200, height=1000, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = window.FPSDisplay(win)
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(1200, 1000)
    # add one agent & planet
    world.agents.append(Agent(world, 60.0, 20, "hunt"))
    world.planets.append(Planet(win.width, win.height))
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        fps_display.draw()
        # swap the double buffer
        win.flip()
