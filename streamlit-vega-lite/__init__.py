import os
import streamlit.components.v1 as components
import pandas as pd


# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

COMPONENT_NAME = 'vega_lite_selector'

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
def vega_lite_events(spec={}, data=pd.DataFrame(), key=None):
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

    # Create an instance of our component with a constant `name` arg, and
    # print its output value.
    # vega_spec = {
    #     "description": 'A local bar chart with embedded data from python',
    #     "layer": [
    #         {
    #             "data": { "name": "myData" },
    #             "encoding": {
    #                 "x": {"field": 'a', "type": 'ordinal'},
    #                 "y": {"field": 'b', "type": 'quantitative'},
    #                 "strokeWidth": {
    #                     "condition": { "selection": "highlight", "value": 1},
    #                     "value": 2
    #                 }
    #             },
    #             # https: // vega.github.io/vega-lite/docs/selection.html
    #             "selection": {
    #                 "highlight": {
    #                     "type": "single",
    #                      "on": "mouseover"
    #                 }
    #             },
    #             "mark": "bar"
    #         }
    #     ]
    # }

    vega_spec = {
        "description": "A bar chart with on hover and selecting on click. (Inspired by Tableau's interaction style.)",
        "data": {"name": "myData"},
        "selection": {
            "highlight": {"type": "single", "empty": "none", "on": "click"},
            "select": {"type": "multi"}
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

    # df = pd.DataFrame({
    #     'a': ['a', 'b', 'c'],
    #     'b': [1 ,2, 3]
    # })
    st.subheader("Vega Lite + Streamlit Event Emitter")

    vega_data = {
        "myData": [ # key should match the spec
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
