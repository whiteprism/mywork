# -*- coding: utf-8 -*-
from robot.models import Robot

def update_robot_cache():
    Robot.create_cache()

def get_robots():
    return Robot.get_all_list()


def get_robot(pk):
    return Robot.get(int(pk))
    
