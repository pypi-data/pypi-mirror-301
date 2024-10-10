import napari
from napari.utils import nbscreenshot
from napari_matplotlib import HistogramWidget
from nap_plot_tools import CustomToolbarWidget, CustomToolButton
import numpy as np
from pathlib import Path

def test_tools(make_napari_viewer):
    viewer = make_napari_viewer()

    plotter = HistogramWidget(viewer)

    icon_folder_path = Path().parent.resolve().parent / 'icons'

    custom_toolbar = CustomToolbarWidget()
    name = 'select'
    custom_toolbar.add_custom_button(name=name,
                                 tooltip="Select something", 
                                 default_icon_path=Path(icon_folder_path / "select.png"),
                                 checkable=True, 
                                 checked_icon_path=Path(icon_folder_path / "select_checked.png")
                                 )
    assert len(custom_toolbar.buttons) == 1
    assert custom_toolbar.buttons[name] is not None
    assert custom_toolbar.buttons['select'].isCheckable() == True
    button_state = custom_toolbar.get_button_state(name)
    assert button_state is not None
    assert button_state == False
    custom_toolbar.set_button_state(name, True)
    button_state = custom_toolbar.get_button_state(name)
    assert button_state == True

    
    custom_button = CustomToolButton(default_icon_path=Path(icon_folder_path / "select.png"))

