# -*- coding: utf-8 -*-
from artifact.models import Artifact,ArtifactAttribute, ArtifactFragment, ArtifactEnhance, ArtifactRefine

def update_artifact_cache():
    Artifact.create_cache()
    ArtifactFragment.create_cache()
    ArtifactEnhance.create_cache()
    ArtifactRefine.create_cache()
    ArtifactAttribute.create_cache()
    # ArtifactFragmentGrabProb.create_cache()

def get_artifact(pk):
    return Artifact.get(int(pk))

def get_artifacts():
    return Artifact.get_all_list()

def get_artifactfragment(pk):
    return ArtifactFragment.get(int(pk))

def get_artifactfragments():
    return ArtifactFragment.get_all_list()

def get_artifactenhance(quality, level):
    pk = str(quality * 1000 + level)
    return ArtifactEnhance.get(int(pk))

def get_artifactenhances():
    return ArtifactEnhance.get_all_list()

def get_artifactrefine(quality, level):
    pk = str(quality *100 + level)
    return ArtifactRefine.get(int(pk))

def get_artifactrefines():
    return ArtifactRefine.get_all_list()

# def get_artifactfragment_grabprob(pk):
#     return ArtifactFragmentGrabProb.get(int(pk))
