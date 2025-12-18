import streamlit.components.v1 as components
import pathlib

frontend = pathlib.Path(__file__).parent / "frontend.html"

map_component = components.declare_component(
    "map_component",
    path=str(frontend.parent),
)

