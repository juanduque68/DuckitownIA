#!/usr/bin/env python
# manual

# python usta_test.py --map-name city_3x3_s1 --target av1st1 --mode av
# python usta_test.py --map-name city_3x3_s1 --target av1st1 --mode av --manual-control

import sys
import argparse
import pyglet
import time
from pyglet.window import key
import numpy as np
import gym
import yaml
import gym_duckietown
from gym_duckietown.envs import DuckietownEnv
from gym_duckietown.wrappers import UndistortWrapper
import cv2

from usta_sol import UstaSolution

import logging
gym_logger = logging.getLogger('gym-duckietown')
gym_logger.setLevel(logging.WARNING)

usta_logger = logging.getLogger('usta_test')
usta_logger.setLevel(logging.INFO)

parser = argparse.ArgumentParser()
parser.add_argument('--map-name', required=True, help='map name, without .yaml extension')
parser.add_argument('--target', required=True, help='target location')
parser.add_argument('--mode', required=True, help='target location')
parser.add_argument('--manual-control', action='store_true', help='map name, without .yaml extension')
parser.add_argument('--seed', default=1, type=int, help='seed')
args = parser.parse_args()

if args.mode not in ['ai', 'av']:
    usta_logger.error(f' Mode "{args.mode}" not recognized. Allowed: "ai" and "av"')
    sys.exit(0)

with open(f'./gym_duckietown/maps/{args.map_name}.yaml') as map_file:
    map_dict = yaml.load(map_file)

usta_logger.info(' Starting enviroment...')
env = DuckietownEnv(
        seed = args.seed,
        map_name = args.map_name,
        draw_curve = False,
        draw_bbox = False,
        domain_rand = False,
        frame_skip = 1,
        distortion = False,
    )

env.reset()
env.render()
env.unwrapped.cam_angle[0] = 5.0

@env.unwrapped.window.event
def on_key_press(symbol, modifiers):
    """
    This handler processes keyboard commands that
    control the simulation
    """

    if symbol == key.BACKSPACE or symbol == key.SLASH:
        print('RESET')
        env.reset()
        env.render()

    elif symbol == key.ESCAPE:
        env.close()
        sys.exit(0)

# Register a keyboard handler
key_handler = key.KeyStateHandler()
env.unwrapped.window.push_handlers(key_handler)

sol = UstaSolution(target=args.target, map_dict=map_dict)

action = np.array([0.0, 0.0])

i=0

def update(dt):
    """
    This function is called at every frame to handle
    movement/stepping and redrawing
    """
    global action, i

    """En el siguiente segmento if ejecuta el modo manual"""
    if args.manual_control:
        action = np.array([0.0, 0.0])
        if key_handler[key.UP]:
            action = np.array([0.3, 0.0])
        if key_handler[key.DOWN]:
            action = np.array([-0.3, 0])
        if key_handler[key.LEFT]:
            action = np.array([0.0, + 0.7]) 
        if key_handler[key.RIGHT]:
            action = np.array([0.0, - 0.7])
        if key_handler[key.SPACE]:
            action = np.array([0, 0])
        # Speed boost
        if key_handler[key.LSHIFT]:
            action *= 1.5

    obs, reward, done, info = env.step(action)

    dist, angle, pos, point, curves, global_angle = env.get_lane_pos3(env.cur_pos, env.cur_angle)
    distance_to_road_center = dist
    angle_from_straight_in_deg = angle
    coords = env.get_grid_coords(env.cur_pos) 

    i += 1

    usta_logger.debug(f'distance_to_road_center: {distance_to_road_center}')
    usta_logger.debug(f'angle_from_straight_in_deg: {angle_from_straight_in_deg}')
    usta_logger.debug(f'global_angle: {global_angle}')
    usta_logger.debug(f'coords: {coords}')

    """Es en el siguiente if donde se determina que algoritmo va a usar para
    resolver el mapa."""
    if args.mode == 'ai':
        action = sol.step_ai(   obs=obs, 
                                coord=coords, 
                                dist=distance_to_road_center, 
                                angle=angle_from_straight_in_deg,
                                global_angle=global_angle)
    else:
        action = sol.step_av(obs=obs)

    if done:
        usta_logger.info(' Episode finished.')
        env.reset()

    env.render()

pyglet.clock.schedule_interval(update, 1.0 / env.unwrapped.frame_rate)

# Enter main event loop
usta_logger.info(' Starting test...')
pyglet.app.run()

env.close()
