import streamlit.components.v1 as components
import os

_component_func = components.declare_component(
    "map_component",
    path=os.path.join(os.path.dirname(__file__), "frontend")
)

def map_component():
    return _component_func()
