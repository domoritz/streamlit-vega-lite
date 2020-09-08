import os
import streamlit.components.v1 as components
import pandas as pd


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

COMPONENT_NAME = 'vega_lite_component'

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

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


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
# data can be a PD dataframe or a JSON dict... start with JSON first and investigate JSON table another time.
def vega_lite_component(spec={}, data=pd.DataFrame(), key=None):
    """Returns event dictionary from the vega lite chart

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.

    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(spec=spec, data=data, key=key, default=0)

    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    
    vl_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "data": {
            "name": "myData"
        },
        "selection": {
            "clicked": {"type": "multi", "empty": "none"}
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

    data = {
        "myData": [
            {"a": 'A', "b": 10},
            {"a": 'B', "b": 34},
            {"a": 'C', "b": 55},
            {"a": 'D', "b": 19},
            {"a": 'E', "b": 40},
            {"a": 'F', "b": 34},
            {"a": 'G', "b": 91},
            {"a": 'H', "b": 78},
            {"a": 'I', "b": 25},
        ],
    }

    event_dict = vega_lite_component(spec=vl_spec, data=data)
    st.write(event_dict)
