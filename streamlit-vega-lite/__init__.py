import os
import streamlit.components.v1 as components
import pandas as pd


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

COMPONENT_NAME = 'vega_lite_selector'

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
def vega_lite_events(spec={}, data=pd.DataFrame(), key=None):
    """Returns event dictionary from the vega lite selection event

    Parameters
    ----------
    spec: dict
        A dictionary complying with the vega lite specification.
        If "data" arg is an object, the "data" key in the spec will be unmodified.
        If "data" arg is a pandas.Dataframe, the "data" key in the spec will be overwritten.

        specs must contain a selection key, and selections must be "projected selections"
        (meaning each selection must contain an "encodings" key with an array of dimensions, e.g. x, y)

    data: dict or pandas.DataFrame
        if object: this should be an object with key names corresponding to named data sources in spec.
        if pandas.DataFrame: no special treatment is needed.

    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        The selection object returned by interacting with the vega lite API.
        Schema
            name: string
            [key corresponding a dimension]: [array of selected values along that dimension]

        In the case of a multi selection, a key called "vlMulti" may be present too.
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.

    # basic argument validation
    if not spec.get('selection'):
        raise ValueError('Spec must contain a selection')

    for key in spec['selection']:
        if not spec['selection'][key].get('encodings'):
            raise ValueError('Every selection in spec must contain an encodings key')

    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(spec=spec, data=data, key=key, default={})

    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st

    vega_spec = {
        "description": "A bar chart with on hover and selecting on click. (Inspired by Tableau's interaction style.)",
        "data": {"name": "myData"},
        "selection": {
            "highlight": {"type": "single", "empty": "none", "on": "mouseover", "encodings": ['x']},
            "brush": {"type": "interval", "encodings": ['x']},
            "select": {"type": "multi", "encodings": ['x']}
        },
        "mark": {
            "type": "bar",
            "fill": "#4C78A8",
            "stroke": "black",
            "cursor": "pointer"
        },
        "encoding": {
            "x": {"field": "a", "type": "ordinal"},
            "y": {"field": "b", "type": "quantitative"},
            "fillOpacity": {
                "condition": {"selection": "select", "value": 1},
                "value": 0.3
            },
            "strokeWidth": {
                "condition": [
                    {
                        "test": {
                            "and": [
                                {"selection": "select"},
                                "length(data(\"select_store\"))"
                            ]
                        },
                        "value": 2
                    },
                    {"selection": "highlight", "value": 1}
                ],
                "value": 0
            }
        },
        "config": {
            "scale": {
                "bandPaddingInner": 0.2
            }
        }
    }

    st.subheader("Vega Lite + Streamlit Event Emitter")
    vega_data = {
        "myData": [ # key should match spec.data.name
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

    event_dict = vega_lite_events(spec=vega_spec, data=vega_data)
    st.write(event_dict)


    df = pd.DataFrame({
        'a': ['a', 'b', 'c'],
        'b': [1 ,2, 3]
    })

    # df

    # st.markdown("You've clicked %s times!" % int(num_clicks))

    # st.markdown("---")


    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    # name_input = st.text_input("Enter a name", value="Streamlit")
    # num_clicks = my_component(name_input, key="foo")
    # st.markdown("You've clicked %s times!" % int(num_clicks))
