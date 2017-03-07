# -*- coding: utf-8 -*-
from skill.models import *

def update_skill_cache():
    SkillEffect.create_cache()
    SkillLevel.create_cache()
    SkillEffectDetail.create_cache()
    Skill.create_cache()
    Conditions.create_cache()
    Condition.create_cache()
    Flag.create_cache()
    SkillLevelUpCosts.create_cache()

def get_flag_configs():
    return Flag.get_all_list()

def get_skills():
    return Skill.get_all_list()

def get_skilllevel(skill_or_skill_id, level):
    pk = skill_or_skill_id * 100 + level
    return SkillLevel.get(pk)

def get_skilllevels_by_skill(skill_or_skill_id):
    return SkillLevel.get_skilllevels(skill_or_skill_id)

def get_conditions_all():
    return Conditions.get_all_list()

def get_conditions():
    return Condition.get_all_list()
