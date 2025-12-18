# map_component/map_component.py
import streamlit.components.v1 as components
import os

# フロントエンドの build ディレクトリ
_component_func = components.declare_component(
    "map_component",
    path=os.path.join(os.path.dirname(__file__), "frontend"),
)

def map_component():
    """
    戻り値:
    {
      "lat": number,
      "lng": number
    }
    """
    return _component_func()
