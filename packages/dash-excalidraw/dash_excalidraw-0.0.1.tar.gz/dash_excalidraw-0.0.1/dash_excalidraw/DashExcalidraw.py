# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class DashExcalidraw(Component):
    """A DashExcalidraw component.


Keyword arguments:

- id (string; optional)

- appState (dict; optional)

- elements (list; optional)

- height (string; default '400px')

- initialData (dict; optional)

- width (string; default '100%')"""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'dash_excalidraw'
    _type = 'DashExcalidraw'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, width=Component.UNDEFINED, height=Component.UNDEFINED, initialData=Component.UNDEFINED, elements=Component.UNDEFINED, appState=Component.UNDEFINED, **kwargs):
        self._prop_names = ['id', 'appState', 'elements', 'height', 'initialData', 'width']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'appState', 'elements', 'height', 'initialData', 'width']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        super(DashExcalidraw, self).__init__(**args)
