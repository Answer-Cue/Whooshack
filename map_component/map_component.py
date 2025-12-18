import streamlit.components.v1 as components
from pathlib import Path

_component_func = components.declare_component(
    "map_component",
    path=str(Path(__file__).parent / "frontend"),
)

def map_component():
    return _component_func()
