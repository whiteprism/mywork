# -*- coding: utf-8 -*-

from tutorial.models import Tutorial, TutorialDetail, Plot

def update_tutorial_cache():
    Tutorial.create_cache()
    Plot.create_cache()
    TutorialDetail.create_cache()

def get_tutorials():
    return Tutorial.get_all_list()

def get_tutorialdetails():
    return TutorialDetail.get_all_list()

def get_plots():
    return Plot.get_all_list()
