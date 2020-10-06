import os
import streamlit.components.v1 as components
import pandas as pd


# Set this to False while we're developing the component, and True when we're
# ready to package and distribute it.
_RELEASE = True

COMPONENT_NAME = "vega_lite_component"

if not _RELEASE:
    _component_func = components.declare_component(
        COMPONENT_NAME, url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(COMPONENT_NAME, path=build_dir)


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

    # basic argument validation
    if not spec.get("selection"):
        raise ValueError("Spec must contain selection")

    for selection in spec["selection"].values():
        if (
            (selection["type"] == "single" or selection["type"] == "multi")
            and not selection.get("encodings")
            and not selection.get("fields")
        ):
            raise ValueError(
                "Every single and multi selection in spec must be projected onto encodings or fields."
            )

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

    import altair as alt

    # Normally altair_chart.to_dict() would transform the dataframe used by the
    # chart into an array of dictionaries. To avoid that, we install a
    # transformer that replaces datasets with a reference by the object id of
    # the dataframe. We then fill in the dataset manually later on.

    datasets = {}

    # make a copy of the chart so that we don't have to rerender it even if nothing changed
    altair_chart = altair_chart.copy()

    def id_transform(data):
        """Altair data transformer that returns a fake named dataset with the
        object id."""
        name = f"d{id(data)}"
        datasets[name] = data
        return {"name": name}

    alt.data_transformers.register("id", id_transform)

    with alt.data_transformers.enable("id"):
        chart_dict = altair_chart.to_dict()

    return _component_func(spec=chart_dict, **datasets, key=key, default={})


# Add some test code to play with the component while it"s in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/__init__.py`
if not _RELEASE:
    import streamlit as st
    import numpy as np
    import altair as alt

    st.subheader("Vega-Lite + Streamlit Event Emitter")

    bar_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "data": {"name": "bar_data"},
        "selection": {
            "clicked": {"type": "multi", "empty": "none", "encodings": ["x"]}
        },
        "mark": "bar",
        "encoding": {
            "x": {"field": "a", "type": "nominal", "axis": {"labelAngle": 0}},
            "y": {"field": "b", "type": "quantitative"},
            "color": {
                "condition": {"selection": "clicked", "value": "firebrick"},
                "value": "steelblue",
            },
        },
    }

    bar_data = pd.DataFrame(
        [
            {"a": "A", "b": 10},
            {"a": "B", "b": 34},
            {"a": "C", "b": 55},
            {"a": "D", "b": 19},
            {"a": "E", "b": 40},
            {"a": "F", "b": 34},
            {"a": "G", "b": 91},
            {"a": "H", "b": 78},
            {"a": "I", "b": 25},
        ]
    )

    event_dict = vega_lite_component(spec=bar_spec, bar_data=bar_data)
    selection = event_dict.get("a")
    if selection:
        fields = " and ".join(selection)
        st.write(f"You selected on { fields }.")
    else:
        st.write("You haven't selected any bars yet.")

    st.subheader("Vega-Lite + Streamlit Event Emitter")

    hist_spec = {
        "$schema": "https://vega.github.io/schema/vega-lite/v4.json",
        "data": {"name": "hist_data"},
        "mark": "bar",
        "selection": {"brushed": {"type": "interval"}},
        "encoding": {"x": {"bin": True, "field": "x"}, "y": {"aggregate": "count"}},
    }

    np.random.seed(0)
    hist_data = pd.DataFrame(np.random.normal(42, 10, (200, 1)), columns=["x"])

    event_dict = vega_lite_component(spec=hist_spec, hist_data=hist_data)

    def print_range(r):
        st.write(
            f"You selected data in the range from {r[0]:.1f} to {r[1]:.1f}."
            if r
            else "You haven't selected anything yet."
        )

    print_range(event_dict.get("x"))

    st.subheader("Altair + Streamlit Event Emitter")

    @st.cache
    def make_altair_histogram():
        brushed = alt.selection_interval(encodings=["x"], name="brushed")
        return (
            alt.Chart(hist_data)
            .mark_bar()
            .encode(alt.X("x:Q", bin=True), y="count()",)
            .add_selection(brushed)
        )

    chart = make_altair_histogram()
    event_dict = altair_component(altair_chart=chart)
    r = event_dict.get("x")
    print_range(r)

    if r:
        filtered = hist_data[(hist_data.x >= r[0]) & (hist_data.x < r[1])]
        st.write(filtered.describe())
