from ipywidgets import register, Text, widget_serialization
from ipywidgets.widgets.widget_string import TextStyle
from ipywidgets.widgets.trait_types import InstanceDict
from traitlets import Unicode, Bool
from ._version import __npm_module__, __version__


@register
class ClearText(Text):
    """Text box widget with clear button."""
    _model_name = Unicode('ClearTextModel').tag(sync=True)
    _model_module = Unicode(__npm_module__).tag(sync=True)
    _model_module_version = Unicode(__version__).tag(sync=True)

    _view_name = Unicode('ClearTextView').tag(sync=True)
    _view_module = Unicode(__npm_module__).tag(sync=True)
    _view_module_version = Unicode(__version__).tag(sync=True)

    disabled = Bool(False, help="Enable or disable user changes").tag(sync=True)
    continuous_update = Bool(False, help="Update the value as the user types. If False, update on submission, e.g., pressing Enter or navigating away.").tag(sync=True)
    style = InstanceDict(TextStyle).tag(sync=True, **widget_serialization)

    def __init__(self, **kwargs):
        super(ClearText, self).__init__(**kwargs)
