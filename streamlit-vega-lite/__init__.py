import os
import streamlit.components.v1 as components
import pandas as pd


# Create a _RELEASE constant. We"ll set this to False while we"re developing
# the component, and True when we"re ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

COMPONENT_NAME = "vega_lite_component"

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We"re naming this
# function "_component_func", with an underscore prefix, because we don"t want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component"s public API.

# It"s worth noting that this call to `declare_component` is the
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

def vega_lite_component(spec={}, key=None, **kwargs):
    """Returns selections from the Vega-Lite chart.

    Parameters
    ----------
    spec: dict
        The Vega-Lite spec for the chart. See https://vega.github.io/vega-lite/docs/
        for more info.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component"s arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.
    **kwargs: pandas.DataFrame or list
        Datasets to be passed to the spec via named datasets.

    Returns
    -------
    dict
        The selections from the chart.

    """
    return _component_func(spec=spec, **kwargs, key=key, default={})


def altair_component(altair_chart, key=None):
    """Returns selections from the Altair chart.

    Parameters
    ----------
    altair_chart: altair.vegalite.v2.api.Chart
        The Altair chart object to display.
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component"s arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict
        The selections from the chart.

    """

    # TODO get spec and data from altair_chart

    return vega_lite_component(spec=spec, data=data, key=key, default={})


def extract_data(altair_chart):
    import altair as alt

    # Normally altair_chart.to_dict() would transform the dataframe used by the
    # chart into an array of dictionaries. To avoid that, we install a
    # transformer that replaces datasets with a reference by the object id of
    # the dataframe. We then fill in the dataset manually later on.

    datasets = {}

    def id_transform(data):
        """Altair data transformer that returns a fake named dataset with the
        object id."""
        datasets[id(data)] = data
        return {"name": str(id(data))}

    alt.data_transformers.register("id", id_transform)

    with alt.data_transformers.enable("id"):
        chart_dict = altair_chart.to_dict()

        # Put datasets back into the chart dict but note how they weren"t
        # transformed.
        chart_dict["datasets"] = datasets

        return chart_dict


# Add some test code to play with the component while it"s in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st
    import numpy as np

    bar_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "data": {
            "name": "bar_data"
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

    bar_data = pd.DataFrame([
        {"a": "A", "b": 10},
        {"a": "B", "b": 34},
        {"a": "C", "b": 55},
        {"a": "D", "b": 19},
        {"a": "E", "b": 40},
        {"a": "F", "b": 34},
        {"a": "G", "b": 91},
        {"a": "H", "b": 78},
        {"a": "I", "b": 25},
    ])

    event_dict = vega_lite_component(spec=bar_spec, bar_data=bar_data)
    st.write(event_dict)


    hist_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "data": {
            "name": "hist_data"
        },
        "mark": "bar",
        "selection": {
            "brushed": {"type": "interval"}
        },
        "encoding": {
            "x": {
                "bin": True,
                "field": "x"
            },
            "y": {"aggregate": "count"}
        }
    }


    st.subheader("Vega-Lite + Streamlit Event Emitter")

    np.random.seed(0)
    hist_data = pd.DataFrame(
        np.random.normal(42, 10, (200, 1)),
        columns=["x"]
    )

    event_dict = vega_lite_component(spec=hist_spec, hist_data=hist_data)
    st.write(event_dict)
