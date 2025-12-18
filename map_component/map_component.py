import os
import streamlit.components.v1 as components

_component = components.declare_component(
    "map_component",
    path=os.path.join(os.path.dirname(__file__), "frontend"),
)

def map_component():
    return _component()
