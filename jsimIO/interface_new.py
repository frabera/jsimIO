from .distributions import *
# from .strategies import _SchedStrategy
from .model import _Model
from .userclasses import *
from .nodes import *


# UTILS


def link_classes_and_nodes(model):
    for node in model.nodes:
        node.classes_referenced = [
            userclass for userclass in model.userclasses
            if userclass.reference_station is node]


def add_logger(baked_model, node):
    baked_model.add_child(_Logger(baked_model, f"LOG_{node.name}"))


def bake(model, fill_loggers=True):
    link_classes_and_nodes(model)
    baked_model = _Model(model, options=model.options)

    # Add userclass ELEMENTS
    add_userclass_elements(model, baked_model)

    # Add nodes ELEMENTS
    for node in enumerate(model.nodes):
        node.add_to_model()
