# Streamlit Vega-Lite

[![code style black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Downloads](https://img.shields.io/pypi/v/streamlit-vega-lite)](https://pypi.org/project/streamlit-vega-lite)

**🐉 Here be dragons. This is a proof of concept.**

Making Vega-Lite selection created by user interactions available in Python. Works with [Altair](https://altair-viz.github.io/).

For examples, see https://github.com/domoritz/streamlit-vega-lite/blob/master/streamlit_vega_lite/__init__.py. You can also try the demo at https://github.com/domoritz/streamlit-vega-lite-demo. 

<img src="./demo.gif" alt="Demo screencast" width=400></img>

## Documentation

### Installation

`pip install streamlit-vega-lite`

### Usage

There are two functions available. `vega_lite_component` expects a Vega-Lite specification as a dictionary and any named datasets as keyword arguments. The datasets will be transferred as efficient Arrow tables. `altair_component` supports Altair charts and automatically extracts all datasets and transfers them as Arrow dataframes.

#### Example

```python
import altair as alt
import streamlit as st
import pandas as pd
import numpy as np
from streamlit_vega_lite import vega_lite_component, altair_component

hist_data = pd.DataFrame(np.random.normal(42, 10, (200, 1)), columns=["x"])

@st.cache
def altair_histogram():
    brushed = alt.selection_interval(encodings=["x"], name="brushed")

    return (
        alt.Chart(hist_data)
        .mark_bar()
        .encode(alt.X("x:Q", bin=True), y="count()")
        .add_selection(brushed)
    )

event_dict = altair_component(altair_chart=altair_histogram())

r = event_dict.get("x")
if r:
    filtered = hist_data[(hist_data.x >= r[0]) & (hist_data.x < r[1])]
    st.write(filtered)
```

## Dev Setup

Open two terminals in the dev container using VSCode's [Remote Containers Extension](https://code.visualstudio.com/docs/remote/containers).

In the first terminal, run:

```bash
# Install python module in editable mode
pip install -e .

# Launch streamlit app
streamlit run streamlit_vega_lite/__init__.py
```

In the second terminal:

```bash
# Switch to location of frontend code
cd streamlit_vega_lite/frontend
# Install dependencies
yarn
# Launch frontend assets
yarn start
```

Then open http://localhost:8501/.

## Style

Run Black for Python formatting.

```
black . -l 120
```

Run Prettier for other formatting in the frontend directory.

```
yarn format
```

## Publish

See https://docs.streamlit.io/en/stable/publish_streamlit_components.html.

Make sure that `_RELEASE` is set to `True`.

```sh
pushd streamlit_vega_lite/frontend
yarn build
popd
python setup.py sdist bdist_wheel
python3 -m twine upload --repository pypi dist/*
```
