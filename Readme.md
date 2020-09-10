# Streamlit Vega-Lite

**🐉 Work in progress. Do not use yet.**

Making Vega-Lite selection created by user interactions available in Python. Works with [Altair](https://altair-viz.github.io/).

## Dev Setup

Open two terminals in the dev container using VSCode's [Remote Containers Extension](https://code.visualstudio.com/docs/remote/containers).

In the first terminal, run:

```bash
# Install python module in editable mode
pip install -e .

# Launch streamlit app
streamlit run streamlit-vega-lite/__init__.py
```

In the second terminal:

```bash
# Switch to location of frontend code
cd streamlit-vega-lite/frontend
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
