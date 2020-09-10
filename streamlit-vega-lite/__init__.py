import os
import streamlit.components.v1 as components
import pandas as pd


# Create a _RELEASE constant. We"ll set this to False while we"re developing
# the component, and True when we"re ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

COMPONENT_NAME = 'vega_lite_component'

if not _RELEASE:
    _component_func = components.declare_component(
        COMPONENT_NAME,
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        COMPONENT_NAME, path=build_dir)

def vega_lite_component(spec={}, data={}, key=None):
    """Returns selections from the Vega-Lite chart.

    Parameters
    ----------
    spec: dict
        The Vega-Lite spec for the chart. See https://vega.github.io/vega-lite/docs/
        for more info.

        If "data" arg is an object, the "data" key in the spec will be unmodified.
        If "data" arg is a pandas.Dataframe, the "data" key in the spec will be overwritten.

        specs must contain a selection key, and selections must be "projected selections"
        (meaning each selection must contain an "encodings" key with an array of dimensions, e.g. x, y)

    data: dict or pandas.DataFrame
        if object: this should be an object with key names corresponding to named data sources in spec.
        if pandas.DataFrame: no special treatment is needed.

    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component"s arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        The selection object returned by the chart.

        Schema
            name: string
            [key corresponding a dimension]: [array of selected values along that dimension]

        In the case of a multi selection, a key called "vlMulti" may be present too.
    """

    # basic argument validation
    if not spec.get('selection'):
        raise ValueError('Spec must contain a selection')

    for key in spec['selection']:
        if not spec['selection'][key].get('encodings'):
            raise ValueError(
                'Every selection in spec must contain an encodings key')

    # update spec to read the pandas dataframe
    DATAFRAME_KEY = 'DATAFRAME_DATA'
    if isinstance(data, pd.DataFrame):
        spec['data'] = {
            "name": DATAFRAME_KEY
        }

    return _component_func(
        spec=spec, data=data, dataframe_key=DATAFRAME_KEY, key=key, default={})



# Add some test code to play with the component while it"s in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st
    import numpy as np

    bar_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "data": {
            "name": "myData"
        },
        "selection": {
            "clicked": {"type": "multi", "empty": "none", 'encodings': ['x']}
        },
        "mark": "bar",
        "encoding": {
            "x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},
            "y": {"field": "b", "type": "quantitative"},
            "color": {
                "condition": {"selection": "clicked", "value": "firebrick"},
                "value": "steelblue"
            }
        }
    }

    st.subheader("Vega-Lite + Streamlit Event Emitter")

    bar_data = {
        "myData": [
            {"a": "A", "b": 10},
            {"a": "B", "b": 34},
            {"a": "C", "b": 55},
            {"a": "D", "b": 19},
            {"a": "E", "b": 40},
            {"a": "F", "b": 34},
            {"a": "G", "b": 91},
            {"a": "H", "b": 78},
            {"a": "I", "b": 25},
        ],
    }

    basic_event_dict = vega_lite_component(
        spec=bar_spec, data=bar_data)
    st.write(basic_event_dict)

    hist_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "mark": "bar",
        "selection": {
            "brushed": {"type": "interval", "encodings": ['x']}
        },
        "encoding": {
            "x": {
                "bin": True,
                "field": "0" # column name does not survive serialization to frontend, so the columns="x" below had no effect :/
            },
            "y": {"aggregate": "count"}
        }
    }

    np.random.seed(0)
    hist_data = pd.DataFrame(np.random.normal(42, 10, (200, 1)), columns=["x"])
    hist_data

    hist_event_dict = vega_lite_component(
        spec=hist_spec, data=hist_data)
    st.write(hist_event_dict)
